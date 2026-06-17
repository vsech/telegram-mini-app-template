from __future__ import annotations

import os

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123456:TEST_TOKEN")
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+aiosqlite:////tmp/telegram-mini-app-template-test.db",
)

import pytest_asyncio

from app.db.base import Base
from app.db.session import engine


@pytest_asyncio.fixture(autouse=True)
async def test_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
