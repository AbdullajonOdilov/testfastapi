import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.homes import all_homes, create_new_home, update_home_r
from models.homes import Homes
from schemas.homes import CreateHome, UpdateHome
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

homes_router = APIRouter(
    tags=["Homes endpoints"]
)


@homes_router.get("/homes")
def get_homes(
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
        return the_one(id, Homes, db)
    return all_homes(search, page, limit, db)


@homes_router.post("/create_home")
def create_home(home: CreateHome,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_home(home, db, current_user)
    raise HTTPException(status_code=201, detail="New home created")

@homes_router.put("/update_home")
def update_home(home_update: UpdateHome,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    update_home_r(home_update, db, current_user)
    raise HTTPException(status_code=200, detail="The home updated")


