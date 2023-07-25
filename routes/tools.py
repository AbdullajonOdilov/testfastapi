import inspect

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import database
from functions.tools import all_tools, create_new_tool, update_tool_r
from models.tools import Tools
from schemas.tools import CreateTools, UpdateTools
from schemas.users import UserCreate
from utils.db_operations import the_one
from utils.login import get_current_active_user
from utils.role_verification import role_verification

tools_router = APIRouter(
    tags=["Tools(dastgohlar) endpoints."]
)



@tools_router.get("/tools")
def get_tools(
        search: str = None,
        id: int = 0,
        page: int = 0,
        limit: int = 10,
        status: bool = None,
        db: Session = Depends(database),

        current_user: UserCreate = Depends(get_current_active_user)):
    role_verification(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page or limit should not be less than 0")
    if id > 0:
        return the_one(id, Tools, db)
    return all_tools(search, page, limit, status, db)


@tools_router.post("/create_tool")
def create_tool(tool: CreateTools,
                current_user: UserCreate = Depends(get_current_active_user),
                db: Session = Depends(database)):
    role_verification(current_user)
    create_new_tool(tool, db, current_user)
    raise HTTPException(status_code=201, detail="New tool created")



@tools_router.put("/update_tool")
def update_tool(
    tool_update: UpdateTools,
    db: Session = Depends(database),
    current_user: UserCreate = Depends(get_current_active_user)
):
    role_verification(current_user)
    update_tool_r(id, tool_update, db)
    raise HTTPException(status_code=200, detail="The tool updated")


# @tools_router.delete("/delete_tools")
# def delete_tool(
#     tool_id: int,
#     current_user: UserCreate = Depends(get_current_active_user),
#     db: Session = Depends(database)
# ):
#     delete_tool_r(current_user,tool_id, db)
#     return {"message": "Tool deleted successfully"}
