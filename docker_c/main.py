from fastapi import FastAPI

app = FastAPI()
@app.get('/')
def read_root():
    return {'message': 'hello world'}


@app.get('/items/{item_id}')
def get_item_id(item_id: int, q: str =None):
    return {'item id': item_id, 'query': q}


@app.get('/products')
def list_products(skip: int =0, limit: int =0):
    return {'skip': skip, 'limit': limit}