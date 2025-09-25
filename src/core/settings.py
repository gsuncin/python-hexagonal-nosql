from decouple import config
from src.adapters.driven.aws.config import instantiate_cloud_client


DEBUG = config("DEBUG", default=False, cast=bool)
VERSION = config("VERSION", default="0.0.1")
# API Config
API_VERSION = config("API_VERSION", default="v1")


# DB Config
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_NAME = config("DATABASE_NAME")

DATABASE_URL = (
    f"mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?authSource=admin"
)

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

# Server Config
TIMEZONE = config("TIMEZONE", default="America/Sao_Paulo")
LOGGER = config("LOGGER", default="logger")


SUPER_USER_EMAIL = config("SUPER_USER_EMAIL", default="superuser@example.com")
SUPER_USER_PASSWORD = config("SUPER_USER_PASSWORD", default="superpassword")

# AWS Config
CLOUD_ACCESS_KEY = config("CLOUD_ACCESS_KEY", default="")
CLOUD_SECRET_KEY = config("CLOUD_SECRET_KEY", default="")
CLOUD_SESSION_TOKEN = config("CLOUD_SESSION_TOKEN", default="")
CLOUD_BUCKET_NAME = config("CLOUD_BUCKET_NAME", default="")
CLOUD_REGION = config("CLOUD_REGION", default="us-east-1")
CLOUD_PROVIDER = config("CLOUD_PROVIDER", default="S3")
CLOUD_ENABLED = config("CLOUD_ENABLED", default=False, cast=bool)

CLOUD_SESSION, CLOUD_CLIENT = instantiate_cloud_client()
