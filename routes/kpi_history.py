import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.kpi_history import all_kpi_histories, create_new_kpihistory
from models.kpi_histories import Kpi_history
from schemas.kpi_histories import CreateKpi_history

from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

kpihistory_router = APIRouter(
    tags=["Kpi History operation"]
)



@kpihistory_router.get("/kpi_histories")
def get_hitories(

        id: int = 0,
        page: int = 0,
        limit: int = 10,
        db: Session = Depends(database),
        current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Kpi_history, db)
    return all_kpi_histories(page, limit, db)


@kpihistory_router.post("/create_kpihistory")
def create_kpihistory(kpihistory: CreateKpi_history,
                      current_user: UserCreate = Depends(get_current_active_user),
                      db: Session = Depends(database)):
    role_verification(current_user)
    create_new_kpihistory(kpihistory, db)
    raise HTTPException(status_code=201, detail="New kpi_history created")






