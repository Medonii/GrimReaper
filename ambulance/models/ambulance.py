from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

ambulances = Table('ambulances', meta,
Column('id', Integer, primary_key = True),
Column('tag', String(255), index = True, nullable = False),
Column('type', String(255), index = True, nullable = False),
Column('status', String(255), index = True, nullable = True),
Column('position', String(255), index = True, nullable = False)
)

meta.create_all(engine)