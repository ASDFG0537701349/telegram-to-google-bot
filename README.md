# telegram-to-google-bot

Forwards Telegram messages (text + photos) to Google Chat.

## Setup

1. Clone and install:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

2. Configure environment variables (see `.env.example`):
```bash
cp .env.example .env
# Edit .env with your values
```

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_TOKEN` | Yes | Telegram Bot API token |
| `GOOGLE_CHAT_WEBHOOK` | Yes | Google Chat incoming webhook URL |
| `PORT` | No | Health server port (default: 5000) |
| `LOG_LEVEL` | No | Log level (default: INFO) |

## Run

```bash
python -m src.main
```

## Test

```bash
pytest
pytest --cov=src --cov-report=term-missing
```

## Lint

```bash
ruff check src/ tests/
```
