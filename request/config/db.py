from sqlalchemy import create_engine, MetaData

engine = create_engine('mysql+pymysql://root:grimreaperpassword@host.docker.internal:3306/GrimReaper')
meta = MetaData()
conn = engine.connect()