from typing import Annotated
from fastapi import HTTPException, status, Depends

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.exceptions import (
    TokenExpiredException,
    NoJwtException,
    NoUserIdException,
    ForbiddenException,
)
from src.users.dao import UsersDAO
from src.users.models import User
from src.users.utils import get_auth_data, oauth2_scheme


async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=auth_data["algorithm"])
    except ExpiredSignatureError:
        raise TokenExpiredException from None
    except InvalidTokenError:
        raise NoJwtException from None

    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_pk(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_admin_user(current_user: Annotated[User, Depends(verify_token)]):
    if current_user.is_admin:
        return current_user
    raise ForbiddenException
