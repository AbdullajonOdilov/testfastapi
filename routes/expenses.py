from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.expenses import all_expenses, create_new_expense, delete_expense_r
from models.expenses import Expenses
from schemas.expenses import CreateExpenses
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

expenses_router = APIRouter(
    tags=["Expenses endpoints"]
)


@expenses_router.get("/expenses")
def get_expenses(search: str = None, id: int = 0, page: int = 0,
                 limit: int = 10,
                 db: Session = Depends(database),
                 current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Expenses, db)
    return all_expenses(search, page, limit, db)


@expenses_router.post("/create_expenses")
def create_expenses(expense: CreateExpenses,
                    current_user: UserCreate = Depends(get_current_active_user),
                    db: Session = Depends(database)):
    role_verification(current_user)
    create_new_expense(expense, db, current_user)
    raise HTTPException(status_code=201, detail="New expense created")


@expenses_router.delete("/delete_expenses")
def delete_expense(id: int,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    delete_expense_r(id, db)
    raise HTTPException(status_code=200, detail="The expense deleted")

