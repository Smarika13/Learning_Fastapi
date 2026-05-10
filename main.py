from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from auth import hash_password,verify_password,create_access_token,get_current_user

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

class StudentSchema(BaseModel):
    name:str
    age: int
    grade: str
    passed: bool

class UserRegisterSchema(BaseModel):
    name: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@app.post("/register",response_model = UserResponse)
def register(user: UserRegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/students")
def create_student(student:StudentSchema, db:Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user).first()
    db_item = models.Student(
        name=student.name,
        age=student.age,
        grade=student.grade,
        passed= student.passed,
        user_id = user.id
        )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/students")
def get_all_students(skip:int=0,limit: int =10,db:Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    return db.query(models.Student).offset(skip).limit(limit).all()

@app.get("/students/{student_id}")
def get_student(student_id:int, db:Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    item = db.query(models.Student).filter(models.Student.id ==student_id).first()
    if not item:
        raise HTTPException(status_code = 404, detail="Not found")
    return item
    
@app.put("/students/{student_id}")
def update_student(student_id:int,student:StudentSchema ,db:Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    item = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code = 404,detail = "Item not found")
    item.name =student.name
    item.age = student.age
    item.grade =student.grade
    item.passed=student.passed
    db.commit()
    db.refresh(item)
    return item

@app.delete("/students/{student_id}")
def delete_student(student_id:int, db:Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    item = db.query(models.Student).filter(models.Student.id==student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail ="Item not found")
    db.delete(item)
    db.commit()
    return {"message":"Student deleted"}

    







