from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.warehouse_products import create_new_warehouse
from models.products import Products
from models.suppliers import Suppliers
from models.supplies import Supplies
from models.store import Stores
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one, update_in_db
from utils.pagination import pagination


def all_supplies(search, page, limit, db):
    supplies = db.query(Supplies).options(joinedload(Supplies.product), joinedload(Supplies.suppliers))
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
    # if db.query(Supplies).filter(Supplies.product_id == form.product_id).first():
    #     raise HTTPException(status_code=404, detail="That product is available in the database")
    # elif db.query(Supplies).filter(Supplies.suppliers_id == form.suppliers_id).first():
    #     raise HTTPException(status_code=404, detail="That supplier is available in the database")
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
            db=db)



def update_supply_r(supply, db, thisuser):
    # product = db.query(Products).filter(Products.id == supply.product_id).first()
    # supplier = db.query(Suppliers).filter(Suppliers.id == supply.suppliers_id).first()
    #
    the_one(supply.id, Supplies, db), the_one(supply.suppliers_id, Suppliers, db),\
    the_one(supply.product_id, Products, db), the_one(supply.warehouse_id, Warehouse_products, db)
    # if (product and supplier) or (product is None and supplier is None):
    #     raise HTTPException(status_code=400, detail="You must input Product or Supplier")
    db.query(Supplies).filter(Supplies.id == supply.id).update({
        Supplies.measure: supply.measure,
        Supplies.quantity: supply.quantity,
        Supplies.price: supply.price,
        Supplies.date: supply.date,
        Supplies.product_id: supply.product_id,
        Supplies.suppliers_id: supply.suppliers_id,
        Supplies.store_id: supply.store_id,
        # Supplies.user_id: thisuser.id
    })
    db.commit()

#
# def delete_supply_r(user, id, db):
#     the_one(id, Supplies, db)
#     if user.role != "admin":
#         raise HTTPException(status_code=400, detail="Role error!")
#     db.query(Supplies).filter(Supplies.id == id).delete()
#     db.commit()
