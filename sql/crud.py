from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(name=user.name, id=user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.ToDo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.ToDoCreate, user_id: str):
    db_todo = models.ToDo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, user_id: schemas.ToDoBase, id: int, update: str):
    todo_update = db.query(models.User).filter_by(user_id=id).first()
    todo_update.todo = update
    db.add(todo_update)
    db.commit()


def delete_todo(db: Session, id: int):
    todo_delete = db.query(models.User).filter_by(id=id).first()
    db.delete(todo_delete)
    db.commit()
