from fastapi import FastAPI


from routes.draws import draws_router
from routes.expenses import expenses_router
from routes.homes import homes_router
from routes.kpi import kpi_router
from routes.kpi_history import kpihistory_router
from routes.material_type import material_router
from routes.proces import proces_router
from routes.products import products_router
from routes.store import stores_router
from routes.suppliers import suppliers_router

from routes.supplies import supplies_router
from routes.tools import tools_router
from routes.toquvchilar import toquvchilar_router
from routes.users import users_router
from routes.warehouse_products import warehouses_router
from routes.work import work_router
from routes.work_history import work_history_router
from utils.login import login_router

app = FastAPI()

app.include_router(login_router)
app.include_router(users_router)

app.include_router(stores_router)
app.include_router(suppliers_router)
app.include_router(products_router)
app.include_router(supplies_router)
app.include_router(warehouses_router)
app.include_router(material_router)

app.include_router(proces_router)
app.include_router(kpi_router)
app.include_router(kpihistory_router)
app.include_router(work_router)
app.include_router(work_history_router)
app.include_router(expenses_router)

app.include_router(tools_router)
app.include_router(draws_router)
app.include_router(toquvchilar_router)
app.include_router(homes_router)





