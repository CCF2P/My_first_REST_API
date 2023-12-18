from fastapi.responses import JSONResponse
from fastapi import APIRouter

from DataBase.database import *
from Models.model import UserCreate


# create tables
Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/todo")
def get_todo_user_id():
    db = SessionLocal()
    res = db.query(ToDo).all()
    db.close()
    return res


@router.post("/user")
def add_user(data: UserCreate):
    db = SessionLocal()

    user = ToDo(name=data.name, task=data.task)
    db.add(user)
    db.commit()

    db.close()
    return data


@router.put("/todo/{user_id}")
def update_todo_user_id(user_id: int, data: UserCreate):
    db = SessionLocal()

    user = db.query(ToDo).filter(ToDo.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})
    
    user.task = data.task
    db.commit()

    db.close()
    return {"message": "change is complete"}


@router.delete("/todo/{user_id}")
def delete_todo_user_id(user_id: int):
    db = SessionLocal()

    user = db.query(ToDo).filter(ToDo.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})
    
    db.delete(user)
    db.commit()

    db.close()
    return {"message": "the user has been successfully deleted"}
