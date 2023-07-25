from pydantic import BaseModel

class CreateStore(BaseModel):
    name: str
    address: str



class UpdateStore(BaseModel):
    id: int
    name: str
    address: str

