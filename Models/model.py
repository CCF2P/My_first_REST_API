from pydantic import BaseModel


class UserCreate(BaseModel):
    #id: int
    name: str
    task: str


class Token(BaseModel):
    access_token: str
    token_type: str
