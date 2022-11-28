from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table('users', meta,
Column('id', Integer, primary_key = True),
Column('nickname', String(255), index = True, nullable = False),
Column('password', String(255), nullable = False)
)

meta.create_all(engine)