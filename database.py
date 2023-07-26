from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base

# 1.) We will create sqlite engine isinstance
engine=create_engine("sqlite:///todooo.db") 

# 2.) Create declarative base meta
Base=declarative_base()

class ToDo(Base):
    __tablename__='todos'
    id=Column(Integer,primary_key=True,)
    task=Column(String(50))

