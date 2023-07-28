from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.products import Products
from models.users import Users


class Material_type(Base):
    __tablename__ = "material_types"
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(Integer)
    name = Column(String(255))
    user_id = Column(Integer)

    product = relationship('Products', foreign_keys=[product_id],
                        primaryjoin=lambda: and_(Products.id == Material_type.product_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Material_type.user_id))

