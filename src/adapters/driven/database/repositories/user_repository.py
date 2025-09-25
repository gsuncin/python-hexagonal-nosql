from src.domain.entities.user_entity import UserAPIEntity
from src.adapters.driven.database.repositories.generic_repository import GenericORM


class UserRepository(GenericORM):
    __collection__ = "user"

    @classmethod
    def create_obj(cls, user: UserAPIEntity) -> UserAPIEntity:
        return cls.create(user, UserAPIEntity)

    @classmethod
    def list_all(cls) -> list[UserAPIEntity]:
        return cls.find_all(UserAPIEntity)

    @classmethod
    def get(cls, user_id: str) -> UserAPIEntity:
        return cls.find_by_id(user_id, UserAPIEntity)

    @classmethod
    def get_by_email(cls, email: str) -> UserAPIEntity:
        return cls.filter_obj({"email": email})

    @classmethod
    def update(cls, user: UserAPIEntity) -> UserAPIEntity:
        return cls.save(user, UserAPIEntity)

    @classmethod
    def delete(cls, user_id: str) -> None:
        cls.delete_by_id(user_id)

    @classmethod
    def filter_obj(cls, syntax):
        return cls.filter(syntax, UserAPIEntity)
