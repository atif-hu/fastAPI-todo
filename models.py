from sqlalchemy import create_engine,Column,Integer,String,Boolean
from database import Base

class ToDo(Base):
    __tablename__='todos'
    id=Column(Integer,primary_key=True)
    task=Column(String(50))




