from pydantic import BaseModel


class CreateKpi(BaseModel):
    proces_id: int
    price: float
    user_id: int


class UpdateKpi(BaseModel):
    id: int
    proces_id: int
    price: float
    user_id: int