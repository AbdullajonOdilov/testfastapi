from fastapi import HTTPException

from models.users import Users
from utils.db_operations import save_in_db, the_one
from utils.login import get_password_hash
from utils.pagination import pagination


def all_users(search, page, limit, status, db):
    users = db.query(Users)

    if search:
        users = users.filter(Users.username.ilike(f"%{search}%"))
    elif status is True:
        users = users.filter(Users.status==True)
    elif status is False:
        users = users.filter(Users.status==False)
    users = users.order_by(Users.id.desc())
    return pagination(users, page, limit)


def create_new_user(form, db):
    if db.query(Users).filter(Users.username == form.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if form.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Role error!")
    password_hash = get_password_hash(form.password)
    new_user_db = Users(
        name=form.name,
        username=form.username,
        password=form.password,
        password_hash=password_hash,
        role=form.role,
        status=form.status,
        balance=0,
        token="",
    )
    save_in_db(db, new_user_db)


def update_user_r(form, db):
    the_one(form.id, Users, db)
    if db.query(Users).filter(Users.username == form.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if form.role != "admin" and form.role != "user":
        raise HTTPException(status_code=400, detail="Role error!")
    password_hash = get_password_hash(form.password)
    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password: form.password,
        Users.password_hash: password_hash,
        Users.role: form.role,
        Users.status: form.status,
    })
    db.commit()
