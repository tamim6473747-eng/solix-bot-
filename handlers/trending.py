from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from services.dexscreener import dex_api


async def trending(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await update.message.reply_text("🔍 Fetching trending tokens...")

    try:
        tokens = await dex_api.get_trending(limit=10)

        if not tokens:
            await update.message.reply_text(
                "No trending tokens found."
            )
            return

        message = "<b>🔥 Solix Trending Tokens</b>\n\n"

        for index, pair in enumerate(tokens, start=1):

            base = pair.get("baseToken", {})
            price = pair.get("priceUsd", "N/A")

            volume = pair.get("volume", {}).get("h24", 0)
            liquidity = pair.get("liquidity", {}).get("usd", 0)

            message += (
                f"<b>{index}. {base.get('symbol','Unknown')}</b>\n"
                f"💲 Price: <code>${price}</code>\n"
                f"📊 24H Volume: <code>{dex_api.format_number(volume)}</code>\n"
                f"💧 Liquidity: <code>${dex_api.format_number(liquidity)}</code>\n\n"
            )

        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    except Exception:

        await update.message.reply_text(
            "❌ Failed to fetch trending tokens."
      )
