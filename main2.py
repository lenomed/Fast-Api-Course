#Pydantic Models
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class item(BaseModel):# item data model
    name: str
    price: float 
    is_offer: bool = False
    password: str = 'thou shalt not show thy password'


class itemresponse(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post('/item', response_model=itemresponse)
def creat_item(item: item):
    return item

        