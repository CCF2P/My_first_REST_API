from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, Body, FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class UserCreate(BaseModel):
    #id: int
    name: str
    task: str


# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    db = SessionLocal()
    res = db.query(ToDo).all()
    db.close()
    return res


@app.post("/user")
def add_user(data: UserCreate):
    db = SessionLocal()

    user = ToDo(name=data.name, task=data.task)
    db.add(user)
    db.commit()

    db.close()
    return data


@app.put("/todo/update/{user_id}")
def update_todo_user_id(user_id: int, data: UserCreate):
    db = SessionLocal()

    user = db.query(ToDo).filter(ToDo.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})
    
    user.task = data.task
    db.commit()

    db.close()
    return {"message": "change is complete"}


@app.get("/todo/{user_id}")
def get_todo_user_id(user_id: int):
    db = SessionLocal()

    user = db.query(ToDo).filter(ToDo.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})
    
    db.close()
    return user


@app.delete("/todo/delete/{user_id}")
def delete_todo_user_id(user_id: int):
    db = SessionLocal()

    user = db.query(ToDo).filter(ToDo.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})
    
    db.delete(user)
    db.commit()

    db.close()
    return {"message": "the user has been successfully deleted"}
