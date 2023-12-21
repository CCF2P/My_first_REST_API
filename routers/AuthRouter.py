from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import jwt
import json

from Models.model import KeycloakToken

CLIENT_SECRET = "dV01GiUqczgCxafe7tIKoY2Ck3ElufSc"
ALGORITHM = "RS256"


class KeycloakJWTBearerHandler():
    def __init__(self) -> None:        
        self.token = None

    def set_token(self, token: KeycloakToken) -> None:
        self.token = self._decode_jwt(token)

    @staticmethod
    def _decode_jwt(token):
        if token is None:
            raise Exception("current token is empty")
        
        if token.access_token == "":
            raise Exception("access token is empty")
        
        header = jwt.get_unverified_header(token.access_token)
        data = jwt.decode(jwt=token.access_token,
                        key="secret",
                        algorithms=[ALGORITHM],
                        options={"verify_signature": False},)
        
        payload = json.loads(json.dumps(data))

        if payload["typ"] != "Bearer":
            raise Exception("wrong type token")

        return {"header": header, "payload": payload}


auth_router = APIRouter(
    prefix="/auth"
)
keycloakJWTBearerHandler = KeycloakJWTBearerHandler()


@auth_router.post("/")
def root(token: KeycloakToken):
    try:        
        keycloakJWTBearerHandler.set_token(token)

        return keycloakJWTBearerHandler.token
    except Exception as e:
        return JSONResponse(content={"message": f"{e}"},
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
