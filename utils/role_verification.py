from fastapi import HTTPException


def role_verification(user):
    # allowed_functions_for_worker = []
    if user.role == "admin" or user.role == "user":
        return True
    # elif user.role == "user" and function in allowed_functions_for_worker:
    #     return True
    else:
        raise HTTPException(status_code=404, detail='You are not allowed user')