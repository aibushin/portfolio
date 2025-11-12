from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import APIRouter, Cookie, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from datetime import timedelta
from src.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from src.users.auth import (
    create_token,
    decode_token,
    get_password_hash,
    authenticate_user,
)
from src.users.dao import UsersDAO
from src.users.dependencies import get_current_admin_user, verify_token
from src.users.models import User
from src.users.schemas import RefreshRequest, SUserRegister, SUserAuth
from src.users.utils import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.dict()
    user_dict["password"] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login/")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(email=form_data.username, password=form_data.password)
    if user is None:
        raise IncorrectEmailOrPasswordException

    access_token = create_token(
        {"sub": str(user.id)}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": str(user.id), "type": "refresh"}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # HttpOnly refresh_token
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, samesite="lax", secure=False
    )

    # обычная access_token cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=False,  # JS может читать
        samesite="lax",
        secure=False,
    )

    return {"access_token": access_token}


@router.post("/refresh/")
def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),  # берём токен из куки
):
    # def refresh_token(data: RefreshRequest):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_token(
        {"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": new_access_token}


@router.post("/logout/")
async def logout(response: Response):
    return {"message": "Пользователь успешно вышел из системы"}


@router.get("/me/")
async def me(user_data: Annotated[User, Depends(verify_token)]):
    return user_data


@router.get("/all_users/")
async def all_users(user_data: Annotated[User, Depends(get_current_admin_user)]):
    return await UsersDAO.find_all()
