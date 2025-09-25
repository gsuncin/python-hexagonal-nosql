from datetime import datetime
from pydantic import BaseModel, ConfigDict


class VideoEntity(BaseModel):
    id: str | None = None
    external_id: str | None = None
    email_user: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_processed: bool | None = False
    status: str | None = None  # pending, processing, completed, failed
    video_input: str | None = None  # S3 path or local path
    processed_output: str | None = None  # zip/tar.gz path
    error_message: str | None = None
    frame_amount: int | None = 0
    quality: str | None = "2"

    class Config:
        from_attributes = True
        validate_assignment = True
        model_config = ConfigDict(populate_by_name=True)

