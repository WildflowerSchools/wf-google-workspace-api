from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from . import auth
from .google import directory
from .models.watch import CreateWatch

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:users']))],
    responses={404: {"description": "Not found"}}
)


@router.get("/{email}")
def get_user_by_email(email: str):
    user = directory.get_user_by_email(email)
    return JSONResponse(content=user)


@router.post("/watch")
def create_user_watch(payload: CreateWatch):
    watch = directory.create_user_watch(uuid=payload.uuid, url=payload.url, token=payload.token, ttl=payload.ttl)
    return JSONResponse(content=watch)
