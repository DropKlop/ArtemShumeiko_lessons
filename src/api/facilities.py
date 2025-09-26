from fastapi import APIRouter

import json

from src.api.dependecies import DBDep
from src.schemas.facilities import FacilitiesAdd

from fastapi_cache.decorator import cache

from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
#@cache(expire=10)
async def get_facilities(
        db: DBDep
):
    facilities = await db.facilities.get_all()
    return {"status": "OK", "data": facilities}

@router.post("")
async def add_facilities(
        db:DBDep,
        facilities_data: FacilitiesAdd
):
    facilities = await db.facilities.add_(facilities_data)
    await db.commit()

    test_task.delay()

    return {"status":"OK", "data":facilities}
