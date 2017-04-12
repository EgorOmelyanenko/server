from sqlalchemy import orm, MetaData,create_engine, Table, select,Column,Integer,VARCHAR, func
from sqlalchemy.orm import Session,create_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('postgresql://postgres:1234@localhost:5432/log_db')
meta= MetaData(bind=engine)
#log = Table('log',meta, autoload=True)
class log(Base):
    __tablename__ = 'log'
    id_log = Column(Integer, primary_key=True)
    id_user = Column(Integer)
    result = Column(Integer)
    may = Column (Integer)
    action = Column(VARCHAR)

session = Session(bind=engine)


for i in session.query(log):
    print (i)

def select():
    result = session.query(log)
    other_operation('select')
    return result

def other_operation(operation):
    id_log =int(session.query(func.max(log.id_log)).first()[0])+1
    new = log(id_log = id_log, id_user = 2,result = 2, may = 2, action = operation)
    session.add(new)
    session.commit()
#other_operation('test')
select()
