import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.warehouse_products import all_warehouses
from models.warehouse_products import Warehouse_products
from schemas.users import UserCreate
# from schemas.warehouse_products import CreateWarehouse, UpdateWarehouse
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

warehouses_router = APIRouter(
    tags=["Warehouse_products endpoints"]
)


@warehouses_router.get("/get_warehouses")
def get_warehouses(id: int = 0, page: int = 0, limit: int = 10,
                   db: Session = Depends(database),
                   current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Warehouse_products, db)

    return all_warehouses(page, limit, db)




