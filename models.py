from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Student(Base):
    __tablename__="student"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)
    passed = Column(Boolean)



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index =True)
    name = Column(String)
    email = Column(String, unique = True)
    hashed_password = Column(String)