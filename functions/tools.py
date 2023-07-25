from fastapi import HTTPException

from models.tools import Tools
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_tools(search, page, limit, status, db):
    tools = db.query(Tools)
    if search:
        search_filter = Tools.name.ilike(f"%{search}%")
    else:
        search_filter = Tools.id > 0
    if status is True:
        status_filter = Tools.status = True
    elif status is False:
        status_filter = Tools.status = False
    else:
        status_filter = Tools.id > 0
    tools = tools.filter(search_filter, status_filter).order_by(Tools.id.asc())
    return pagination(tools, page, limit)


def create_new_tool(form, db, thisuser):
    if db.query(Tools).filter(Tools.name == form.name).first():
        raise HTTPException(status_code=400, detail="Tool error")
    new_tool_db = Tools(
        name=form.name,
        status=form.status,
        user_id=thisuser.id
    )
    save_in_db(db, new_tool_db)


def update_tool_r(tool_update, db, thisuser):
    the_one(tool_update.id, Tools, db)
    if db.query(Tools).filter(Tools.name == tool_update.name).first():
        raise HTTPException(status_code=400, detail="Tool error")
    db.query(Tools).filter(Tools.id == id).update({
        Tools.name: tool_update.name,
        Tools.status: tool_update.status,
        Tools.user_id: thisuser.id
    })
    db.commit()

# def delete_tool_r(user, id, db):
#     the_one(id, Tools, db)
#     if user.role != "admin":
#         raise HTTPException(status_code=400, detail="Role error!")
#     db.query(Tools).filter(Tools.id == id).delete()
#     db.commit()