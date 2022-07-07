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
    update,
    delete,
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
            await db.add(user)
            await db.commit()
            await db.refresh(user)

    @classmethod
    async def get(cls, id: Optional[int] = None, email: Optional[str] = None):
        if id is None and email is None:
            async with get_db() as db:
                response = await db.execute(select(cls))
            response = response.mappings().all()
            if not response:
                raise NotFound("No users in database!")
            return response
        else:
            if id is None:
                async with get_db() as db:
                    response = await db.execute(select(cls).filter(cls.email == email))
                response = response.mappings().all()
                if not response:
                    raise NotFound("User not found!")
                return response
            else:
                async with get_db() as db:
                    response = await db.execute(select(cls).filter(cls.id == id))
                response = response.mappings().all()
                if not response:
                    raise NotFound("User not found!")
                return response

    @classmethod
    async def update(
            cls,
            id,
            email: Optional[str],
            password: Optional[str],
            first_name: Optional[str],
            last_name: Optional[str]
    ):
        try:
            await cls.get(id=id)
        except NotFound as e:
            raise NotFound(str(e))
        if email is None and password is None and first_name is None and last_name is None:
            raise ValueError("You can't change it to None value!")
        if email is not None:
            async with get_db() as db:
                await db.execute(update(cls).where(cls.id == id).values(email=email))
        if password is not None:
            async with get_db() as db:
                await db.execute(update(cls).where(cls.id == id).values(password=password))
        if first_name is not None:
            async with get_db() as db:
                await db.execute(update(cls).where(cls.id == id).values(first_name=first_name))
                await db.commit()
        if last_name is not None:
            async with get_db() as db:
                await db.execute(update(cls).where(cls.id == id).values(last_name=last_name))
                await db.commit()

    @classmethod
    async def delete(cls, id):
        try:
            await cls.get(id=id)
        except NotFound:
            raise NotFound("Can't delete user which don't exist!")
        async with get_db() as db:
            await db.execute(delete(cls).where(cls.id == id))
            await db.commit()
