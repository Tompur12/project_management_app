from ..database.db_conf import (
    Base,
    get_db,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
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
        with get_db() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
