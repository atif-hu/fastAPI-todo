from fastapi import FastAPI, status, HTTPException
from database import Base,engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
import schema


# 3.) Create the database
Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return "todooo"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo:schema.ToDo):
    #create a new database session
    session=Session(bind=engine,expire_on_commit=False)

    #create an instance of ToDo database model
    tododb=models.ToDo(task=todo.task)

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
    todo=session.query(models.ToDo).get(id)

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
    todolist=session.query(models.ToDo).all()

    return todolist


@app.put("/todo/{id}")
def update_todo(id: int,task:str):
    # 1.)create session
    session=Session(bind=engine,expire_on_commit=False)

    # 2.) get the task by id
    todo=session.query(models.ToDo).get(id)
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
    todo=session.query(models.ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404,detail=f"todo item with id {id} not found")
    return None






from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://username:password@localhost/dbname"  # Replace with your PostgreSQL connection details
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

app = FastAPI()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)

Base.metadata.create_all(bind=engine)

@app.post("/items/", response_model=Item)
def create_item(name: str, description: str):
    item = Item(name=name, description=description)
    with SessionLocal() as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    with SessionLocal() as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, name: str, description: str):
    with SessionLocal() as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        item.name = name
        item.description = description
        session.commit()
        session.refresh(item)
        return item

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    with SessionLocal() as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return item
