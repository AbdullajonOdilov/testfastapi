from fastapi import HTTPException

from models.material_type import Material_type
from models.products import Products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_materials(search, page, limit, db):
    materials = db.query(Material_type)
    if search:
        materials = materials.filter(Material_type.name.ilike(f"%{search}%"))
    materials = materials.order_by(Material_type.id.desc())
    return pagination(materials, page, limit)


def create_new_material(form, db, thisuser):
    the_one(form.product_id, Products, db)
    if db.query(Material_type).filter(Material_type.name == form.name).first():
        raise HTTPException(status_code=400, detail="The material already exists in the database")
    new_material_db = Material_type(
        name=form.name,
        product_id=form.product_id,
        user_id=thisuser.id
    )
    save_in_db(db, new_material_db)


def update_material_r(form, db, thisuser):
    material_type = the_one(form.id, Material_type, db)  # Use assignment operator instead of comma
    the_one(form.product_id, Products, db)  # This line is correct as it is

    if db.query(Material_type).filter(Material_type.name == form.name).first() \
            and material_type.name != form.name:
        raise HTTPException(status_code=400, detail="The material already exists in the database")

    db.query(Material_type).filter(Material_type.id == form.id).update({
        Material_type.product_id: form.product_id,
        Material_type.name: form.name,
        Material_type.user_id: thisuser.id
    })
    db.commit()



