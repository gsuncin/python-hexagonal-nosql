import sys
import os

sys.path.append(os.getcwd())

from src.core import settings
from src.adapters.driven.database.repositories.user_repository import UserRepository
from src.application.use_cases.user_use_case import UserUseCases
from src.domain.entities.user_entity import UserAPIEntity
from src.infrastructure.logging.logger import logger


def create_super_user():
    """
    Creates a super user in the database if it does not already exist.
    To run this script, you can simply copy and paste this code in a python shell
    """
    user_repo = UserRepository()
    user_use_case = UserUseCases(user_repo)

    super_user_email = settings.SUPER_USER_EMAIL
    super_user_password = settings.SUPER_USER_PASSWORD

    existing_user = user_use_case.get_by_email(super_user_email)

    if existing_user:
        logger.info(f"Super user with email {super_user_email} already exists.")
        return

    super_user = UserAPIEntity(
        email=super_user_email, password=super_user_password, is_active=True
    )

    created_user = user_use_case.create_user(super_user)
    logger.info(f"Super user created with email: {created_user.email}")


if __name__ == "__main__":
    create_super_user()