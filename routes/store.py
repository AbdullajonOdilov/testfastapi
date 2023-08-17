import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.store import all_stores, create_new_store, update_store_r
from models.store import Stores
from schemas.store import CreateStore, UpdateStore
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

stores_router = APIRouter(
    tags=["Stores(Warehouse) endpoints"]
)


@stores_router.get("/stores")
def get_stores(
    search: str = None,
    id: int = 0,
    page: int = 0,
    limit: int = 10,
    db: Session = Depends(database),
    current_user: UserCreate = Depends(get_current_active_user),
):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Stores, db)
    return all_stores(search, page, limit, db)


@stores_router.post("/create_store")
def create_store(store: CreateStore,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_store(store, db, current_user)
    raise HTTPException(status_code=201, detail="New store created")


@stores_router.put("/update_store")
def update_store(store_update: UpdateStore,
                 current_user: UserCreate = Depends(get_current_active_user),
                 db: Session = Depends(database)):
    role_verification(current_user)
    update_store_r(store_update, db, current_user)
    raise HTTPException(status_code=200, detail="The store updated")
