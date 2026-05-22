from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from contextlib import asynccontextmanager
from sqlalchemy.engine import URL

postgres_uri = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres.poegvvcyuespgvjhryjc",
    password="HNTFOQVWef99XS0h",
    host="aws-1-eu-north-1.pooler.supabase.com",
    port=6543,
    database="postgres"
)
class Item(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 👈 explicitly target public schema
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False


engine = create_engine(postgres_uri, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items
 