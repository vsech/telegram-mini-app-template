import hashlib
import hmac
import json
from urllib.parse import urlencode

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.telegram import validate_telegram_init_data
from app.main import app

BOT_TOKEN = "123456:TEST_TOKEN"


def build_init_data(payload: dict[str, str], bot_token: str = BOT_TOKEN) -> str:
    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(payload.items())
    )
    secret_key = hmac.new(
        b"WebAppData",
        bot_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    payload_hash = hmac.new(
        secret_key,
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return urlencode({**payload, "hash": payload_hash})


def test_validate_telegram_init_data_accepts_valid_payload() -> None:
    init_data = build_init_data(
        {
            "auth_date": "1700000000",
            "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
            "user": json.dumps(
                {
                    "id": 42,
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "username": "ada",
                    "language_code": "en",
                    "photo_url": "https://example.com/avatar.jpg",
                },
                separators=(",", ":"),
            ),
        }
    )

    auth_data = validate_telegram_init_data(
        init_data=init_data,
        bot_token=BOT_TOKEN,
        max_age_seconds=3600,
        now=1700000100,
    )

    assert auth_data.user.id == 42
    assert auth_data.user.username == "ada"
    assert auth_data.user.first_name == "Ada"
    assert auth_data.user.photo_url == "https://example.com/avatar.jpg"


@pytest.mark.asyncio
async def test_invalid_init_data_is_rejected() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/api/auth/telegram",
            json={"init_data": "user=%7B%22id%22%3A1%7D&hash=invalid"},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_users_me_without_auth_header_returns_401() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/api/users/me")

    assert response.status_code == 401
