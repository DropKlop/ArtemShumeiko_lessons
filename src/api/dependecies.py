from typing import Annotated

from fastapi import Query
from fastapi.params import Depends
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, gt=1, le=3)]

PaginationDep = Annotated[PaginationParams, Depends()]