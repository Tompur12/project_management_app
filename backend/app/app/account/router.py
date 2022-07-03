from fastapi import APIRouter
from .schema import UserSchema
from .models import User


account_router = APIRouter()


@account_router.post("/create")
async def create(request: UserSchema):
    await User.create(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name
    )
# TODO add validation for create
