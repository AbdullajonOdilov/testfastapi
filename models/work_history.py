import datetime

from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from models.work import Work


class Work_history(Base):
    __tablename__ = "work_histories"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Numeric)
    work_id = Column(Integer)
    status = Column(Boolean)
    date = Column(DateTime, default=datetime.datetime.utcnow())

    work = relationship('Work', foreign_keys=[work_id],
                        primaryjoin=lambda: and_(Work.id == Work_history.work_id))
