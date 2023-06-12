from sqlalchemy import create_engine, MetaData



engine = create_engine('mysql+pymysql://root:grimreaperpassword@10.110.107.76/GrimReaper')
meta = MetaData()
conn = engine.connect()