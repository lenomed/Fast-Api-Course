#User Auth

from sqlalchemy import Table, Integer, String ,Column
from db import metadata # pyright: ignore[reportMissingImports]

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), nullable=False, index=True),
    Column('password', String)
    )

