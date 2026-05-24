from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from db import SessionLocal, Base, engine, Session
from auth_util import decode_access_token,verify_password,hash_password, create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Users

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post('/create_account')
def create_acc(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail= 'username already exists')
    hashed_password = hash_password(user.password)
    new_user = Users(username = user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'username': new_user.username, 'id': new_user.id}

@app.post('/login')
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(Users).filter(Users.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="invalid credentials")

    access_token = create_access_token(data={'sub': db_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }