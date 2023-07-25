from sqlalchemy.orm import joinedload
from models.material_type import Material_type
from models.proces import Process
from models.users import Users
from models.work import Work
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_work(search, page, limit, db):
    works = db.query(Work).options(joinedload(Work.proces), joinedload(Work.material))
    if search:
        works = db.query(Material_type).filter(Material_type.name.ilike(f"%{search}%"))
    works = works.order_by(Work.id.desc())
    return pagination(works, page, limit)


def create_new_work(form, db, thisuser):
    # if db.query(Work).filter(Work.material_id == form.material_id).first():
    #     raise HTTPException(status_code=400, detail="The material  already exists in the database")
    the_one(form.material_type_id, Material_type, db),
    the_one(form.proces_id, Process, db)
    new_work_db = Work(
        material_type_id=form.material_type_id,
        proces_id=form.proces_id,
        comment=form.comment,
        user_id=thisuser.id
    )

    save_in_db(db, new_work_db)


def update_work_r(work_update, db, thisuser):
    the_one(work_update.id, Work, db),
    the_one(work_update.material_type_id, Material_type, db),
    the_one(work_update.proces_id, Process, db),
    # process = db.query(Process).filter(Process.id == work_update.proces_id).first() #6
    db.query(Work).filter(Work.id == work_update.id).update({
        Work.material_type_id: work_update.material_type_id,
        Work.proces_id: work_update.proces_id,
        Work.comment: work_update.comment,
        Work.user_id: thisuser.id
    })
    db.commit()

    # process2 = db.query(Process).filter(Process.id == Work.proces_id).first() #5
    #
    # kpis_id = db.query(Kpi).filter(Kpi.proces_id == process.id).first()  # 14
    #
    # kpi_history_id = db.query(Kpi_history).filter(Kpi_history.kpi_id == kpis_id.id).first()
    # user_id = kpis_id.user_id
    #
    # kpi_record = db.query(Kpi).filter(Kpi.user_id == user_id).first()
    # user_record = db.query(Users).filter(Users.id == user_id).first()
    #
    # if process.step > process2.step:
    #
    #     the_one(kpi_history_id, Kpi_history, db)
    #     if thisuser.role != "admin":
    #         raise HTTPException(status_code=400, detail="Role error!")
    #     db.query(Kpi_history).filter(Kpi_history.kpi_history_id).delete()
    #     db.commit()
    #
    # elif kpi_record and user_record:
    #     # Step 3: Subtract Kpi.price from user's balance
    #     updated_balance = user_record.balance - kpi_record.price
    #
    #     # Step 4: Update the user's balance in the database
    #     stmt = update(Users).where(Users.id == user_id).values(balance=updated_balance)
    #     db.execute(stmt)
    #     db.commit()







