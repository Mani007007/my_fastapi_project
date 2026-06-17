from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from database import local_session, base, db_engine
from model import TODOS

base.metadata.create_all(bind=db_engine)

app = FastAPI()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.commit()


@app.post("/todos", response_model=TodoSchema)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TODOS(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


@app.get("/todos", response_model=list[TodoSchema])
def getTodo(db: Session = Depends(get_db)):
    return db.query(TODOS).all()


@app.get("/todos/{id}", response_model=TodoSchema)
def get_single_todo(id: int, db: Session = Depends(get_db)):
    current_todo = db.query(TODOS).filter(TODOS.id == id).first()
    if not current_todo:
        raise HTTPException(status_code=404, detail="Todo Not found ")
    return current_todo


@app.put("/todo/{id}", response_model=TodoSchema)
def update_todo(id: int, updated: TodoCreate, db: Session = Depends(get_db)):
    current_todo = db.query(TODOS).filter(TODOS.id == id).first()
    if not current_todo:
        raise HTTPException(status_code=404, detail="Todo Not found ")

    for k, v in updated.model_dump().items():
        setattr(current_todo, k, v)
    db.commit()
    db.refresh(current_todo)
    return current_todo


@app.delete("/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    current_todo = db.query(TODOS).filter(TODOS.id == id).first()
    if not current_todo:
        raise HTTPException(status_code=404, detail="Todo Not found ")
    db.delete(current_todo)
    db.commit()
    return {"message ": "To Deleted"}
