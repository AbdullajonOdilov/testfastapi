import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.products import all_products, create_new_product, update_product_r
from models.products import Products
from schemas.products import CreateProduct, UpdateProduct
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

products_router = APIRouter(
    tags=["Products endpoints"]
)


@products_router.get("/products")
def get_products(

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
        return the_one(id, Products, db)
    return all_products(search, page, limit, db)


@products_router.post("/create_product")
def create_product(product: CreateProduct,
                    current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_product(product, db)
    raise HTTPException(status_code=201, detail="New product created")

@products_router.put("/update_product")
def update_product(product_update: UpdateProduct,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    update_product_r(product_update, db)
    raise HTTPException(status_code=200, detail="The product updated")

