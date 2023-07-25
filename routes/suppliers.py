import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.suppliers import all_suppliers, create_new_supplier, update_supplier_r
from models.suppliers import Suppliers
from schemas.suppliers import CreateSuppliers, UpdateSuppliers
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

suppliers_router = APIRouter(
    tags=["Suppliers endpoints"]
)


@suppliers_router.get("/suppliers")
def get_suppliers(
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
        return the_one(id, Suppliers, db)
    return all_suppliers(search, page, limit, db)


@suppliers_router.post("/create_supplier")
def create_supplier(supplier: CreateSuppliers,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_supplier(supplier, db, current_user)
    raise HTTPException(status_code=201, detail="New supplier created")

@suppliers_router.put("/update_supplier")
def update_supplier(supplier_update: UpdateSuppliers,
                    current_user: UserCreate = Depends(get_current_active_user),
                    db: Session = Depends(database)):
    role_verification(current_user)
    update_supplier_r(supplier_update, db, current_user)
    raise HTTPException(status_code=200, detail="The supplier updated")

