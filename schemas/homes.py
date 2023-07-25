from pydantic import BaseModel

class CreateHome(BaseModel):
    address: str
    phone_number: int
    # balance: int


class UpdateHome(BaseModel):
    id: int
    address: str
    phone_number: int
    # balance: int

