from sqlalchemy import String, Float, Integer, Column
from db import base

class Item(base):
    __tablename__ = 'items'
    Id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(String(200))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default = 0)
    category = Column(String(50), nullable = False)