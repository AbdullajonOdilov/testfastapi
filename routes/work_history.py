import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.work_history import all_histories, create_new_work_history
from models.work_history import Work_history
from schemas.users import UserCreate
from schemas.work_histories import CreateWork_history
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

work_history_router = APIRouter(
    tags=["Work History endpoints"]
)


@work_history_router.get("/work_histories")
def get_history(id: int = 0,
                page: int = 0,
                limit: int = 10,
                db: Session = Depends(database),
                current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Work_history, db)
    return all_histories(page, limit, db)

@work_history_router.post("/create_workhistory")
def create_workhistory(work_history: CreateWork_history,
                       current_user: UserCreate = Depends(get_current_active_user),
                       db: Session = Depends(database)):
    role_verification(current_user)
    create_new_work_history(work_history, current_user, db)
    raise HTTPException(status_code=201, detail="New work_history created")
