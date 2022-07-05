from ..account.models import User
from .exceptions import (
    NotFound,
    ValidationError,
)


async def validate_email(email):
    try:
        await User.get(email=email)
    except NotFound:
        return email
    raise ValidationError("This email is already used!")
