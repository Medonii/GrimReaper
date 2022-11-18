from sqlalchemy import create_engine, MetaData

engine = create_engine('mysql+pymysql://root:userpassword@localhost:3306/user')
meta = MetaData()
conn = engine.connect()