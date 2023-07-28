from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import *

from models.users import Users


class Weavers(Base):
    __tablename__ = "weavers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    phone_number = Column(Integer)
    balance = Column(Float)
    comment = Column(String(255))
    address = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Weavers.user_id))


