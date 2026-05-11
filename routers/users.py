from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import models
from auth import hash_password,verify_password,create_access_token,create_refresh_token,SECRET_KEY,ALGORITHM
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

class RefreshTokenSchema(BaseModel):
    refresh_token: str

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
        raise HTTPException(status_code = 404, detail= "User not found")
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code = 401,detail ="Incorrect password")
    token = create_access_token(data={"sub":db_user.email})
    refresh_token = create_refresh_token(data={"sub":db_user.email})
    

    return  {"access_token":token,"refresh_token":refresh_token, "token_type":"bearer"}

@router.post("/refresh")
def refresh_token(data: RefreshTokenSchema, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    new_token = create_access_token(data={"sub": email})
    return {"access_token": new_token, "token_type": "bearer"}