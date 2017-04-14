from sqlalchemy import orm, MetaData,create_engine, Table, select,Column,Integer,VARCHAR,TIMESTAMP, func
from sqlalchemy.orm import Session,create_session
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
engine = create_engine('postgresql://postgres:1234@localhost:5432/log_db')
meta= MetaData(bind=engine)

class log(Base):
    __tablename__ = 'log'
    id_log = Column(Integer, primary_key=True)
    id_user = Column(Integer)
    result = Column(Integer)
    may = Column (Integer)
    action = Column(VARCHAR)
    action_time = Column(TIMESTAMP)
    def __init__(self,id_log,id_user,result,may,action,action_time):
        self.id_log=id_log
        self.id_user = id_user
        self.result=result
        self.may = may
        self.action=action
        self.action_time=action_time

def retr(row):
        return "{'id_log':%s,'id_user':%s,'result':%s,'may':%s,'action':%s,'action_time':%s}" % \
               (row.id_log,row.id_user,row.result,row.may,row.action,row.action_time)

session = Session(bind=engine)



def select():
    res = []
    for r in session.query(log).all():
        res.append(retr(r))
    return res

def other_operation(operation,error,id_user=None):
    id_log=(session.query(func.max(log.id_log)).first()[0])
    if (id_log != None):
        id_log = int(session.query(func.max(log.id_log)).first()[0])+1
    else:
        id_log=1
    if (id_user!=None):

        operation = operation + '-' + id_user
    print(operation)
    new = log(id_log = id_log, id_user = 2,result = error, may = 2, action = operation, action_time=datetime.datetime.now())
    session.add(new)
    session.commit()







