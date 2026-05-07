from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

class BookSchema(BaseModel):
    title: str
    author: str
    price: float
    available: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books")
def create_book(book: BookSchema, db : Session =Depends(get_db)):
    db_book = models.Book(title=book.title,author =book.author, price = book.price, available =book.available)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.get("/books/{books_id}")
def get_books(books_id: int, db: Session = Depends(get_db)):
    
    books = db.query(models.Book).filter(models.Book.id == books_id).first()
    if not books:
        raise HTTPException(status_code = 404,detail ="Item not found")
    return books

@app.delete("/books/{books_id}")
def delete_book(books_id: int, db: Session =Depends(get_db)):
    books = db.query(models.Book).filter(models.Book.id ==books_id).first()
    if not books:
        raise HTTPException(status_code = 404, detail = "Item not found")
    db.delete(books)
    db.commit()
    return {"message": "Item deleted"}

@app.put("/books/{books_id}")
def update_book(books_id:int, book: BookSchema,db:Session = Depends(get_db)):
    books = db.query(models.Book).filter(models.Book.id ==books_id).first()
    if not books:
        raise HTTPException(status_code = 404, detail = "Item not found")
    books.title = book.title
    books.author = book.author
    books.price = book.price
    books.available = book.available
    db.commit()
    db.refresh(books)
    return books

    