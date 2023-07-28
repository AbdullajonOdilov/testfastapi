from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.draws import Draws
from models.homes import Homes

from models.tools import Tools
from models.toquvchilar import Weavers
from models.users import Users
from models.work import Work


class Work_history(Base):
    __tablename__ = "work_histories"
    id = Column(Integer, autoincrement=True, primary_key=True)
    money = Column(Float)
    work_id = Column(Integer)
    home_id = Column(Integer)
    tool_id = Column(Integer)
    weaver_id = Column(Integer)
    draw_id = Column(Integer)
    status = Column(Boolean)
    date = Column(Date)
    connection_user_id = Column(Integer)
    user_id = Column(Integer)

    work = relationship('Work', foreign_keys=[work_id],
                        primaryjoin=lambda: and_(Work.id == Work_history.work_id))

    home = relationship('Homes', foreign_keys=[home_id],
                         primaryjoin=lambda: and_(Homes.id == Work_history.home_id))
    tool = relationship('Tools', foreign_keys=[tool_id],
                          primaryjoin=lambda: and_(Tools.id == Work_history.tool_id))
    weaver = relationship('Weavers', foreign_keys=[weaver_id],
                          primaryjoin=lambda: and_(Weavers.id == Work_history.weaver_id))
    draw = relationship('Draws', foreign_keys=[draw_id],
                         primaryjoin=lambda: and_(Draws.id == Work_history.draw_id))

    connection_user = relationship('Users', foreign_keys=[connection_user_id],
                                   primaryjoin=lambda: and_(Users.id == Work_history.connection_user_id))
    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Work_history.user_id))
