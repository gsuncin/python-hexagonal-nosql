from src.infrastructure.logging.logger import logger
from src.adapters.driven.database.base import get_db
from pymongo import MongoClient


class TestConfig:
    def __init__(
        self,
        use_database: bool = False,
        delete_after_completed: bool = True,
        use_external_auth: bool = False,
        auth_service_url: str = "http://localhost:8000",
        auth_service_user: str = "admin",
        auth_service_password: str = "admin",
    ):
        self.use_database = use_database
        self.delete_after_completed = delete_after_completed
        self.use_external_auth = use_external_auth
        self.auth_service_url = auth_service_url
        self.auth_service_user = auth_service_user
        self.auth_service_password = auth_service_password

    def get_database_connection_pool(self) -> None | MongoClient:
        if self.use_database:
            logger.info("Setting up database connection pool...")
            database = get_db()
            logger.info("Database connection pool established.")
            return database
        return None


class BaseTestSetupConfig:
    def __init__(self, config: TestConfig):
        self.config = config
        self.__setup()

    def __setup(self):
        # Here you can add setup logic based on the config
        database = self.config.get_database_connection_pool()
        if database is not None:
            logger.info("Database connection pool is ready to use.")
        if self.config.use_external_auth:
            logger.info("Setting up external auth service... TODO be implemented")
