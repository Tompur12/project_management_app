from ..database.db_conf import (
    Base,
    get_db,
)
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    select,
)
from ..core.exceptions import (
    MissingArguments,
    NotFound,
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    @classmethod
    async def create(cls, email, password, first_name, last_name):
        user = cls(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        async with get_db() as db:
            db.add(user)
            await db.commit()
            await db.refresh(user)

    @classmethod
    async def get(cls, id: Optional[int] = None, email: Optional[str] = None):
        if id is None and email is None:
            raise MissingArguments("Missing arguments!")
        else:
            if id is None:
                async with get_db() as db:
                    response = await db.execute(select(cls).filter(cls.email == email))
                response = response.mappings().all()
                if not response:
                    raise NotFound("User not found!")
                return response[0]
            else:
                async with get_db() as db:
                    response = await db.execute(select(cls).filter(cls.id == id))
                response = response.mappings().all()
                if not response:
                    raise NotFound("User not found!")
                return response[0]
