from database import Base
from sqlalchemy import *
from datetime import date

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))
    password_hash = Column(String(255))
    role = Column(String(10))
    status = Column(Boolean)
    token = Column(String(255), default='')
    balance = Column(Numeric)
    # date = Column(date)

