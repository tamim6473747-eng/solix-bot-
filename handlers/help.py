from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    message = (
        "📖 <b>Solix Bot Help</b>\n\n"
        "<b>Commands</b>\n\n"
        "🚀 /start\n"
        "Start the bot and show the welcome message.\n\n"
        "📖 /help\n"
        "Show this help message.\n\n"
        "🔥 /trending\n"
        "Show the current trending tokens.\n\n"
        "🔍 /search &lt;token&gt;\n"
        "Example:\n"
        "<code>/search sol</code>\n\n"
        "🪙 /token &lt;contract_address&gt;\n"
        "Example:\n"
        "<code>/token So11111111111111111111111111111111111111112</code>\n"
    )

    await update.message.reply_text(
        message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
