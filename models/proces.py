from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import *

from models.homes import Homes
from models.material_type import Material_type
from models.products import Products
from models.tools import Tools
from models.toquvchilar import Toquvchilar
from models.users import Users


class Process(Base):
    __tablename__ = "process"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    step = Column(Integer)
    deadline = Column(Integer)
    product_id = Column(Integer)
    material_type_id = Column(Integer)
    connection = Column(String(255))
    connection_id = Column(Integer)

    user_id = Column(Integer)

    product = relationship('Products', foreign_keys=[product_id],
                           primaryjoin=lambda: and_(Products.id == Process.product_id))
    material_type = relationship('Material_type', foreign_keys=[material_type_id],
                                 primaryjoin=lambda: and_(Material_type.id == Process.material_type_id))
    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Process.user_id))
    c_user = relationship('Users', foreign_keys=[connection_id],
                          primaryjoin=lambda: and_(Users.id == Process.connection_id,
                          Process.connection == "admin", Process.connection == 'user'))
    c_toquvchi = relationship('Toquvchilar', foreign_keys=[connection_id],
                              primaryjoin=lambda: and_(Toquvchilar.id == Process.connection_id,
                                                     Process.connection == 'toquvchi'))
    c_home = relationship('Homes', foreign_keys=[connection_id],
                          primaryjoin=lambda: and_(Homes.id == Process.connection_id,
                                                 Process.connection == 'home'))
    c_tool = relationship('Tools', foreign_keys=[connection_id],
                          primaryjoin=lambda: and_(Tools.id == Process.connection_id,
                                                 Process.connection == 'tool'))




