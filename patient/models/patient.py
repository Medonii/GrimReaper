from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

patients = Table('patients', meta,
Column('id', Integer, primary_key = True),
Column('name', String(255), index = True, nullable = False),
Column('status', String(255), index = True, nullable = True),
Column('address', String(255), index = True, nullable = False),
Column('ambulance', String(255), index = True, nullable = True),
Column('people', Integer, index = True, nullable = False, default = 1),
Column('type', String(255), index = True, nullable = False)
)

meta.create_all(engine)