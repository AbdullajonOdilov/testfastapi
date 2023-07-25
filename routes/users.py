import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.users import all_users, create_new_user, update_user_r
from models.users import Users
from schemas.users import UserCreate, UserUpdate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

users_router = APIRouter(
    prefix="",
    tags=["Users operation"]
)




@users_router.get("/users")
def get_users(
        search: str = None,
        id: int = 0,
        page: int = 0,
        limit: int = 10,
        status: bool = None,
        db: Session = Depends(database),
        current_user: UserCreate = Depends(get_current_active_user)

):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Users, db)
    return all_users(search, page, limit, status, db)

@users_router.post("/create_user")
def create_user(new_user: UserCreate, db: Session = Depends(database),
                current_user: UserCreate = Depends(get_current_active_user)
                ):

    role_verification(current_user)
    create_new_user(new_user, db)
    raise HTTPException(status_code=201, detail="New user created")


@users_router.put("/update_user")
def update_user(this_user: UserUpdate, db: Session = Depends(database),
                current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    update_user_r(this_user, db)
    raise HTTPException(status_code=200, detail="User updated successfully")


@users_router.get("/request_user")
def request_user(current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    return current_user
