from ..database.db_conf import Base
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
