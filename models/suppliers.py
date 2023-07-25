from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.users import Users


class Suppliers(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    phone_number = Column(Integer)
    balance = Column(Float)
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Suppliers.user_id))
