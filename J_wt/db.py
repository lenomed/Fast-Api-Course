from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker


DATABASE_URL = 'sqlite:///./users.db'

engine = create_engine(DATABASE_URL, connect_args={'check same thread': False})

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

Base = declarative_base()
