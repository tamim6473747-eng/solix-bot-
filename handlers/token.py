from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from services.dexscreener import dex_api


async def token(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/token <contract_address>"
        )
        return

    address = context.args[0]

    await update.message.reply_text("🔍 Fetching token details...")

    try:
        pairs = await dex_api.get_token_pairs(address)

        if not pairs:
            await update.message.reply_text(
                "❌ Token not found."
            )
            return

        pair = dex_api.best_pair(pairs)

        if not pair:
            await update.message.reply_text(
                "❌ No trading pair found."
            )
            return

        base = pair.get("baseToken", {})
        quote = pair.get("quoteToken", {})
        liquidity = pair.get("liquidity", {}).get("usd", 0)
        volume = pair.get("volume", {}).get("h24", 0)

        message = (
            f"🪙 <b>{base.get('name', 'Unknown')}</b>\n\n"
            f"Symbol: <code>{base.get('symbol', 'N/A')}</code>\n"
            f"Chain: <code>{pair.get('chainId', 'Unknown')}</code>\n"
            f"DEX: <code>{pair.get('dexId', 'Unknown')}</code>\n"
            f"Price: <code>${pair.get('priceUsd', 'N/A')}</code>\n"
            f"Liquidity: <code>${dex_api.format_number(liquidity)}</code>\n"
            f"24H Volume: <code>${dex_api.format_number(volume)}</code>\n"
            f"Pair: <code>{base.get('symbol', '?')}/{quote.get('symbol', '?')}</code>\n"
            f"Contract:\n<code>{address}</code>"
        )

        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    except Exception:
        await update.message.reply_text(
            "❌ Failed to fetch token details."
                                             )
