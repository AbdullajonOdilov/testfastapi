import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.kpi import all_kpi, create_new_kpi, update_kpi_r
from models.kpi import Kpi
from schemas.kpi import CreateKpi, UpdateKpi
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

kpi_router = APIRouter(
    tags=["Kpi endpoints"]
)

@kpi_router.get("/get_kpis")
def get_kpis(id: int = 0, page: int = 0, limit: int = 10,
             db: Session = Depends(database),
             current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)

    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Kpi, db)
    return all_kpi(page, limit, db)



@kpi_router.post("/create_kpi")
def create_kpi(new_kpi: CreateKpi,
               db: Session = Depends(database),
               current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    create_new_kpi(new_kpi, db)
    raise HTTPException(status_code=201, detail="New kpi created")


@kpi_router.put("/update_kpi")
def update_kpi(update_kpi: UpdateKpi, db: Session = Depends(database),
               current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    update_kpi_r(update_kpi, db)
    raise HTTPException(status_code=200, detail="The kpi updated")

