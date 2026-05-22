from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select

# Model
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False

# Database setup
sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# App
app = FastAPI(lifespan=lifespan)

# Routes
@app.post('/items/')
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)  # fixed: pass the object
        return item

@app.get('/items/', response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items