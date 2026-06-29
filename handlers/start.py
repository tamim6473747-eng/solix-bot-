from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "🚀 <b>Welcome to Solix Bot</b>\n\n"
        "Track Solana & multi-chain tokens with DexScreener.\n\n"
        "<b>Available Commands:</b>\n"
        "• /help - Show all commands\n"
        "• /trending - View trending tokens\n"
        "• /search <token> - Search a token\n"
        "• /token <contract_address> - Get token details\n\n"
        "Built with ❤️ using DexScreener API."
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
