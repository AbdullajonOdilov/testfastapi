from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *

from models.products import Products
from models.store import Stores


class Warehouse_products(Base):
    __tablename__ = "warehouse_products"
    id = Column(Integer, autoincrement=True, primary_key=True)
    measure = Column(String(255))
    quantity = Column(Integer)
    price = Column(Numeric)
    product_id = Column(Integer)
    store_id = Column(Integer)
    product = relationship('Products', foreign_keys=[product_id],
                           primaryjoin=lambda: and_(Products.id == Warehouse_products.product_id))

    store = relationship('Stores', foreign_keys=[store_id],
                           primaryjoin=lambda: and_(Stores.id == Warehouse_products.store_id))


