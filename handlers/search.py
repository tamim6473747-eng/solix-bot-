from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from services.dexscreener import dex_api


async def search(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/search <token name>\n\nExample:\n/search sol"
        )
        return

    query = " ".join(context.args)

    await update.message.reply_text("🔍 Searching...")

    try:
        pairs = await dex_api.search_pairs(query)

        if not pairs:
            await update.message.reply_text(
                "❌ No matching token found."
            )
            return

        message = f"<b>Search Results for:</b> <code>{query}</code>\n\n"

        for pair in pairs[:5]:

            base = pair.get("baseToken", {})
            quote = pair.get("quoteToken", {})

            message += (
                f"<b>{base.get('symbol','Unknown')}</b>\n"
                f"Name: {base.get('name','Unknown')}\n"
                f"Chain: {pair.get('chainId','Unknown')}\n"
                f"DEX: {pair.get('dexId','Unknown')}\n"
                f"Price: <code>${pair.get('priceUsd','N/A')}</code>\n"
                f"Pair: {base.get('symbol','?')}/{quote.get('symbol','?')}\n\n"
            )

        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    except Exception:
        await update.message.reply_text(
            "❌ Search failed."
          )
