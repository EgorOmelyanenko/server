from aiopg.sa import *

def select():
    engine = create_engine('postgresql://postgres:1234@localhost:5432/log_db')
    result = engine.execute("select * from log;")
    return result

