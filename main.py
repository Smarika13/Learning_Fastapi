from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

class ItemSchema(BaseModel):
    name: str
    price: float
    in_stock: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items")
def create_item(item: ItemSchema, db : Session =Depends(get_db)):
    db_item = models.Item(name=item.name, price = item.price, in_stock =item.in_stock)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.get("/items/{item_id}")
def get_items(item_id: int, db: Session = Depends(get_db)):
    
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code = 404,detail ="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session =Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id ==item_id).first()
    if not item:
        raise HTTPException(status_code = 404, detail = "Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}
    