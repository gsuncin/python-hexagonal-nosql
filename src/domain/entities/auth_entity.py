from pydantic import BaseModel, ConfigDict, field_validator


class TokenData(BaseModel):
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: str
