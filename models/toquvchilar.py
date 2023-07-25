from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import *

from models.users import Users


class Toquvchilar(Base):
    __tablename__ = "toquvchilar"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    phone_number = Column(Integer)
    balance = Column(Float)
    comment = Column(String(255))
    address = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Toquvchilar.user_id))


