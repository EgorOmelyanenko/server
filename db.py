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

def retr(sel):
        return "{'id_log':%s,'id_user':%s,'result':%s,'may':%s,'action':%s,'action_time':%s}" % \
               (sel.id_log,sel.id_user,sel.result,sel.may,sel.action,sel.action_time)

session = Session(bind=engine)



def select():
    other_operation('select')
    res = []
    for r in session.query(log).all():
        res.append(retr(r))
    return res

def other_operation(operation):
    id_log=(session.query(func.max(log.id_log)).first()[0])
    if (id_log != None):
        id_log = int(session.query(func.max(log.id_log)).first()[0])+1
    else:
        id_log=1
    new = log(id_log = id_log, id_user = 2,result = 2, may = 2, action = operation, action_time=datetime.datetime.now())
    session.add(new)
    session.commit()





select()

