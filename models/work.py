from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.homes import Homes
from models.material_type import Material_type
from models.proces import Process
from models.tools import Tools
from models.toquvchilar import Weavers
from models.users import Users


class Work(Base):
    __tablename__ = "works"
    id = Column(Integer, autoincrement=True, primary_key=True)

    material_type_id = Column(Integer)
    connection_id = Column(Integer)
    process_id = Column(Integer)
    user_id = Column(Integer)
    comment = Column(String(255))

    material_type = relationship('Material_type', foreign_keys=[material_type_id],
                            primaryjoin=lambda: and_(Material_type.id == Work.material_type_id))

    connection_user = relationship('Users', foreign_keys=[connection_id],
                                    primaryjoin=lambda: and_(Users.id == Work.connection_id))
    connection_home = relationship('Homes', foreign_keys=[connection_id],
                                     primaryjoin=lambda: and_(Homes.id == Work.connection_id))
    connection_tool = relationship('Tools', foreign_keys=[connection_id],
                                     primaryjoin=lambda: and_(Tools.id == Work.connection_id))
    connection_weaver = relationship('Weavers', foreign_keys=[connection_id],
                                     primaryjoin=lambda: and_(Weavers.id == Work.connection_id))
    process = relationship("Process", foreign_keys=[process_id],
                           primaryjoin=lambda: and_(Process.id == Work.process_id))
    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Work.user_id))





