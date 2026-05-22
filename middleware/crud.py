from fastapi import FastAPI
from db import engine, sessionLocal
from pydantic import BaseModel
from model import base, Item

app = FastAPI()

base.metadata.create_all(bind=engine)

class ItemSchema(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int
    category: str 

class responseMod(BaseModel):
    name: str
    price: float
    quantity: int

@app.post('/items/')
def create_item(item: ItemSchema):
    db = sessionLocal()
    db_item = Item(
    name=item.name,
    description=item.description,
    price=item.price,
    quantity=item.quantity,
    category=item.category   # MUST be here
)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)# tells alchemy to go back and update the database with the new data
    db.close()
    print(db)
    return db_item

@app.get('/items/{item_id}', response_model= responseMod)
def get_item(item_id: int):
    db = sessionLocal()
    item = db.query(Item).filter(Item.Id == item_id).first()
    db.close()
    print(item_id)
    if item:
        return item
    else:
        return {'error': 'item not found'}

@app.put('/items/{item_id}')
def update_item(item_id: int,item: ItemSchema):
    db=sessionLocal()
    db_item =db.query(Item).filter(Item.Id == item_id).first()
    if not db_item:
        db.close()
        return {'error': 'item not found'}
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.quantity = item.quantity
    db_item.category = item.category
    db.commit()
    db.refresh(db_item)
    db.close()
    print(item_id)
    return db_item

@app.delete('/item/{item_id}')
def delete_item(item_id):
    db = sessionLocal()
    db_item = db.query(Item).filter(Item.Id == item_id).first()
    if not db_item:
        db.close()
        return {'error': 'Item not found'}
    db.delete(db_item)
    db.commit()
    db.close()
    print(item_id)
    return {'Message': 'item deleted successfully'}
