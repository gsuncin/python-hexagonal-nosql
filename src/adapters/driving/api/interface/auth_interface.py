from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt
import pytz
from src.core import settings
from src.domain.entities.auth_entity import TokenData
from src.domain.entities.user_entity import UserAPIEntity
from src.adapters.driven.database.repositories.generic_repository import GenericORM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTAuth:
    pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_access_token(cls, email: str):
        """
        @email: {"email": "$user.email"}
        returns Bearer Token for auth and expire
        """
        expires_delta = timedelta(minutes=50)
        expire = datetime.now(tz=timezone.utc) + expires_delta
        to_encode = {"sub": email, "exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt, expire.astimezone(pytz.timezone("America/Sao_Paulo"))

    @classmethod
    def verify_access_token(cls, token: Annotated[str, Depends(oauth2_scheme)]):
        """
        @data: {"email": "$user.email}
        @expires_delta: datetime.timedelta object
        returns Bearer Token for auth
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:

            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except Exception as exc:
            print(exc)
            raise credentials_exception
        user = cls.get_user(email)
        if user is None or not user.is_active:
            raise credentials_exception
        return user

    @classmethod
    def get_user(cls, email: str):
        users = cls.find_all(UserAPIEntity)
        for user in users:
            if email in user["email"]:
                return UserAPIEntity(**user)

    @classmethod
    def login(cls, form_data):
        user_dict = GenericORM.find_by_id(form_data.email)
        if not user_dict:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        user = UserAPIEntity(**user_dict)
        hashed_password = JWTAuth.pwd_crypt.verify(form_data.password, user.password)
        if not hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        token, expire = JWTAuth.create_access_token(user.email)
        return {"access_token": token, "token_type": "bearer", "expire": expire}
