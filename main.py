from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

class StudentSchema(BaseModel):
    name:str
    age: int
    grade: str
    passed: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students")
def create_student(student:StudentSchema, db:Session=Depends(get_db)):
    db_item = models.Student(name=student.name,age=student.age,grade=student.grade,passed= student.passed)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/students")
def get_all_students(db:Session=Depends(get_db)):
    return db.query(models.Student).all()

@app.get("/students/{student_id}")
def get_student(student_id:int, db:Session=Depends(get_db)):
    item = db.query(models.Student).filter(models.Student.id ==student_id).first()
    if not item:
        raise HTTPException(status_code = 404, detail="Not found")
    return item
    
@app.put("/students/{student_id}")
def update_student(student_id:int,student:StudentSchema ,db:Session=Depends(get_db)):
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
def delete_student(student_id:int, db:Session=Depends(get_db)):
    item = db.query(models.Student).filter(models.Student.id==student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail ="Item not found")
    db.delete(item)
    db.commit()
    return {"message":"Student deleted"}

    







