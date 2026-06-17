import argparse
import json
from urllib import request


def main() -> None:
    parser = argparse.ArgumentParser(description="Register Telegram bot commands.")
    parser.add_argument("--token", required=True, help="Telegram bot token")
    args = parser.parse_args()

    payload = json.dumps(
        {
            "commands": [
                {"command": "start", "description": "Open the Mini App"},
                {"command": "help", "description": "Show help"},
            ]
        }
    ).encode("utf-8")

    req = request.Request(
        f"https://api.telegram.org/bot{args.token}/setMyCommands",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=20) as response:
        print(response.read().decode("utf-8"))


if __name__ == "__main__":
    main()
