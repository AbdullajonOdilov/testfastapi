from fastapi import HTTPException

from models.store import Stores
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_stores(search, page, limit, db):
    stores = db.query(Stores)

    if search:
        stores = stores.filter(Stores.name.ilike(f"%{search}%"))
    stores = stores.order_by(Stores.name.asc())
    return pagination(stores, page, limit)


def create_new_store(form, db, thisuser):
    if db.query(Stores).filter(Stores.name == form.name).first():
        raise HTTPException(status_code=400, detail="Store already exists")
    new_store_db = Stores(
        name=form.name,
        address=form.address,
        user_id=thisuser.id
    )
    save_in_db(db, new_store_db)


def update_store_r(form, db, thisuser):
    store = the_one(form.id, Stores, db)
    if db.query(Stores).filter(Stores.name == form.name).first() and store.name != form.name:
        raise HTTPException(status_code=400, detail="Store already exists")
    db.query(Stores).filter(Stores.id == form.id).update({
        Stores.name: form.name,
        Stores.address: form.address,
        Stores.user_id: thisuser.id
    })
    db.commit()

