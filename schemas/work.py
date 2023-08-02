from pydantic import BaseModel


class CreateWork(BaseModel):
    material_type_id: int
    connection_id: int
    comment: str


class UpdateWork(BaseModel):
    id: int
    material_type_id: int
    connection_id: int
    comment: str


