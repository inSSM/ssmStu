from sqlalchemy import ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(20), primary_key=True, index=True)
    name = Column(String(50), index=True)

    todos = relationship("ToDo", back_populates="user")


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20), ForeignKey("users.id"))
    todo = Column(String(250))

    user = relationship("User", back_populates="todos")
