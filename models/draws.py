from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *


from models.users import Users


class Draws(Base):
    __tablename__ = "draws"
    id = Column(Integer, autoincrement=True, primary_key=True)

    name = Column(String(255))
    status = Column(Boolean)
    file = Column(Text)
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Draws.user_id))



