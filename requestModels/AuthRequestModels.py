from pydantic import BaseModel


class Signup(BaseModel):
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    is_admin:bool
    access_token: str
    token_type: str
