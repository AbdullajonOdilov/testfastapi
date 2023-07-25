from pydantic import BaseModel
from datetime import date


class CreateWork_history(BaseModel):
    work_id: int
    # process_id: int
    toquvchi_id: int
    draw_id: int
    tool_id: int
    home_id: int
    date: date
    status: bool

