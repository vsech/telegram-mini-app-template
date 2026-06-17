from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str | None
    photo_url: str | None
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class TelegramAuthRequest(BaseModel):
    init_data: str
