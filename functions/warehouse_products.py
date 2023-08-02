from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.products import Products
from models.store import Stores
from models.warehouse_products import Warehouse_products
from utils.db_operations import save_in_db, the_one, update_in_db
from utils.pagination import pagination


def all_warehouses(page, limit, db):
    warehouse_products = db.query(Warehouse_products).\
        options(joinedload(Warehouse_products.product).load_only(Products.name), joinedload(Warehouse_products.store).load_only(Stores.name))
    warehouse_products = warehouse_products.order_by(Warehouse_products.id.desc())
    return pagination(warehouse_products, page, limit)


def create_new_warehouse(measure, quantity, price, product_id, store_id, db):
    the_one(product_id, Products, db), the_one(store_id, Stores, db)
    new_warehouse_db = Warehouse_products(
        measure=measure,
        quantity=quantity,
        price=price,
        product_id=product_id,
        store_id=store_id
    )
    save_in_db(db, new_warehouse_db)

