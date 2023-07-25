import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.material_type import all_materials, create_new_material, update_material_r
from models.material_type import Material_type
from schemas.material_type import CreateMaterial, UpdateMaterial
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

material_router = APIRouter(
    tags=["Material_type endpoints"]
)


@material_router.get("/materials")
def get_material_type(
    search: str = None,
    id: int = 0,
    page: int = 0,
    limit: int = 10,
    db: Session = Depends(database),
    current_user: UserCreate = Depends(get_current_active_user),
):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Material_type, db)
    return all_materials(search, page, limit, db)


@material_router.post("/create_material")
def create_material(material: CreateMaterial,
                   current_user: UserCreate = Depends(get_current_active_user),
                   db: Session = Depends(database)):
    role_verification(current_user)
    create_new_material(material, db, current_user)
    raise HTTPException(status_code=201, detail="New material created")

@material_router.put("/update_material")
def update_material(material_update: UpdateMaterial,
                    current_user: UserCreate = Depends(get_current_active_user),
                    db: Session = Depends(database)):
    role_verification(current_user)
    update_material_r(material_update, db, current_user)
    raise HTTPException(status_code=200, detail="The material updated")

