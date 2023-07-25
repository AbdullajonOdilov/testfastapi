from fastapi import HTTPException

from models.suppliers import Suppliers
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_suppliers(search, page, limit, db):
    suppliers = db.query(Suppliers)

    if search:
        suppliers = suppliers.filter(Suppliers.name.ilike(f"%{search}%"))
    suppliers = suppliers.order_by(Suppliers.name.asc())
    return pagination(suppliers, page, limit)


def create_new_supplier(form, db, thisuser):
    if db.query(Suppliers).filter(Suppliers.phone_number == form.phone_number).first():
        raise HTTPException(status_code=400, detail="Supplier error")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number must be  9 numbers ")
    new_supplier_db = Suppliers(
        name=form.name,
        address=form.address,
        phone_number=form.phone_number,
        balance=0,
        user_id=thisuser.id
    )
    save_in_db(db, new_supplier_db)


def update_supplier_r(form, db, thisuser):
    the_one(form.id, Suppliers, db)
    if db.query(Suppliers).filter(Suppliers.phone_number == form.phone_number).first():
        raise HTTPException(status_code=400, detail="Supplier error")
    if len(str(form.phone_number)) != 9:
        raise HTTPException(status_code=400, detail="Phone number must be  9 characters")
    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.name: form.name,
        Suppliers.address: form.address,
        Suppliers.phone_number: form.phone_number,

        Suppliers.user_id: thisuser.id
    })
    db.commit()

