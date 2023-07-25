import os
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from models.draws import Draws
from utils.db_operations import save_in_db, the_one
from utils.pagination import pagination


def all_draws(search, page, limit, status, db):
    draws = db.query(Draws).options(joinedload(Draws.user))
    if search:
        search_filter = Draws.name.ilike(f"%{search}%")
    else:
        search_filter = Draws.id > 0
    if status is True:
        status_filter = Draws.status = True
    elif status is False:
        status_filter = Draws.status = False
    else:
        status_filter = Draws.id > 0
    draws = draws.filter(search_filter, status_filter).order_by(Draws.id.asc())
    return pagination(draws, page, limit)


def create_new_draw(name, status, db, thisuser, file):
    if db.query(Draws).filter(Draws.name == name).first():
        raise HTTPException(status_code=400, detail="Draw already exists")

    if file:
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpeg", ".png", ".jpg", ".svg"]:
            raise HTTPException(status_code=400, detail="The file format cannot macht!")
        with open(f"upload_files/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        new_draw_db = Draws(
            name=name,
            status=status,
            file=file.filename,
            user_id=thisuser.id
        )
        save_in_db(db, new_draw_db)
    else:
        new_draw_db = Draws(
            name=name,
            status=status,
            file="",
            user_id=thisuser.id
        )
        save_in_db(db, new_draw_db)


def update_draw_r(id, name, status, db, thisuser, file):
    the_one(id, Draws, db)
    if db.query(Draws).filter(and_(Draws.name == name, Draws.file == file, Draws.status == status)).first():
        raise HTTPException(status_code=400, detail="Draw already exists")
    draw = db.query(Draws).filter(Draws.id == id).first()
    if not draw:
        raise HTTPException(status_code=404, detail="Draw not found")

    # Check if a new file is provided
    if file:
        # Save the new file and update the "file" attribute
        file_location = file.filename
        ext = os.path.splitext(file_location)[-1].lower()
        if ext not in [".jpeg", ".png", ".jpg", ".svg"]:
            raise HTTPException(status_code=400, detail="The file format does not match!")
        os.unlink(f"upload_files/{draw.file}")
        with open(f"upload_files/{file_location}", "wb+") as file_object:
            file_object.write(file.file.read())
        file_name = file.filename
    else:
        # Keep the existing file name
        file_name = draw.file
    draw.name = name
    draw.status = status
    draw.user_id = thisuser.id
    draw.file = file_name  # Update the "file" attribute with the new/unchanged file name

    db.commit()



