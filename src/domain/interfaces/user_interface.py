from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.user_entity import UserAPIEntity


class UserInterface(ABC):
    @abstractmethod
    def create_obj(self, user: UserAPIEntity) -> UserAPIEntity: ...

    @abstractmethod
    def list_all(self) -> List[UserAPIEntity]: ...

    @abstractmethod
    def get(self, user_id: str) -> UserAPIEntity: ...

    @abstractmethod
    def get_by_email(self, email: str) -> UserAPIEntity: ...

    @abstractmethod
    def update(self, user: UserAPIEntity) -> UserAPIEntity: ...

    @abstractmethod
    def delete(self, user_id: str) -> bool: ...

    @abstractmethod
    def filter_obj(self, syntax) -> List[UserAPIEntity]: ...

    @abstractmethod
    def authenticate(self, email: str, password: str) -> UserAPIEntity: ...

    @abstractmethod
    def refresh_token(self, token: str) -> str: ...

    @abstractmethod
    def create_access_token(self, email: str) -> str: ...

    @abstractmethod
    def verify_access_token(self, token: str) -> UserAPIEntity: ...

    @abstractmethod
    def to_dict(self) -> dict: ...
