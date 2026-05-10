from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from auth import hash_password,verify_password,create_access_token
from dependencies import get_db

router = APIRouter()

class UserRegisterSchema(BaseModel):
    name:str
    email:str
    password:str

class UserLoginSchema(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse)
def register(user:UserRegisterSchema,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email,hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user:UserLoginSchema, db:Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if not db_user:
        raise HTTPException(staus_code = 404, detail= "User not found")
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code = 401,detail ="Incorrect password")
    token = create_access_token(data={"sub":db_user.email})
    return  {"access_token":token, "token_type":"bearer"}