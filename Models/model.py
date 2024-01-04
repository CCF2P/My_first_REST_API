from pydantic import BaseModel, Field
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import json

CLIENT_SECRET = "dV01GiUqczgCxafe7tIKoY2Ck3ElufSc"
ALGORITHM = "RS256"


class UserCreate(BaseModel):
    #id: int
    name: str
    task: str


class KeycloakToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    not_before_policy: int = Field(alias="not-before-policy")
    session_state: str
    scope: str


class KeycloakJWTBearerHandler(HTTPBearer):
    def __init__(self) -> None:
        super(KeycloakJWTBearerHandler, self).__init__()

    async def __call__(self, request: Request):
        KeycloakJWTBearerHandler._check_request_headers(request._headers)

        credentials: HTTPAuthorizationCredentials = await super(KeycloakJWTBearerHandler, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        if not KeycloakJWTBearerHandler._verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        return credentials.credentials
    
    @staticmethod
    def _verify_jwt(credentials):
        decode_credentials = KeycloakJWTBearerHandler._decode_jwt(credentials)
        
        # check if the user has the role: my-role
        roles: list = decode_credentials["payload"]["realm_access"]["roles"]
        if "my-role" not in roles:
            raise HTTPException(status_code=403, detail="The user does not have the required role")

        return True

    @staticmethod
    def _check_request_headers(headers):
        # check there is an authorization header
        if "authorization" not in headers.keys():
            raise HTTPException(status_code=403, detail="Header has not attribute: authorization")
        
        # check if the authorization token is empty
        auth_value = headers.getlist("authorization")
        if len(auth_value) == 0:
            raise HTTPException(status_code=403, detail="Authorization token is empty")
        
        # check if the token begins with the word Bearer
        value = auth_value[0].split(" ")
        if value[0] != "Bearer":
            raise HTTPException(status_code=403, detail="The authorization token must begin with the word 'Bearer'")
        
        # check if there is a token after the word Bearer
        if len(value) != 2 or value[1] == "":
            raise HTTPException(status_code=403, detail="Authorization token is wrong")

        return True

    @staticmethod
    def _decode_jwt(token):        
        header = jwt.get_unverified_header(token)
        data = jwt.decode(jwt=token,
                        key="secret",
                        algorithms=[ALGORITHM],
                        options={"verify_signature": False},)
        
        payload = json.loads(json.dumps(data))

        return {"header": header, "payload": payload}
