from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *


from models.material_type import Material_type
from models.proces import Process
from models.users import Users


class Work(Base):
    __tablename__ = "works"
    id = Column(Integer, autoincrement=True, primary_key=True)

    material_type_id = Column(Integer)
    proces_id = Column(Integer)

    user_id = Column(Integer)
    comment = Column(String(255))

    material = relationship('Material_type', foreign_keys=[material_type_id],
                        primaryjoin=lambda: and_(Material_type.id == Work.material_type_id))

    proces = relationship('Process', foreign_keys=[proces_id],
                           primaryjoin=lambda: and_(Process.id == Work.proces_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Work.user_id))





