from fastapi import HTTPException
from models.products import Products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_products(search, page, limit, db):
    products = db.query(Products)
    if search:
        products = products.filter(Products.name.ilike(f"%{search}%"))
    products = products.order_by(Products.id.desc())
    return pagination(products, page, limit)


def create_new_product(form, db):
    if db.query(Products).filter(Products.name == form.name).first():
        raise HTTPException(status_code=400, detail="The product already exists in the database")
    new_product_db = Products(
        name=form.name,
    )
    save_in_db(db, new_product_db)


def update_product_r(product_update, db):
    the_one(product_update.id, Products, db)
    if db.query(Products).filter(Products.name == product_update.name).first():
        raise HTTPException(status_code=400, detail="The product already exists in the database")
    db.query(Products).filter(Products.id == product_update.id).update({
        Products.name: product_update.name,
    })
    db.commit()


