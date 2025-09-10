

from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import re 

app = FastAPI()



class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    tags: List[str] = []

DB: Dict[int, Item] = {}

_id = 0


# data = { "id" : "12", "text" :"dfdhfroeroeuwueow"}    


# print(Receipt(**data))


@app.get("/ping")
async def ping():
    return {"status": "ok"}

# greeting  Function
@app.get("/greet")
async def greet(name: str = Query("friend", min_length=2, max_length=30)):
    return {"message": f"Hello, {name}!"}

#  add with typed query params
@app.get("/math/add")
async def add(a: float, b: float):
    return {"a": a, "b": b, "sum": a + b}

#Simple 
@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/{name]")
async def getpathvariable(name):
    return {"name" : name}

@app.get("/try")
async def tryOutQueryParameters(name :str , age :int):
    return{"name" : name, "age" : age }



@app.get("/try/{name}")
async def tryOutQueryParameters(name :str , age :int):
    return{"name" : name, "age" : age }


# Get item w
@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., ge=1)):
    item = DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": item}

# Create item 
@app.post("/items", status_code=201)
async def create_item(item: Item):
    global _id
    _id += 1
    DB[_id] = item
    return {"id": _id, "item": item}

#  Delete item
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int = Path(..., ge=1)):
    if DB.pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message" : delete_item}

# @app.get("/try/{name}")
# async def tryOutQueryParameters(name :str= Path(..., min_length =5 , max_length =20) , age :int):
#     return{"name" : name, "age" : age }


















# Item amount and Subtotal or total extraction

class Receipt(BaseModel):
   
    text : str




@app.post("/extract/data")
async def extractReceipt(rp : Receipt):

    item_amount = re.findall(r'(?i)^Items\s*(?:Amount)?\s*[:-]?\s*[$]?\s*\s*(\d+(?:,\d{3})*(?:\.\d{2,}))' , rp.text, flags=re.MULTILINE) 

    print("item amount",item_amount)

    total = re.findall(r'(?i)^(?:Sub)?\s*(?:Total)?\s*[:-]?\s*[$]?\s*\s*(\d+(?:,\d{3})*(?:\.\d{2,}))', rp.text , flags=re.MULTILINE)       

    print("total amount", total)

    return {
        "item_amounts": item_amount,
        "subtotal": total
    }



