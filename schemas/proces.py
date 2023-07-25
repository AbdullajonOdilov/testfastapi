from pydantic import BaseModel


class CreateProcess(BaseModel):
    product_id: int
    material_type_id: int
    connection_id: int
    connection: str
    name: str
    step: int
    deadline: int


class UpdateProcess(BaseModel):
    id: int
    product_id: int
    material_type_id: int
    connection_id: int
    connection: str
    name: str
    step: int
    deadline: int


