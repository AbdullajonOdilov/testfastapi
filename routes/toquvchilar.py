import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.toquvchilar import all_toquvchilar, create_new_toquvchi, update_weaver_r
from models.toquvchilar import Weavers
from schemas.toquvchilar import CreateToquvchi, UpdateToquvchi
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification


weaver_router = APIRouter(
    tags=["weavers (Toquvchilar) endpoints"]
)


@weaver_router.get("/weavers")
def get_weavers(
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
        return the_one(id, Weavers, db)
    return all_toquvchilar(search, page, limit, db)


@weaver_router.post("/create_weaver")
def create_weaver(toquvchi: CreateToquvchi,
                    current_user: UserCreate = Depends(get_current_active_user),
                    db: Session = Depends(database)):
    role_verification(current_user)
    create_new_toquvchi(toquvchi, db, current_user)
    raise HTTPException(status_code=201, detail="New weaver created")


@weaver_router.put("/update_weaver")
def update_weaver(toquvchi_update: UpdateToquvchi,
                    current_user: UserCreate = Depends(get_current_active_user),
                    db: Session = Depends(database)):
    role_verification(current_user)
    update_weaver_r(toquvchi_update, db, current_user)
    raise HTTPException(status_code=200, detail="The weaver updated")


