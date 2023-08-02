from pydantic import BaseModel


class CreateMaterial(BaseModel):
    product_id: int
    name: str


class UpdateMaterial(BaseModel):
    id: int
    name: str


