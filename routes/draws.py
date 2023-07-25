import inspect

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from database import database
from functions.draws import all_draws, create_new_draw, update_draw_r
from models.draws import Draws
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

draws_router = APIRouter(
    tags=["Draws(chizgilar) operation"]
)



@draws_router.get("/draws")
def get_draws(
        search: str = None,
        id: int = 0,
        page: int = 0,
        limit: int = 10,
        status: bool = None,
        db: Session = Depends(database),
        current_user: UserCreate = Depends(get_current_active_user)):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Draws, db)
    role_verification(current_user)
    return all_draws(search, page, limit, status, db)


@draws_router.post("/create_draws")
def create_draw(name: str, status: bool = None,
                current_user: UserCreate = Depends(get_current_active_user),
                db: Session = Depends(database),
                file: UploadFile = File(None)):
    role_verification(current_user)
    create_new_draw(name, status, db, current_user, file)
    raise HTTPException(status_code=201, detail="New draw created")

@draws_router.put("/update_draw")
def update_draw(
    id: int = Form(0),
    name: str = Form(None),
    status: bool = Form(None),
    db: Session = Depends(database),
    current_user: UserCreate = Depends(get_current_active_user),
    file: UploadFile = File(None)
):
    role_verification(current_user)
    update_draw_r(id, name, status, db, current_user, file)
    return {"message": "The draw updated"}




