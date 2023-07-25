from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import *



class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))

