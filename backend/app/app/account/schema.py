from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class GetUserByIdAndDeleteUserSchema(BaseModel):
    id: int


class GetUserByEmailSchema(BaseModel):
    email: str


class UpdateUserSchema(BaseModel):
    id: int
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
