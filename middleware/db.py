from sqlite3 import connect
from sqlalchemy import create_engine
from sqlalchemy import declarative_base, sessionmaker

DATABASE_URL = 'sqlite:///./items.db'

engine = create_engine(DATABASE_URL, connect_args='check_same_thread': False)

base = declarative_base()
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

