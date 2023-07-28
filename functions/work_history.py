from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.draws import Draws
from models.homes import Homes
from models.tools import Tools

from models.toquvchilar import Weavers
from models.users import Users
from models.work import Work
from models.work_history import Work_history
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_histories(page, limit, db):
    histories = db.query(Work_history).options(joinedload(Work_history.work))
    histories = histories.order_by(Work_history.id.asc())
    return pagination(histories, page, limit)


def create_new_work_history(form, thisuser, db):
    the_one(form.work_id, Work, db),
    the_one(form.tool_id, Tools, db),
    the_one(form.connection_user_id, Users, db)
    the_one(form.weaver_id, Weavers, db), the_one(form.draw_id, Draws, db),
    the_one(form.home_id, Homes, db)
    if db.query(Work_history).filter(Work_history.work_id == form.work_id).first():
        raise HTTPException(status_code=400, detail="The work already exists in the database")
    new_work_db = Work_history(
        money=0,
        work_id=form.work_id,
        # process_id=form.process_id,
        toquvchi_id=form.toquvchi_id,
        draw_id=form.draw_id,
        tool_id=form.tool_id,
        home_id=form.home_id,
        connection_user_id=form.connection_user_id,
        date=form.date,
        status=form.status,
        user_id=thisuser.id
    )
    save_in_db(db, new_work_db)

