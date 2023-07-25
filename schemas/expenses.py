from pydantic import BaseModel
from datetime import date


class CreateExpenses(BaseModel):
    source: str
    source_id: int
    money: float
    date: date
    comment: str


class UpdateExpenses(BaseModel):
    id: int
    source: str
    source_id: int
    money: float
    date: date
    comment: str

