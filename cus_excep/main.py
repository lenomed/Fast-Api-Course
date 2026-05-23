from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request


app = FastAPI()

@app.get('/divide')
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"result": a / b}

class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"{exc.name} not found."}
    )

items = {'apple': 'A sweet red fruit', 'banana': 'A long yellow fruit'}

@app.get('/items/{item_name}')
def get_item(item_name: str):
        if item_name not in items:
            raise NotFoundException(item_name)
        return {"item": items[item_name], 'desc': items[item_name]}