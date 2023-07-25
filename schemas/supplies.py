from pydantic import BaseModel
from datetime import date


class CreateSupplies(BaseModel):
    measure: str
    quantity: int
    price: float
    date: date
    product_id: int
    suppliers_id: int
    store_id: int



class UpdateSupplies(BaseModel):
    id: int
    measure: str
    quantity: int
    price: float
    date: date
    product_id: int
    suppliers_id: int
    store_id: int

