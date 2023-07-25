from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str


class UpdateProduct(BaseModel):
    id: int
    name: str