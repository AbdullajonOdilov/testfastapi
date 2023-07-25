from fastapi import HTTPException

from models.toquvchilar import Toquvchilar
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_toquvchilar(search, page, limit, db):
    toquvchilar = db.query(Toquvchilar)

    if search:
        toquvchilar = toquvchilar.filter(Toquvchilar.name.ilike(f"%{search}%"))
    toquvchilar = toquvchilar.order_by(Toquvchilar.name.asc())
    return pagination(toquvchilar, page, limit)

def create_new_toquvchi(form, db, thisuser):
    if db.query(Toquvchilar).filter(Toquvchilar.phone_number == form.phone_number).first():
        raise HTTPException(status_code=400, detail="Toquvchi  error")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number length must be longer than 9")
    new_toquvchi_db = Toquvchilar(
        name=form.name,
        address=form.address,
        balance=0,
        comment=form.comment,
        phone_number=form.phone_number,
        user_id=thisuser.id
    )
    save_in_db(db, new_toquvchi_db)


def update_toquvchi_r(toquvchi_update, db, thisuser):
    the_one(toquvchi_update.id, Toquvchilar, db)
    if db.query(Toquvchilar).filter(Toquvchilar.phone_number == toquvchi_update.phone_number).first():
        raise HTTPException(status_code=400, detail="Toquvchi  error")
    if len(str(toquvchi_update.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number must be longer than 9 characters")

    db.query(Toquvchilar).filter(Toquvchilar.id == toquvchi_update.id).update({
        Toquvchilar.name: toquvchi_update.name,
        Toquvchilar.phone_number: toquvchi_update.phone_number,
        # Toquvchilar.balance: toquvchi_update.balance,
        Toquvchilar.comment: toquvchi_update.comment,
        Toquvchilar.address: toquvchi_update.address,
        Toquvchilar.user_id: thisuser.id
    })
    db.commit()
