from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.security import unauthorized
from app.core.telegram import TelegramInitDataError, validate_telegram_init_data
from app.db.session import get_db
from app.schemas.user import TelegramAuthRequest, UserRead
from app.services.users import upsert_telegram_user

router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[AsyncSession, Depends(get_db)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.post("/telegram", response_model=UserRead)
async def auth_telegram(
    payload: TelegramAuthRequest,
    db: DbSession,
    settings: SettingsDep,
) -> UserRead:
    try:
        auth_data = validate_telegram_init_data(
            init_data=payload.init_data,
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            max_age_seconds=settings.TELEGRAM_INIT_DATA_TTL_SECONDS,
        )
    except TelegramInitDataError as exc:
        raise unauthorized() from exc

    return await upsert_telegram_user(db, auth_data.user)
