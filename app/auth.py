from datetime import datetime, timedelta, timezone
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user_model import UserModel
from app.schemas.user_schema import TokenData, User


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def register_user(username: str, password: str, db: Session) -> UserModel:
    errors = []
    if len(username) < 5 or len(username) > 20:
        errors.append('Username length should be >4 and <21')
    if len(password) < 5 or len(password) > 20:
        errors.append('Password length should be >4 and <21')
    if ' ' in username:
        errors.append('Username cannot contain spaces')
    if ' ' in password:
        errors.append('Password cannot contain spaces')
    if len(errors) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='; '.join(errors)
        )
    user = UserModel(
        username=username,
        password_hash=get_password_hash(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(username: str, db: Session):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user == None:
        return None
    return User(username=username, password_hash=user.password_hash)


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        'SECRET_KEY'), algorithm=ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv(
            'SECRET_KEY'), algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user
