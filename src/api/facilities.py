from fastapi import APIRouter
from typing import Optional

from fastapi.params import Query
from sqlalchemy.util import await_only

from src.api.dependecies import DBDep
from src.schemas.facilities import Facilities, FacilitiesAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(
        db: DBDep
):
    facilities = await db.facilities.get_all()
    return {"status":"OK", "data":facilities}

@router.post("")
async def add_facilities(
        db:DBDep,
        facilities_data: FacilitiesAdd
):
    facilities = await db.facilities.add_(facilities_data)
    await db.commit()
    return {"status":"OK", "data":facilities}
