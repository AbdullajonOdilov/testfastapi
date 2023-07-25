from fastapi import HTTPException

from models.products import Products
from models.store import Stores
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one, update_in_db
from utils.pagination import pagination



def all_warehouses(page, limit, db):
    warehouse_products = db.query(Warehouse_products)
    warehouse_products = warehouse_products.order_by(Warehouse_products.id.desc())
    return pagination(warehouse_products, page, limit)



def create_new_warehouse(measure,quantity,price,product_id, store_id, db):
    the_one(product_id, Products, db), the_one(store_id, Stores, db)
    # if db.query(Warehouse).filter(Warehouse.product_id == form.product_id).first():
    #     raise HTTPException(status_code=404, detail="That product is available in the database")
    new_warehouse_db = Warehouse_products(
        measure=measure,
        quantity=quantity,
        price=price,
        product_id=product_id,
        store_id=store_id
    )
    save_in_db(db, new_warehouse_db)


def update_warehouse_r(form, db):
    the_one(form.id, Warehouse_products, db), the_one(form.product_id, Products, db),
    the_one(form.store_id, Stores, db)
    db.query(Warehouse_products).filter(Warehouse_products.id == form.id).update({
        Warehouse_products.measure: form.measure,
        Warehouse_products.quantity: form.quantity,
        Warehouse_products.price: form.price,
        Warehouse_products.product_id: form.product_id,
        Warehouse_products.store_id: form.store_id
    })

    db.commit()


def delete_warehouse_p(user, id, db):
    the_one(id, Warehouse_products, db)
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Role error!")
    db.query(Warehouse_products).filter(Warehouse_products.id == id).delete()
    db.commit()