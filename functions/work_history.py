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


def create_new_work_history(work_id, money, date, status, db):
    if db.query(Work_history).filter(Work_history.work_id == work_id).first():
        raise HTTPException(status_code=400, detail="The work already exists in the database")
    new_work_db = Work_history(
        work_id=work_id,
        money=money,
        date=date,
        status=status,
    )
    save_in_db(db, new_work_db)

