from warnings import deprecated
from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from db import database, metadata, engine
from models import users
from schemas import CreateUser, UserLogin

    
app = FastAPI()

metadata.create_all(engine)

pwd_context =CryptContext(schemes=['bcrypt'], deprecated='auto')

@app.on_event('startup')
async def startUp():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

    #creat user endpoint
@app.post('/register')
async def register(user: CreateUser):
    querry = users.select().where(users.c.username == user.username)
    existing_user = await database.fetch_one(querry)
    if existing_user:
        raise HTTPException(status_code=400, detail='username already exists')
    hashed_password =pwd_context.hash(user.password)
    querry = users.insert().values(username = user.username, password= hashed_password)
    await database.execute(querry)
    return {'message': 'User Registered Successfully'}

#login endpoint
@app.post('/login')
async def login(user: UserLogin):
    querry = users.select().where(users.c.username == user.username)
    existing_user = await database.fetch_one(querry)
    if not existing_user:
        raise HTTPException(status_code=400, detail='Invalid username or password')
    if not pwd_context.verify(user.password, existing_user['password']):
        raise HTTPException(status_code=400, detail='Invalid username or password')
    return {'message': 'login successful'}
