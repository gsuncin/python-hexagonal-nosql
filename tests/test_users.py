from src.domain.entities.user_entity import UserAPIEntity
from src.adapters.driven.database.repositories.user_repository import UserRepository
from src.application.use_cases.user_use_case import UserUseCases
from tests.base import BaseTestSetupConfig, TestConfig
import unittest


class UserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = TestConfig(use_database=True, delete_after_completed=True)
        cls.setup = BaseTestSetupConfig(config)
        cls.use_cases = cls.__get_use_case()
        cls.created_objects = []

    @classmethod
    def __get_use_case(cls):
        user_repo = UserRepository()
        return UserUseCases(user_repo)

    @classmethod
    def tearDownClass(cls):
        if cls.setup.config.delete_after_completed and cls.setup.config.use_database:
            db = cls.setup.config.get_database_connection_pool()
            if db is not None:
                for obj in cls.created_objects:
                    db.user.delete_one({"id": obj.id})
                print("Cleaned up test database.")

    def test_a_create_user(self):
        user_data = UserAPIEntity(email="test@example.com", password="password123")
        user = self.use_cases.create_user(user_data)
        self.created_objects.append(user)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, user_data.email)
        self.assertTrue(hasattr(user, "id"))

    def test_get_user(self):
        user_data = UserAPIEntity(email="test@example.com", password="password123")
        fetched_user = self.use_cases.get_by_email(user_data.email)
        self.assertIsNotNone(fetched_user)

    def test_authenticate_user(self):
        user_data = UserAPIEntity(email="test@example.com", password="password123")
        user, token, expire = self.use_cases.authenticate(
            user_data.email, user_data.password
        )
        self.assertIsNotNone(user)

    def test_authenticate_user_wrong_password(self):
        """
        It's expected to fail authentication with wrong password.
        """
        user_data = UserAPIEntity(email="test@example.com", password="password123")
        user, token, expire = self.use_cases.authenticate(
            user_data.email, "wrongpassword"
        )
        self.assertIsNone(user)
