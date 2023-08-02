from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.toquvchilar import Weavers
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_toquvchilar(search, page, limit, db):
    weavers = db.query(Weavers).options(joinedload(Weavers.user))

    if search:
        weavers = weavers.filter(Weavers.name.ilike(f"%{search}%"))
    weavers = weavers.order_by(Weavers.name.asc())
    return pagination(weavers, page, limit)


def create_new_toquvchi(form, db, thisuser):
    if db.query(Weavers).filter(Weavers.phone_number == form.phone_number).first():
        raise HTTPException(status_code=400, detail="Weaver  error")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number length must be longer than 9")
    new_weaver_db = Weavers(
        name=form.name,
        address=form.address,
        balance=0,
        comment=form.comment,
        phone_number=form.phone_number,
        user_id=thisuser.id
    )
    save_in_db(db, new_weaver_db)


def update_weaver_r(form, db, thisuser):
    weaver = the_one(form.id, Weavers, db)
    if db.query(Weavers).filter(Weavers.phone_number == form.phone_number).first() and weaver.phone_number != form.phone_number:
        raise HTTPException(status_code=400, detail="Weaver  error")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number must be longer than 9 characters")

    db.query(Weavers).filter(Weavers.id == form.id).update({
        Weavers.name: form.name,
        Weavers.phone_number: form.phone_number,
        # Weavers.balance: form.balance,
        Weavers.comment: form.comment,
        Weavers.address: form.address,
        Weavers.user_id: thisuser.id
    })
    db.commit()

