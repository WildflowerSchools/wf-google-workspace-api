from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from . import auth
from .google import directory

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    dependencies=[Depends(auth.JWTBearer(any_scope=['read:groups']))],
    responses={404: {"description": "Not found"}}
)


@router.get("/{group_email}")
def get_group_by_email(group_email):
    group = directory.get_group_by_email(group_email)
    return JSONResponse(content=group)


@router.get("/{group_email}/members")
def get_group_members(group_email):
    group = directory.get_group_by_email(group_email)
    return JSONResponse(content=group['members'])


@router.post("/{group_email}/members/{member_email}", dependencies=[Depends(auth.JWTBearer(any_scope=['edit:groups']))])
def add_member(group_email, member_email):
    response = None
    try:
        response = directory.add_member_to_group(group_email, member_email)
    except directory.errors.HttpError as ex:
        if ex.status_code == 409:
            raise HTTPException(status_code=409, detail="Member already exists in Group")

    return JSONResponse(content=response)


@router.delete("/{group_email}/members/{member_email}",
               dependencies=[Depends(auth.JWTBearer(any_scope=['edit:groups']))])
def delete_member(group_email, member_email):
    try:
        directory.remove_member_from_group(group_email, member_email)
    except directory.errors.HttpError as ex:
        if ex.status_code == 404:
            pass

    return JSONResponse(content=None)
