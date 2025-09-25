from src.adapters.driving.api.interface.auth_interface import JWTAuth
from src.domain.interfaces.user_interface import UserInterface
from src.domain.entities.user_entity import UserAPIEntity
from datetime import datetime, timedelta, timezone
from jose import jwt
from src.core import settings
import pytz
from src.domain.entities.auth_entity import TokenData
from src.infrastructure.logging.logger import logger


class UserUseCases:

    def __init__(self, user_repo: UserInterface):
        self.user_repo = user_repo
        self.auth = JWTAuth()

    def create_user(self, user: UserAPIEntity):
        user.password = self.auth.pwd_crypt.hash(user.password)
        return self.user_repo.create_obj(user)

    def get_user(self, user_id: str) -> UserAPIEntity:
        return self.user_repo.get(user_id)

    def update_user(self, user: UserAPIEntity):
        return self.user_repo.update(user)

    def delete_user(self, user_id: str):
        self.user_repo.delete(user_id)

    def list_users(self) -> list[UserAPIEntity]:
        return self.user_repo.list_all()

    def filter_users(self, syntax):
        return self.user_repo.filter_obj(syntax)

    def get_by_email(self, email: str) -> UserAPIEntity:
        return self.user_repo.get_by_email(email)

    def authenticate(self, email: str, password: str) -> UserAPIEntity:
        _user = self.get_by_email(email)
        if not _user:
            logger.error("User not found")
        if len(_user) >= 1:
            _user = _user[0]
        if not self.auth.pwd_crypt.verify(password, _user.password):
            logger.error("Invalid password")
            return None, None, None
        token, expire = self.auth.create_access_token(email=email)
        return _user, token, expire

    def refresh_token(self, token: str) -> str:
        return self.user_repo.refresh_token(token)

    def create_access_token(self, email: str) -> str:
        expires_delta = timedelta(minutes=50)
        expire = datetime.now(tz=timezone.utc) + expires_delta
        to_encode = {"sub": email, "exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt, expire.astimezone(pytz.timezone("America/Sao_Paulo"))

    def verify_access_token(self, token: str) -> UserAPIEntity:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")

            if email is None:
                logger.error("Email not found in token")
            token_data = TokenData(email=email)

        except Exception as exc:
            logger.error(exc)

        user = self.get_by_email(email)

        if user is None:
            logger.error("User not found")
            return None

        if len(user) >= 1:
            user = user[0]

        if not user.is_active:
            logger.error("Inactive user")
            return None

        return user
