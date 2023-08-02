import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.supplies import all_supplies, create_new_supply, delete_supply_r
from models.supplies import Supplies
from schemas.supplies import CreateSupplies, UpdateSupplies
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

supplies_router = APIRouter(
    tags=["Supplies endpoints"]
)


@supplies_router.get("/get_supplies")
def get_supplies(search: str = None, id: int = 0, page: int = 0, limit: int = 10,
                  db: Session = Depends(database),
                 current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Supplies, db)
    return all_supplies(search, page, limit, db)


@supplies_router.post("/create_supply")
def create_supply(new_supply: CreateSupplies, db: Session = Depends(database),
                  current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    create_new_supply(new_supply, db, current_user)
    raise HTTPException(status_code=201, detail="Supply created successfully")


@supplies_router.delete("/delete_supply")
def deleter_supply(id: int, db: Session = Depends(database),
                  current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    delete_supply_r(current_user, id, db)
    raise HTTPException(status_code=200, detail="The supply deleted")

