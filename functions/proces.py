from sqlalchemy import and_

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.material_type import Material_type
from models.proces import Process
from models.products import Products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_proces(search, page, limit, status, db):
    proces = db.query(Process).options(joinedload(Process.product), joinedload(Process.material_type))
    search_filter = None

    if search:
        search_filter = Process.name.ilike(f"%{search}%")
    elif status is True:
        proces = proces.filter(Process.status == True)
    elif status is False:
        proces = proces.filter(Process.status == False)
    if search_filter is not None:
        proces = proces.filter(search_filter)
    proces = proces.order_by(Process.id.desc())
    return pagination(proces, page, limit)


def create_new_process(form, db, thisuser):
    the_one(form.product_id, Products, db)
    the_one(form.material_type_id, Material_type, db),

    if db.query(Process).filter(Process.name == form.name).first():
        raise HTTPException(status_code=400, detail="The process already exists")
    existing_process = db.query(Process).filter(and_(Process.step == form.step, Process.product_id == form.product_id)).first()
    if existing_process:
        raise HTTPException(status_code=400, detail="Step cannot be same for the product_id")

    new_process_db = Process(
        product_id=form.product_id,
        material_type_id=form.material_type_id,
        name=form.name,
        step=form.step,
        deadline=form.deadline,
        connection_id=form.connection_id,
        connection=form.connection,
        user_id=thisuser.id,
    )
    save_in_db(db, new_process_db)


def update_process_r(form, db, thisuser):
    the_one(form.id, Process, db), the_one(form.product_id, Products, db),
    the_one(form.material_type_id, Material_type, db)
    if db.query(Process).filter(Process.name == form.name).first():
        raise HTTPException(status_code=400, detail="The process already exists")
    existing_process = db.query(Process).filter(and_(Process.step == form.step, Process.product_id == form.product_id)).first()
    if existing_process:
        raise HTTPException(status_code=400, detail="Step cannot be same for the product_id")

    db.query(Process).filter(Process.id == form.id).update({
        Process.product_id: form.product_id,
        Process.material_type_id: form.material_type_id,
        Process.name: form.name,
        Process.step: form.step,
        Process.deadline: form.deadline,
        Process.connection_id: form.connection_id,
        Process.connection: form.connection,
        Process.user_id: thisuser.id

    })
    db.commit()
