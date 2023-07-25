from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.homes import Homes
from models.tools import Tools
from models.toquvchilar import Toquvchilar
from models.users import Users


class Expenses(Base):
    __tablename__ = "Expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255))
    source_id = Column(Integer)
    money = Column(Float)
    date = Column(Date)
    comment = Column(String(255))
    user_id = Column(Integer)

    source_user = relationship('Users', foreign_keys=[source_id],
                               primaryjoin=lambda: and_(Users.id == Expenses.source_id, Expenses.source == "user"))

    source_toquvchi = relationship('Toquvchilar', foreign_keys=[source_id],
                                   primaryjoin=lambda: and_(Toquvchilar.id == Expenses.source_id,
                                   Expenses.source == "toquvchi"))
    source_home = relationship('Homes', foreign_keys=[source_id],
                               primaryjoin=lambda: and_(Homes.id == Expenses.source_id,
                                                        Expenses.source == "home"))

    source_user = relationship('Users', foreign_keys=[source_id],
                               primaryjoin=lambda: and_(Users.id == Expenses.source_id,
                                                        Expenses.source == "user", Expenses.source == "admin"))

    user = relationship('Users', foreign_keys=[user_id],
                          primaryjoin=lambda: and_(Users.id == Expenses.user_id))


