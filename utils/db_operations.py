from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base


def get_in_db(
        db: Session,
        model,
        ident: int
):
    obj = db.query(model).get(ident)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No such {model} exists in the database"
        )
    return obj


def save_in_db(
        db: Session,
        obj: Base
):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_in_db(
        db: Session,
        obj: Base
):
    db.commit()
    db.refresh(obj)
    return obj


def the_one(id, model, db):
    the_one = db.query(model).filter(model.id == id).first()
    if not the_one:
        raise HTTPException(status_code=400, detail=f"No such {model} exists in the database")
    return the_one


