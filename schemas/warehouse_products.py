from pydantic import BaseModel


class CreateWarehouse(BaseModel):
    measure: str
    quantity: int
    price: float
    product_id: int
    store_id: int

class UpdateWarehouse(BaseModel):
    id: int
    measure: str
    quantity: int
    price: float
    product_id: int
    store_id: int
