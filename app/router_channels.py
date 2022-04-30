from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from . import auth
from .google import directory
from .models.watch import DeleteWatch

router = APIRouter(
    prefix="/channels",
    tags=["Channels"],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:users']))],
    responses={404: {"description": "Not found"}}
)


@router.delete("/")
def delete_watch(payload: DeleteWatch):
    response = directory.delete_watch(payload.uuid, payload.resource_id)
    return JSONResponse(content=response)
