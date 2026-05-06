from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def home():
    return {"message":"Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is my first FastAPI app"}

@app.get("/items/{item_id}")
def get_item(item_id:int):
    return {"item_id": item_id, "name":f"Item number {item_id}"}

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

@app.post("/items")
def create_item(item: Item):
    return {"message": "Item created", "item": item}
