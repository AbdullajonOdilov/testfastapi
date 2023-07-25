from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.expenses import Expenses
from models.homes import Homes
from models.tools import Tools
from models.toquvchilar import Toquvchilar
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_expenses(search, page, limit, db):
    expenses = db.query(Expenses).options(joinedload(Expenses.user), joinedload(Expenses.source_user))

    if search:
        expenses = expenses.filter(expenses.source.ilike(f"%{search}%"))
    expenses = expenses.order_by(Expenses.id.asc())
    return pagination(expenses, page, limit)


def create_new_expense(form, db, thisuser):
    new_expenses_db = Expenses(
        source=form.source,
        source_id=form.source_id,
        money=form.money,
        date=form.date,
        comment=form.comment,
        user_id=thisuser.id
    )
    save_in_db(db, new_expenses_db)

    getuser = db.query(Users).filter(Users.id == form.source_id).first()
    if (form.source == "admin" or form.source == "user") and getuser.status is True:
        db.query(Users).filter(Users.id == form.source_id).update({
            Users.balance: Users.balance + form.money
        })
        db.commit()
    elif form.source == "toquvchi":
        db.query(Toquvchilar).filter(Toquvchilar.id == form.source_id).update({
            Toquvchilar.balance: Toquvchilar.balance + form.money
        })
        db.commit()
    elif form.source == "home":
        db.query(Homes).filter(Homes.id == form.source_id).update({
            Homes.balance: Homes.balance + form.money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source error,"
                                                    " it can be user, admin, toquvchi, home, tool")


def update_expense_r(form, db, thisuser):
    the_one(id, Expenses, db), the_one(form.source_id, Users, db)
    getuser = db.query(Users).filter(Users.id == form.source_id).first()
    if getuser.status is False:
        raise HTTPException(status_code=400, detail="status is not supported")
    db.query(Expenses).filter(Expenses.id == form.id).update({
        Expenses.source: form.source,
        Expenses.source_id: form.source_id,
        Expenses.money: form.money,
        Expenses.date: form.date,
        Expenses.comment: form.comment,
        Expenses.user_id: thisuser.id
    })
    db.commit()


