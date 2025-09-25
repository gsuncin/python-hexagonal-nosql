import boto3
from src.infrastructure.logging.logger import logger
from src.core import settings


def instantiate_cloud_client() -> tuple[boto3.Session, boto3.client]:
    if not settings.CLOUD_ENABLED:
        return None, None
    if settings.CLOUD_PROVIDER != "S3":
        logger.error("Unsupported cloud provider")
        return None, None
    session = boto3.Session(
        aws_access_key_id=settings.CLOUD_ACCESS_KEY,
        aws_secret_access_key=settings.CLOUD_SECRET_KEY,
        aws_session_token=settings.CLOUD_SESSION_TOKEN,
        region_name=settings.CLOUD_REGION,
    )
    s3_client = session.client("s3")
    return session, s3_client
