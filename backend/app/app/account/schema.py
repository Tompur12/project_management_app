from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class GetUserByIdSchema(BaseModel):
    id: int


class GetUserByEmailSchema(BaseModel):
    email: str
