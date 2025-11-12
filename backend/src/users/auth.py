from passlib.context import CryptContext
from pydantic import EmailStr

from datetime import datetime, timedelta
from src.users.dao import UsersDAO


import jwt

from src.users.utils import get_auth_data

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    return encode_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or verify_password(plain=password, hashed=user.password) is False:
        return None
    return user


def decode_token(token: str):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=auth_data["algorithm"])
        return payload
    except jwt.DecodeError:
        return None
