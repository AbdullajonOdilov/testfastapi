import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.proces import all_proces, update_process_r, create_new_process
from models.proces import Process
from schemas.proces import CreateProcess, UpdateProcess
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

proces_router = APIRouter(
    tags=["Process endpoints"]
)

@proces_router.get("/get_proces")
def get_proces(id: int = 0, search: str = None, page: int = 0, limit: int = 10, status: bool =None,
                   db: Session = Depends(database),
                   current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Process, db)
    return all_proces(search, page, limit, status, db)


@proces_router.post("/create_process")
def create_process(new_process: CreateProcess,
                   db: Session = Depends(database),
                   current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    create_new_process(new_process, db, current_user)
    raise HTTPException(status_code=201, detail="New process created")


@proces_router.put("/update_process")
def update_process(update_p: UpdateProcess, db: Session = Depends(database),
                   current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    update_process_r(update_p, db, current_user)
    raise HTTPException(status_code=200, detail="The process updated")

