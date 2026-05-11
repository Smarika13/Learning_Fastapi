from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from auth import get_current_user
from dependencies import get_db
from typing import Optional

router = APIRouter()

class StudentSchema(BaseModel):
    name: str
    age: int
    grade: str
    passed: bool

@router.post("/students")
def create_student(student: StudentSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user).first()
    db_item = models.Student(
        name=student.name,
        age=student.age,
        grade=student.grade,
        passed=student.passed,
        user_id=user.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/students")
def get_all_students(
    skip: int = 0,
    limit: int = 10,
    grade: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = db.query(models.Student)
    
    if grade:
        query = query.filter(func.upper(models.Student.grade)==func.upper(grade))
    
    if sort_by == "name":
        query = query.order_by(models.Student.name)
    elif sort_by == "age":
        query = query.order_by(models.Student.age)
    
    return query.offset(skip).limit(limit).all()

@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    item = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item

@router.put("/students/{student_id}")
def update_student(student_id: int, student: StudentSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    item = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = student.name
    item.age = student.age
    item.grade = student.grade
    item.passed = student.passed
    db.commit()
    db.refresh(item)
    return item

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    item = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Student deleted"}