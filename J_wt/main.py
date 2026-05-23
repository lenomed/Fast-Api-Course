from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    item: str

item_list = []

@app.post('/items')
def create_item(item: Item):
    items = item_list.append(item)
    return {'message': 'item added successfully'}

@app.get('/items{item_names}')
def get_item(item_id: int):
    if not item_list[item_id]:
        return {'message': f'item {item_list[item_id]} not found'}
    return {f'you searched {item_list[item_id]} and it exists'}