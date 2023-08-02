from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.products import Products
from models.store import Stores
from models.suppliers import Suppliers
from models.users import Users


class Supplies(Base):
    __tablename__ = "supplies"
    id = Column(Integer, autoincrement=True, primary_key=True)
    measure = Column(String(255))
    quantity = Column(Integer)
    price = Column(Numeric)
    date = Column(Date)

    product_id = Column(Integer)
    suppliers_id = Column(Integer)
    store_id = Column(Integer)
    user_id = Column(Integer)

    product = relationship('Products', foreign_keys=[product_id],
                        primaryjoin=lambda: and_(Products.id == Supplies.product_id))
    suppliers = relationship('Suppliers', foreign_keys=[suppliers_id],
                        primaryjoin=lambda: and_(Suppliers.id == Supplies.suppliers_id))
    warehouse = relationship('Stores', foreign_keys=[store_id],
                        primaryjoin=lambda: and_(Stores.id == Supplies.store_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.user_id))


