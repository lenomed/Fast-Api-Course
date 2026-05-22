from fastapi import FastAPI
from db import engine, sessionLocal
from pydantic import BaseModel
from model import base, Item

app = FastAPI()

base.metadata.create_all(bind=engine)

class ItemSchema(BaseModel):
    name: str
    quantity: int
    price: float

@app.post('/items/')
def create_item(item: ItemSchema):
    db = sessionLocal()
    db_item = Item(name=item.name, price=item.price, quantity=item.quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.get('/items/{item_id}')
def get_item(item_id: int):
    db = sessionLocal()
    db_items = db.querry(Item).filter(item_id == item_id).first()
    db.close()

    if item:
        return item
    else:
        return {'error': 'item not found'}