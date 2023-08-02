from pydantic import BaseModel


class CreateHome(BaseModel):
    name: str
    address: str
    phone_number: int
    # phone_number: constr(min_length=9, max_length=9)


class UpdateHome(BaseModel):
    id: int
    name: str
    address: str
    phone_number: int
    # phone_number: constr(min_length=9, max_length=9)


