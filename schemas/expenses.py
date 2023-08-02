from pydantic import BaseModel, Field


class CreateExpenses(BaseModel):
    # source: constr(regex='^(admin|user|home|weaver)$') for validation
    # I wrote this in functions
    source: str
    source_id: int
    money: float
    comment: str


class UpdateExpenses(BaseModel):
    id: int
    # source: constr(regex='^(admin|user|home|weaver)$') for validation
    # I wrote this in functions
    source: str
    source_id: int = Field(..., ge=1)
    money: float
    comment: str

