from fastapi import APIRouter, Response, status
from .schema import (
    UserSchema,
    GetUserByIdAndDeleteUserSchema,
    GetUserByEmailSchema,
    UpdateUserSchema,
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


@account_router.post("/get/all", status_code=200)
async def get_all(response: Response):
    try:
        users = await User.get()
        return users
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}


@account_router.post("/get/id", status_code=200)
async def get_by_id(request: GetUserByIdAndDeleteUserSchema, response: Response):
    try:
        user = await User.get(id=request.id)
        return user[0]
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}


@account_router.post("/get/email", status_code=200)
async def get_by_email(request: GetUserByEmailSchema, response: Response):
    try:
        user = await User.get(email=request.email)
        return user[0]
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}


@account_router.put("/update", status_code=200)
async def update(request: UpdateUserSchema, response: Response):
    try:
        await User.update(
            id=request.id,
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name
        )
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}


@account_router.delete("/delete", status_code=200)
async def delete(request: GetUserByIdAndDeleteUserSchema, response: Response):
    try:
        await User.delete(request.id)
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}
