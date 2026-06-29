# 🚀 Solix Telegram Bot

A Telegram bot built with Python and python-telegram-bot v21 that uses the DexScreener API to search tokens and display market information.

## Features

- /start
- /help
- /trending
- /search <token>
- /token <contract_address>

## Requirements

- Python 3.11+
- Telegram Bot Token
- GitHub
- Render

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
BOT_TOKEN=YOUR_BOT_TOKEN
```

Run:

```bash
python bot.py
```

## Deploy

1. Push to GitHub.
2. Create a new Web Service on Render.
3. Connect your GitHub repository.
4. Build Command:

```bash
pip install -r requirements.txt
```

5. Start Command:

```bash
python bot.py
```

6. Add Environment Variable:

```
BOT_TOKEN=YOUR_BOT_TOKEN
```

## License

MIT
