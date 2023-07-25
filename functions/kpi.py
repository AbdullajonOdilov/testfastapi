from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.kpi import Kpi
from models.proces import Process
from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_kpi(page, limit, db):
    kpi = db.query(Kpi).options(joinedload(Kpi.proces))
    kpi = kpi.order_by(Kpi.id.desc())
    return pagination(kpi, page, limit)


def create_new_kpi(form, db):
    the_one(form.proces_id, Process, db), the_one(form.user_id, Users, db)
    existing_kpi = db.query(Kpi).filter(Kpi.proces_id == form.proces_id).first()
    if existing_kpi:
        raise HTTPException(status_code=400, detail="Process id already exists")

    new_kpi_db = Kpi(
        proces_id=form.proces_id,
        price=form.price,
        user_id=form.user_id  # 6
    )
    save_in_db(db, new_kpi_db)

    user = db.query(Users).filter(Users.id == form.user_id).first()
    if form.price:
        db.query(Users).filter(Users.id == user.id).update({
            Users.balance: Users.balance + form.price
        })
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")


def update_kpi_r(form, db):
    the_one(form.id, Kpi, db), the_one(form.user_id, Users, db)
    proces = the_one(form.proces_id, Process, db)
    existing_kpi = db.query(Kpi).filter(Kpi.proces_id == form.proces_id).first()
    if existing_kpi and proces.id != form.proces_id:
        raise HTTPException(status_code=400, detail="Process id already exists")

    db.query(Kpi).filter(Kpi.id == form.id).update({
        Kpi.proces_id: form.proces_id,
        Kpi.price: form.price,
        Kpi.user_id: form.user_id
    })
    db.commit()

    user = db.query(Users).filter(Users.id == form.user_id).first()
    if form.price:
        db.query(Users).filter(Users.id == user.id).update({
            Users.balance: form.price
        })
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")
