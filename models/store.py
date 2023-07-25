from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.users import Users


class Stores(Base):
    __tablename__ = "stores"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Stores.user_id))
