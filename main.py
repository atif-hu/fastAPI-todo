from fastapi import FastAPI, status
from database import Base,engine
from pydantic import BaseModel

#4.) Create todo request base model
class ToDoRequest(BaseModel):
    task:str

# 3.) Create the database
Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return "todooo"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo:ToDoRequest):
    return "create todo item"

@app.get("/todo/{id}")
def read_todo(id: int):
    return "read todo item with id {id}"

@app.put("/todo/{id}")
def update_todo(id: int):
    return "update todo item with id {id}"

@app.delete("/todo/{id}")
def delete_todo(id: int):
    return "delete todo item with id {id}"

@app.get("/todo")
def read_todo_list():
    return "read todo list"
