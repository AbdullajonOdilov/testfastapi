from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.users import Users


class Tools(Base):
    __tablename__ = "tools"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    status = Column(Boolean)
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Tools.user_id))


