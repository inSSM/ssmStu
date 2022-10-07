from pydantic import BaseModel


class ToDoBase(BaseModel):
    todo: str


class ToDoCreate(ToDoBase):
    pass


class ToDo(ToDoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    id: str


class User(UserBase):
    id: str
    todos: list[ToDo] = []

    class Config:
        orm_mode = True
