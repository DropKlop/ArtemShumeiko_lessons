from typing import Annotated

from fastapi import Query, Request, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from src.database import async_sessionmaker_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, gt=1, le=3)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDeb = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_sessionmaker_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
