import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.work import all_work, create_new_work, update_work_r
from models.work import Work

from schemas.users import UserCreate
from schemas.work import CreateWork, UpdateWork
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

work_router = APIRouter(
    tags=["Work endpoints"]
)


@work_router.get("/works")
def get_work_type(
    search: str = None,
    id: int = 0,
    page: int = 0,
    limit: int = 10,
    db: Session = Depends(database),
    current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Work, db)
    return all_work(search, page, limit, db)


@work_router.post("/create_work")
def create_work(work: CreateWork,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_work(work, db, current_user)
    raise HTTPException(status_code=201, detail="New work created")

@work_router.put("/update_work")
def update_material(work_update: UpdateWork,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    update_work_r(work_update, db, current_user)
    raise HTTPException(status_code=200, detail="The work updated")

