from fastapi import APIRouter
from jose import jwt

from Models.model import Token


class KeycloakJWTBearerHandler():
    httpClient: str
    memoryCache: str
    appConfig: str
    logger: str
    tokenHelper: str

    def __init__(
            self, 
            httpClient, 
            memoryCache, 
            appConfig, 
            logger, 
            tokenHelper
        ) -> None:
        self.httpClient = httpClient
        self.memoryCache = memoryCache
        self.appConfig = appConfig
        self.logger = logger
        self.tokenHelper = tokenHelper
    
    


auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post("/")
def root(token: Token):
    return token
