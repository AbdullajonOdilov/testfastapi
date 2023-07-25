from database import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import *

from models.proces import Process
from models.users import Users


class Kpi(Base):
    __tablename__ = "kpi"
    id = Column(Integer, autoincrement=True, primary_key=True)
    proces_id = Column(Integer)
    price = Column(Float)
    user_id = Column(Integer)

    proces = relationship('Process', foreign_keys=[proces_id],
                           primaryjoin=lambda: and_(Process.id == Kpi.proces_id), backref=backref("proces"))

    user = relationship('Users', foreign_keys=[user_id],
                          primaryjoin=lambda: and_(Users.id == Kpi.user_id))