from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import *
from models.material_type import Material_type
from models.users import Users


class Process(Base):
    __tablename__ = "process"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    step = Column(Integer)
    deadline = Column(Integer)
    material_type_id = Column(Integer)
    connection = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Process.user_id))
    material_type = relationship('Material_type', foreign_keys=[material_type_id],
                                 primaryjoin=lambda: and_(Material_type.id == Process.material_type_id))

