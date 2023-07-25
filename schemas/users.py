from pydantic import BaseModel
from datetime import date


class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    role: str
    status: bool
    # date: date


class UserUpdate(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
    # date: date
