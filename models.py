from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index =True)
    name = Column(String)
    email = Column(String, unique = True)
    hashed_password = Column(String)
    students=relationship("Student",back_populates="owner")

class Student(Base):
    __tablename__="student"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)
    passed = Column(Boolean)
    user_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User",back_populates="students")



