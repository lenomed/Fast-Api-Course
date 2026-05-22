from fastapi import FastAPI

app= FastAPI()

@app.get('/')
def root():
    return {'hello': 'world'}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id,"querry": q}

@app.get('/products/')
def list_products(skip: int=0, limit: int = 0):
    return {'skip': skip, 'limit': limit}

store=[]
@app.post('/items')
def creat_item(item: str):
    store.append(item)
    return store