from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Shippable API", version="1.0.0")

class Item(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)

db: dict[int, Item] = {}
counter: int = 1

@app.get("/items", response_model=dict[int, Item])
def get_items():
    return db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db[item_id]

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    global counter
    db[counter] = item
    item_id = counter
    counter += 1
    return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del db[item_id]
    return None
