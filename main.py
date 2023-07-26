from fastapi import FastAPI, status, HTTPException
from database import Base,engine,ToDo
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
    #create a new database session
    session=Session(bind=engine,expire_on_commit=False)

    #create an instance of ToDo database model
    tododb=ToDo(task=todo.task)

    #add it to the db and commit id
    session.add(tododb)
    session.commit()

    #grab the id given to the object from the db
    id=tododb.id

    #close the session
    session.close()

    return f"Successfully created todo item with id: {id}"

@app.get("/todo/{id}")
def read_todo(id: int):
    
    #1.) To read a data with id, first create a db session
    session=Session(bind=engine,expire_on_commit=False)

    #2.) get the todo item from the given id
    todo=session.query(ToDo).get(id)

    #3.) close the session
    session.close()
    if not todo:
        raise HTTPException(status_code=404,detail=f"todo item with id {id} not found")
    
    return todo    


@app.get("/todo")
def read_todo_list():
    #1.) create a db session
    session=Session(bind=engine,expire_on_commit=False)

    #2.) fetch todo list 
    todolist=session.query(ToDo).all()

    return todolist


@app.put("/todo/{id}")
def update_todo(id: int,task:str):
    # 1.)create session
    session=Session(bind=engine,expire_on_commit=False)

    # 2.) get the task by id
    todo=session.query(ToDo).get(id)
    if todo:
        todo.task = task
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo
@app.delete("/todo/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    session=Session(bind=engine,expire_on_commit=False)
    todo=session.query(ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404,detail=f"todo item with id {id} not found")
    return None


