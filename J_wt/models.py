from db import Base
from sqlalchemy import Column, String, Integer

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index=True)
    username = Column(String, index=True)
    #email= Column(String, unique=True)
    hashed_password = Column(String) 