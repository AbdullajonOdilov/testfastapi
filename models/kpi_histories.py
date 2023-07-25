from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.kpi import Kpi
from models.proces import Process
from models.users import Users
from models.work import Work

class Kpi_history(Base):
    __tablename__ = "kpi_histories"
    id = Column(Integer, autoincrement=True, primary_key=True)
    kpi_id = Column(Integer)
    process_id = Column(Integer)
    work_id = Column(Integer)
    date = Column(Date)
    user_id = Column(Integer)

    kpi = relationship('Kpi', foreign_keys=[kpi_id],
                       primaryjoin=lambda: and_(Kpi.id == Kpi_history.kpi_id))
    process = relationship('Process', foreign_keys=[process_id],
                           primaryjoin=lambda: and_(Process.id == Kpi_history.process_id))
    work = relationship('Work', foreign_keys=[work_id],
                        primaryjoin=lambda: and_(Work.id == Kpi_history.work_id))
    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Kpi_history.user_id))
