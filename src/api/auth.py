from fastapi import APIRouter, HTTPException, Response

from src.api.dependecies import UserIdDeb, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    user = await db.users.get_one(email=data.email)
    if user:
        raise HTTPException(
            status_code=409, detail="Пользователь с данным email уже существует"
        )
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add_(new_user_data)
    await db.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(
            status_code=401, detail="Пользователь с таким email не зарегистрирован"
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/me")
async def get_me(db: DBDep, user_id: UserIdDeb):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
