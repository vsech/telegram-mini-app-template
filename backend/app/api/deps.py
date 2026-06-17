from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.security import unauthorized
from app.core.telegram import TelegramInitDataError, validate_telegram_init_data
from app.db.models.user import User
from app.db.session import get_db
from app.services.users import upsert_telegram_user

DbSession = Annotated[AsyncSession, Depends(get_db)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
TelegramInitDataHeader = Annotated[str | None, Header()]


async def get_current_user(
    db: DbSession,
    settings: SettingsDep,
    x_telegram_init_data: TelegramInitDataHeader = None,
) -> User:
    if not x_telegram_init_data:
        raise unauthorized()

    try:
        auth_data = validate_telegram_init_data(
            init_data=x_telegram_init_data,
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            max_age_seconds=settings.TELEGRAM_INIT_DATA_TTL_SECONDS,
        )
    except TelegramInitDataError as exc:
        raise unauthorized() from exc

    return await upsert_telegram_user(db, auth_data.user)
