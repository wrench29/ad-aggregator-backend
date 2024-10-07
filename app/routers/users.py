from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user_schema import CreateUser, Token, User
from app import auth


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(auth.get_current_user)],
):
    return current_user.username


@router.post("/register")
async def register_new_user(user: CreateUser, db: Session = Depends(get_db)):
    auth.register_user(user.username, user.password, db)
