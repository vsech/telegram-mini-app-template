import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qsl


class TelegramInitDataError(ValueError):
    pass


@dataclass(frozen=True)
class TelegramUserData:
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    photo_url: str | None = None


@dataclass(frozen=True)
class TelegramAuthData:
    auth_date: int
    user: TelegramUserData
    raw: dict[str, str]


def validate_telegram_init_data(
    init_data: str,
    bot_token: str,
    max_age_seconds: int,
    now: int | None = None,
) -> TelegramAuthData:
    if not init_data or not bot_token or bot_token == "change-me":
        raise TelegramInitDataError("Invalid init data")

    parsed = dict(parse_qsl(init_data, keep_blank_values=True, strict_parsing=False))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise TelegramInitDataError("Invalid init data")

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(parsed.items())
    )

    # Telegram WebApp validation uses HMAC(bot_token, key="WebAppData") as the
    # secret key for the second HMAC over the sorted data_check_string.
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise TelegramInitDataError("Invalid init data")

    auth_date_raw = parsed.get("auth_date")
    if not auth_date_raw:
        raise TelegramInitDataError("Invalid init data")

    try:
        auth_date = int(auth_date_raw)
    except ValueError as exc:
        raise TelegramInitDataError("Invalid init data") from exc

    current_time = int(time.time()) if now is None else now
    if current_time - auth_date > max_age_seconds:
        raise TelegramInitDataError("Invalid init data")

    user = _parse_user(parsed.get("user"))
    return TelegramAuthData(auth_date=auth_date, user=user, raw=parsed)


def _parse_user(user_raw: str | None) -> TelegramUserData:
    if not user_raw:
        raise TelegramInitDataError("Invalid init data")

    try:
        user_payload: dict[str, Any] = json.loads(user_raw)
    except json.JSONDecodeError as exc:
        raise TelegramInitDataError("Invalid init data") from exc

    telegram_id = user_payload.get("id")
    if not isinstance(telegram_id, int):
        raise TelegramInitDataError("Invalid init data")

    return TelegramUserData(
        id=telegram_id,
        username=_optional_str(user_payload.get("username")),
        first_name=_optional_str(user_payload.get("first_name")),
        last_name=_optional_str(user_payload.get("last_name")),
        language_code=_optional_str(user_payload.get("language_code")),
        photo_url=_optional_str(user_payload.get("photo_url")),
    )


def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
