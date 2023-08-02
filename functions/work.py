from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

# from functions.work_history import create_new_work_history
from functions.work_history import create_new_work_history
from models.homes import Homes
from models.kpi import Kpi
from models.material_type import Material_type
from models.proces import Process
from models.tools import Tools
from models.toquvchilar import Weavers
from models.users import Users
from models.work import Work
from models.work_history import Work_history
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_work(search, page, limit, db):
    works = db.query(Work).options(joinedload(Work.proces).load_only(Process.name),
                                   joinedload(Work.material_type).load_only(Material_type.name))
    if search:
        works = db.query(Material_type).filter(Material_type.name.ilike(f"%{search}%"))
    works = works.order_by(Work.id.desc())
    return pagination(works, page, limit)


def create_new_work(form, thisuser, db):
    the_one(form.material_type_id, Material_type, db)
    work1 = db.query(Work).filter(Work.material_type_id == form.material_type_id).first()
    if work1:
        process1 = db.query(Process).filter(Process.id == work1.process_id).first()
        process2 = db.query(Process).filter(Process.step == (process1.step + 1)).first()
        process_id = process2.id
        process = process1
    else:
        process = db.query(Process).filter(Process.step == 1, Process.material_type_id == form.material_type_id).first()
        process_id = process.id
        # process = db.query(Process).filter(Process.material_type_id == form.material_type_id).first()
    if process.connection in ['admin', 'user']:
        the_one(form.connection_id, Users, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        db.query(Users).filter(Users.id == form.connection_id).update({
            Users.balance: Users.balance + kpi.price
        })
        db.commit()
    elif process.connection == 'home':
        the_one(form.connection_id, Homes, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        db.query(Homes).filter(Homes.id == form.connection_id).update({
            Homes.balance: Homes.balance + kpi.price
        })
        db.commit()
    elif process.connection == 'weaver':
        the_one(form.connection_id, Weavers, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        weaver = db.query(Weavers).filter(Weavers.id == form.connection_id).first()
        if weaver:
            new_balance = weaver.balance + kpi.price
            db.query(Weavers).filter(Weavers.id == form.connection_id).update({
                Weavers.balance: new_balance
            })
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Weaver not found")
    if process.connection in ['draw', 'tool']:
        the_one(form.connection_id, Users, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        db.query(Users).filter(Users.id == form.connection_id).update({
            Users.balance: Users.balance + kpi.price
        })
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Invalid connection_id")

    new_work = Work(
        material_type_id=form.material_type_id,
        connection_id=form.connection_id,
        process_id=process_id,
        user_id=thisuser.id,
        comment=form.comment
    )
    save_in_db(db, new_work)
    kpi = db.query(Kpi).filter(Kpi.proces_id==process_id).first()
    if kpi:
        money = kpi.price
    else:
        raise HTTPException(status_code=400, detail="Kpi not found for process")

    create_new_work_history(
        work_id=new_work.id,
        money=money,
        date=datetime.now(),
        status=True,
        db=db
    )


def delete_work_r(id, db):
    work = the_one(id, Work, db)
    process = db.query(Process).filter(Process.material_type_id == work.material_type_id).all()
    step = len(process)

    if step == 1:
        db.query(Work).filter(Work.id == id).delete()
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="You cannot delete this work")

    db.query(Work_history).filter(Work_history.work_id == work.id).delete()
    db.commit()
    # delete balance
    process_id = work.process_id
    process = db.query(Process).filter(Process.id == process_id).first()
    if process.connection in ['admin', 'user']:
        the_one(work.connection_id, Users, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        db.query(Users).filter(Users.id == work.connection_id).update({
            Users.balance: Users.balance - kpi.price
        })
        db.commit()
    elif process.connection == 'home':
        the_one(work.connection_id, Homes, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        db.query(Homes).filter(Homes.id == work.connection_id).update({
            Homes.balance: Homes.balance - kpi.price
        })
        db.commit()
    elif process.connection == 'weaver':
        the_one(work.connection_id, Weavers, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        weaver = db.query(Weavers).filter(Weavers.id == work.connection_id).first()
        if weaver:
            new_balance = weaver.balance - kpi.price
            db.query(Weavers).filter(Weavers.id == work.connection_id).update({
                Weavers.balance: new_balance
            })
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Weaver not found")

    elif process.connection in ['tool', 'draw']:
        the_one(work.connection_id, Users, db)
        kpi = db.query(Kpi).filter(Kpi.proces_id == process_id).first()
        db.query(Users).filter(Users.id == work.connection_id).update({
            Users.balance: Users.balance - kpi.price
        })
        db.commit()

    else:
        raise HTTPException(status_code=400, detail="Invalid connection_id")





