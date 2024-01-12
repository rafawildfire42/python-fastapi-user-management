from datetime import datetime, timedelta
from typing import Any
from jose import jwt
from pydantic import BaseModel
import logging

from src.apps.users.crud import get_user_by_email
from src.apps.users.models import User
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM, SECRET_KEY, pwd_context

from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer


class RefreshToken(BaseModel):
    refresh_token: str


class Token(RefreshToken):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class AuthUser(BaseModel):
    email: str | None = None
    password: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def raise_http_exception_invalid_email_or_password():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    

def raise_http_exception_while_token_creation(e: Exception):
    logging.error(f"Error during token creation: {e}")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access token is invalid or expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user_and_get_user_id(db, email: str, password: str) -> int:
    user: User | None = get_user_by_email(db, email)
    is_password_valid = verify_password(password, user.password)
    
    if user is None or not is_password_valid:
        raise_http_exception_invalid_email_or_password()
    elif user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to confirm your register first.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user.id


def decode_jwt_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def encode_jwt_token(data: dict[str, Any]) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def create_jwt_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = encode_jwt_token(to_encode)
        return encoded_jwt
    except Exception as e:
        raise_http_exception_while_token_creation(e)
        

def get_access_and_refresh_tokens(data: dict[str, Any]):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data=data, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_jwt_token(
        data=data, expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
