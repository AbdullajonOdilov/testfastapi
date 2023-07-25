from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.draws import Draws
from models.homes import Homes
from models.proces import Process
from models.tools import Tools
from models.toquvchilar import Toquvchilar
from models.users import Users
from models.work import Work


class Work_history(Base):
    __tablename__ = "work_history"
    id = Column(Integer, autoincrement=True, primary_key=True)
    work_id = Column(Integer)
    # process_id = Column(Integer)
    home_id = Column(Integer)
    tool_id = Column(Integer)
    toquvchi_id = Column(Integer)
    draw_id = Column(Integer)
    status = Column(Boolean)
    date = Column(Date)
    user_id = Column(Integer)

    work = relationship('Work', foreign_keys=[work_id],
                            primaryjoin=lambda: and_(Work.id == Work_history.work_id))

    # process = relationship('Process', foreign_keys=[process_id],
    #                         primaryjoin=lambda: and_(Process.id == Work_history.process_id))
    home = relationship('Homes', foreign_keys=[home_id],
                            primaryjoin=lambda: and_(Homes.id == Work_history.home_id))
    tool = relationship('Tools', foreign_keys=[tool_id],
                            primaryjoin=lambda: and_(Tools.id == Work_history.tool_id))
    toquvchi = relationship('Toquvchilar', foreign_keys=[toquvchi_id],
                            primaryjoin=lambda: and_(Toquvchilar.id == Work_history.toquvchi_id))
    draw = relationship('Draws', foreign_keys=[draw_id],
                            primaryjoin=lambda: and_(Draws.id == Work_history.draw_id))

    user = relationship('Users', foreign_keys=[user_id],
                            primaryjoin=lambda: and_(Users.id == Work_history.user_id))
