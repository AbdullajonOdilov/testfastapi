from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from functions.warehouse_products import create_new_warehouse
from models.products import Products
from models.suppliers import Suppliers
from models.supplies import Supplies
from models.store import Stores
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_supplies(search, page, limit, db):
    supplies = db.query(Supplies).options(joinedload(Supplies.product).load_only(Products.name), joinedload(Supplies.suppliers).load_only(Suppliers.name))
    if search:
        search_formatted = "%{}%".format(search)
        supplies = supplies.filter(Suppliers.name.like(search_formatted) |
                                   Products.name.like(search_formatted) |
                                   Stores.name.like(search_formatted))

    supplies = supplies.order_by(Supplies.id.asc())
    return pagination(supplies, page, limit)


def create_new_supply(form, db, thisuser):
    the_one(form.suppliers_id, Suppliers, db), the_one(form.product_id, Products, db),
    the_one(form.store_id, Stores, db)
    new_supply_db = Supplies(
        measure=form.measure,
        quantity=form.quantity,
        price=form.price,
        date=form.date,
        product_id=form.product_id,
        suppliers_id=form.suppliers_id,
        store_id=form.store_id,
        user_id=thisuser.id,
    )
    save_in_db(db, new_supply_db)
    # Calculate the amount
    total_price = form.quantity * form.price
    # Update the supplier's balance
    supplier = db.query(Suppliers).get(form.suppliers_id)
    if supplier:
        db.query(Suppliers).filter(Suppliers.id == supplier.id).update({
            Suppliers.balance: Suppliers.balance - total_price
        })
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Supplier not found")
    warehouse=db.query(Warehouse_products).filter(Warehouse_products.product_id == form.product_id).first()
    price = db.query(Warehouse_products).filter(Warehouse_products.price==form.price).first()
    if warehouse and price:
        warehouse.quantity += form.quantity
        save_in_db(db, warehouse)
    else:
        create_new_warehouse(
            measure=form.measure,
            quantity=form.quantity,
            price=form.price,
            product_id=form.product_id,
            store_id=form.store_id,
            db=db
        )


def delete_supply_r(user, id, db):
    supply = the_one(id, Supplies, db)
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Role error!")

    # Check if there is enough quantity of products in the database
    warehouse_quantity = db.query(Warehouse_products.quantity).filter(
        Warehouse_products.product_id == supply.product_id).scalar()
    if warehouse_quantity is None or warehouse_quantity < supply.quantity:
        raise HTTPException(status_code=400, detail="There are not enough quantity of products in the database")

    # Update the quantity in Warehouse_products and then delete the supply
    db.query(Warehouse_products).filter(Warehouse_products.product_id == supply.product_id).update({
        Warehouse_products.quantity: Warehouse_products.quantity - supply.quantity
    })

    db.query(Supplies).filter(Supplies.id == id).delete()
    db.commit()

