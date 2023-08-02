from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.homes import Homes
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_homes(search, page, limit, db):
    homes = db.query(Homes).options(joinedload(Homes.user))

    if search:
        homes = homes.filter(Homes.address.ilike(f"%{search}%"))
    homes = homes.order_by(Homes.id.asc())
    return pagination(homes, page, limit)


def create_new_home(form, db, thisuser):
    if db.query(Homes).filter(Homes.phone_number == form.phone_number).first():
        raise HTTPException(status_code=400, detail="Home phone number already exists database")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number must be longer than 9 characters")
    new_home_db = Homes(
        name=form.name,
        address=form.address,
        phone_number=form.phone_number,
        balance=0,
        user_id=thisuser.id
    )
    save_in_db(db, new_home_db)


def update_home_r(form, db, thisuser):
    home = the_one(form.id, Homes, db)
    if db.query(Homes).filter(Homes.phone_number == form.phone_number).first()\
            and home.phone_number != form.phone_number:
        raise HTTPException(status_code=400, detail="Home  error")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number must be longer than 9 characters")

    db.query(Homes).filter(Homes.id == form.id).update({
        Homes.address: form.address,
        Homes.phone_number: form.phone_number,
        Homes.name: form.name,
        Homes.user_id: thisuser.id

    })
    db.commit()

