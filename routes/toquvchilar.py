import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.toquvchilar import all_toquvchilar, create_new_toquvchi, update_toquvchi_r
from models.toquvchilar import Toquvchilar
from schemas.toquvchilar import CreateToquvchi, UpdateToquvchi
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

toquvchilar_router = APIRouter(
    tags=["Toquvchilar endpoints"]
)


@toquvchilar_router.get("/toquvchilar")
def get_toquvchilars(
    search: str = None,
    id: int = 0,
    page: int = 0,
    limit: int = 10,
    db: Session = Depends(database),

    current_user: UserCreate = Depends(get_current_active_user)
):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Toquvchilar, db)
    return all_toquvchilar(search, page, limit, db)


@toquvchilar_router.post("/create_toquvchi")
def create_toquvchi(toquvchi: CreateToquvchi,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_toquvchi(toquvchi, db, current_user)
    raise HTTPException(status_code=201, detail="New toquvchi created")

@toquvchilar_router.put("/update_toquvchi")
def update_toquvchi(toquvchi_update: UpdateToquvchi,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    update_toquvchi_r(toquvchi_update, db, current_user)
    raise HTTPException(status_code=200, detail="The toquvchi updated")


