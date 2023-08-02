from pydantic import BaseModel, confloat


class CreateKpi(BaseModel):
    proces_id: int
    price: confloat(gt=0.0)


class UpdateKpi(BaseModel):
    id: int
    proces_id: int
    price: confloat(gt=0.0)
