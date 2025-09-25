from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src.adapters.driven.database.repositories.user_repository import UserRepository
from src.domain.entities.auth_entity import Token
from src.domain.entities.user_entity import UserAPIEntity
from src.application.use_cases.user_use_case import UserUseCases
from src.adapters.driven.database.base import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.adapters.driving.api.routes.base import token_jwt

router = APIRouter()


def get_user_use_case() -> UserUseCases:
    user_repo = UserRepository()
    return UserUseCases(user_repo)


@router.post("/token", tags=["Authentication"])
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user_use_case = get_user_use_case()
    _user, token, expire = user_use_case.authenticate(
        email=form_data.username, password=form_data.password
    )
    if token is None:
        return {"error": "Invalid credentials"}
    return Token(access_token=token, token_type="bearer", expire=expire.isoformat())


@router.post("/signup", tags=["Authentication"])
async def signup(
    token: token_jwt,
    data: UserAPIEntity,
    db: Session = Depends(get_db),
):
    user_use_case = get_user_use_case()
    user_use_case.create_user(data)
    return {"message": "User created successfully"}

@router.get("/list_users", tags=["Authentication"])
async def read_users_me(token: token_jwt, db: Session = Depends(get_db)):
    user_use_case = get_user_use_case()
    users = user_use_case.list_users()
    return users