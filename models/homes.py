from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import *

from models.users import Users


class Homes(Base):
    __tablename__ = "homes"
    id = Column(Integer, autoincrement=True, primary_key=True)
    phone_number = Column(Integer)
    balance = Column(Float)
    address = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                          primaryjoin=lambda: and_(Users.id == Homes.user_id))