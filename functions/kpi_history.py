from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.kpi import Kpi
from models.kpi_histories import Kpi_history
from models.proces import Process
from models.users import Users
from models.work import Work
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_kpi_histories(page, limit, db):
    histories = db.query(Kpi_history).options(joinedload(Kpi_history.kpi))
    histories = histories.order_by(Kpi_history.id.desc())
    return pagination(histories, page, limit)


def create_new_kpihistory(form, db):
    the_one(form.id, Kpi, db), the_one(form.process_id, Process, db),
    the_one(form.work_id, Work, db),  the_one(form.user_id, Users, db)

    if db.query(Kpi_history).filter(Kpi_history.kpi_id == form.kpi_id).first():
        raise HTTPException(status_code=400, detail="The kpi already exists in the database")

    if db.query(Kpi_history).filter(Kpi_history.work_id == form.work_id).first():
        raise HTTPException(status_code=400, detail="The work already exists in the database")

    new_kpi_history_db = Kpi_history(
        kpi_id=form.kpi_id,
        process_id=form.process_id,
        work_id=form.work_id,
        date=form.date,
        user_id=form.user_id,
    )
    save_in_db(db, new_kpi_history_db)