import os
from dotenv import load_dotenv

# Load environment variables from .env (local development)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEXSCREENER_BASE_URL = "https://api.dexscreener.com/latest"

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is missing! Please set BOT_TOKEN in your .env file or Render Environment Variables."
    )
