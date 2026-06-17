from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.telegram import TelegramUserData
from app.db.models.user import User


async def get_user_by_telegram_id(
    db: AsyncSession,
    telegram_id: int,
) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def upsert_telegram_user(
    db: AsyncSession,
    telegram_user: TelegramUserData,
) -> User:
    user = await get_user_by_telegram_id(db, telegram_user.id)
    if user is None:
        user = User(telegram_id=telegram_user.id)
        db.add(user)

    user.username = telegram_user.username
    user.first_name = telegram_user.first_name
    user.last_name = telegram_user.last_name
    user.language_code = telegram_user.language_code
    user.photo_url = telegram_user.photo_url
    user.is_active = True

    await db.commit()
    await db.refresh(user)
    return user
