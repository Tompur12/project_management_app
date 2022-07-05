from fastapi import APIRouter, Response, status
from .schema import (
    UserSchema,
    GetUserByIdSchema,
    GetUserByEmailSchema,
)
from .models import User
from ..core.exceptions import (
    NotFound,
    ValidationError
)
from ..core.validators import validate_email


account_router = APIRouter()


@account_router.post("/create", status_code=201)
async def create(request: UserSchema, response: Response):
    try:
        email = await validate_email(request.email)
    except ValidationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}
    await User.create(
        email=email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name
    )


@account_router.post("/get/id", status_code=200)
async def get_by_id(request: GetUserByIdSchema, response: Response):
    try:
        user = await User.get(id=request.id)
        return user
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}


@account_router.post("/get/email", status_code=200)
async def get_by_email(request: GetUserByEmailSchema, response: Response):
    try:
        user = await User.get(email=request.email)
        return user
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}
