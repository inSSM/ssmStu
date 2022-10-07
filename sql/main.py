from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .db import SessionLocal, engine
from . import crud, models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="해당하는 아이디가 이미 존재합니다.")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user


@app.post("/users/{user_id}/todos/", response_model=schemas.ToDo)
def create_todo_for_user(
    user_id: str, todo: schemas.ToDoCreate, db: Session = Depends(get_db)
):
    return crud.create_todo(db=db, todo=todo, user_id=user_id)


@app.get("/todos/", response_model=list[schemas.ToDo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@app.get("/todos/", response_model=list[schemas.ToDo])
def read_lists(user_id: str, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, user_id)
    lists: list[schemas.ToDo]
    lists.extend(todos)
    return lists


@app.put("/update/{id}", response_model=schemas.ToDo)
def update_todo(id: int, todo: schemas.ToDoBase, db: Session = Depends(get_db)):
    update: crud.update_todo(db, todo, id)

    return update


@app.delete("/delete/{id}", response_model=schemas.ToDo)
def delete_todo(id: int, db: Session = Depends(get_db)):
    delete = crud.delete_todo(db, id)

    return delete
