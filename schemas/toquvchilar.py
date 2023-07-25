from pydantic import BaseModel

class CreateToquvchi(BaseModel):
    name: str
    phone_number: int
    # balance: float
    comment: str
    address: str

class UpdateToquvchi(BaseModel):
    id: int
    name: str
    phone_number: int
    # balance: float
    comment: str
    address: str
