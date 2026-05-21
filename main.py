from fastapi import FastAPI

app= FastAPI()

@app.get('/')
def root():
    return {'hello': 'world'}

store=[]
@app.post('/items')
def creat_item(item: str):
    store.append(item)
    return store