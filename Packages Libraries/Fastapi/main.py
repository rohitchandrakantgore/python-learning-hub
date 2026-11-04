from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.get("/")
def hello_world():
    return {"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id:int, item_name:str|None=None):
    return {"item_id":item_id, "item_name":item_name}

@app.put("/items/{item_id}")
def update_item(item_id:int, item: Item): 
    return {"item_id":item_id, "item": item}