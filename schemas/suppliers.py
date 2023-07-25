from pydantic import BaseModel

class CreateSuppliers(BaseModel):
    name: str
    address: str
    phone_number: int


class UpdateSuppliers(BaseModel):
    id: int
    name: str
    address: str
    phone_number: int

