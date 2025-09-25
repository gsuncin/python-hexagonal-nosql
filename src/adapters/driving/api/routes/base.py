from fastapi import APIRouter, Depends
from typing import Annotated

from src.adapters.driving.api.interface.auth_interface import JWTAuth
from src.adapters.driven.database.repositories.user_repository import UserRepository
from src.application.use_cases.user_use_case import UserUseCases


def get_user_use_case() -> UserUseCases:
    user_repo = UserRepository()
    return UserUseCases(user_repo)


user_use_case = get_user_use_case()
router = APIRouter()
token_jwt = Annotated[str, Depends(user_use_case.verify_access_token)]


@router.get("/health_check", tags=["System"])
async def health_check():
    return {"status_code": 200, "status": "OK", "message": "Health check passed"}
