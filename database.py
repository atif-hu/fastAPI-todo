from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# 1.) We will create sqlite engine isinstance
engine=create_engine("sqlite:///todooo.db") 

# 2.) Create declarative base meta
Base=declarative_base()
