from datetime import datetime, timedelta, date

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.expenses import Expenses
from models.homes import Homes

from models.toquvchilar import Weavers
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

    if form.source not in ['admin', 'user', 'home', 'weaver']:
        raise HTTPException(status_code=400, detail="source error")
    new_expenses_db = Expenses(
        source=form.source,
        source_id=form.source_id,
        money=form.money,
        date=datetime.now(),
        comment=form.comment,
        user_id=thisuser.id
    )
    save_in_db(db, new_expenses_db)

    getuser = db.query(Users).filter(Users.id == form.source_id).first()
    if form.source == "admin" or form.source == "user":
        the_one(form.source_id, Users, db)
        db.query(Users).filter(Users.id == form.source_id).update({
            Users.balance: Users.balance + form.money
        })
        db.commit()
    elif form.source == "weaver":
        the_one(form.source_id, Weavers, db)
        db.query(Weavers).filter(Weavers.id == form.source_id).update({
            Weavers.balance: Weavers.balance + form.money
        })
        db.commit()
    elif form.source == "home":
        the_one(form.source_id, Homes, db)
        db.query(Homes).filter(Homes.id == form.source_id).update({
            Homes.balance: Homes.balance + form.money
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="source_id or source error,"
                                                    " source can be user, admin, weaver, home")


def delete_expense_r(id, db):
    expense = the_one(id, Expenses, db)
    current_time = datetime.now()

    print("Current Time:", current_time)
    print("Expense Creation Time:", expense.date)

    # Check if the expense was created more than 5 minutes ago
    if current_time - expense.date > timedelta(minutes=5):
        raise HTTPException(status_code=400, detail="You can only delete expenses created within the last 5 minutes")

    # If the expense is within the 5-minute window, proceed with the deletion and balance update
    # Update the source's balance by subtracting the money from it
    if expense.source == "user" or expense.source == "admin":
        the_one(expense.source_id, Users, db)
        db.query(Users).filter(Users.id == expense.source_id).update({
            Users.balance: Users.balance - expense.money
        })
    elif expense.source == "weaver":
        the_one(expense.source_id, Weavers, db)
        db.query(Weavers).filter(Weavers.id == expense.source_id).update({
            Weavers.balance: Weavers.balance - expense.money
        })
    elif expense.source == "home":
        the_one(expense.source_id, Homes, db)
        db.query(Homes).filter(Homes.id == expense.source_id).update({
            Homes.balance: Homes.balance - expense.money
        })
    db.query(Expenses).filter(Expenses.id == id).delete()
    db.commit()




