from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserAPIEntity(BaseModel):
    id: str | None = None
    email: str
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_active: bool | None = None

    class Config:
        from_attributes = True
        validate_assignment = True
        model_config = ConfigDict(populate_by_name=True)
