from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from . import auth
from .google import directory

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:users']))],
    responses={404: {"description": "Not found"}}
)


@router.get("/{email}")
def get_user_by_email(email):
    user = directory.get_user_by_email(email)
    return JSONResponse(content=user)
