from pydantic import BaseModel
from datetime import date

class CreateKpi_history(BaseModel):
    kpi_id: int
    process_id: int
    work_id: int
    date: date
    user_id: int

    
class UpdateKpi_history(BaseModel):
    id: int
    kpi_id: int
    process_id: int
    work_id: int
    date: date
    user_id: int
