from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

requests = Table('requests', meta,
Column('id', Integer, primary_key = True),
Column('name', String(255), index = True, nullable = False),
Column('status', String(255), index = True, nullable = False),
Column('address', String(255), index = True, nullable = False)
)

meta.create_all(engine)