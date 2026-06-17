import json
import time

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.test_telegram_auth import build_init_data

# Use the same token as in default settings
TEST_BOT_TOKEN = "123456:TEST_TOKEN"


@pytest.mark.asyncio
async def test_notes_lifecycle() -> None:
    # Use current time to avoid expiration
    now = int(time.time())
    init_data = build_init_data(
        {
            "auth_date": str(now),
            "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
            "user": json.dumps(
                {
                    "id": 42,
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "username": "ada",
                },
                separators=(",", ":"),
            ),
        },
        bot_token=TEST_BOT_TOKEN,
    )
    headers = {"X-Telegram-Init-Data": init_data}

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        # 1. Create a note
        response = await client.post(
            "/api/notes/",
            json={"content": "Test Note Content"},
            headers=headers,
        )
        assert response.status_code == 201
        note_data = response.json()
        assert note_data["content"] == "Test Note Content"
        note_id = note_data["id"]

        # 2. List notes
        response = await client.get("/api/notes/", headers=headers)
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) >= 1
        assert any(n["id"] == note_id for n in notes)

        # 3. Delete the note
        response = await client.delete(f"/api/notes/{note_id}", headers=headers)
        assert response.status_code == 204

        # 4. Verify deletion
        response = await client.get("/api/notes/", headers=headers)
        notes = response.json()
        assert not any(n["id"] == note_id for n in notes)
