from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

#In memory database
items_db = {}
counter = 1

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

@app.get("/")
def home():
    return {"message": "Hello,World"}

@app.post("/items")
def create_item(item: Item):
    global counter
    items_db[counter] = item
    counter += 1
    return {"message": "Item created", "id": counter -1, "item":item}

@app.get("/items")
def get_all_items():
    return items_db

@app.get("/items/{item_id}")
def get_item(item_id:int):
    if item_id not in items_db:
        raise HTTPException(status_code=404,detail="Item not found")
    return items_db[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail ="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}