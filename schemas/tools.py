from pydantic import BaseModel


class CreateTools(BaseModel):
    name: str
    status: bool


class UpdateTools(BaseModel):
    id: int
    name: str
    status: bool
