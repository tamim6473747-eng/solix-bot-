import logging

from telegram.ext import (
    Application,
    CommandHandler,
)

from config import BOT_TOKEN

from handlers.start import start
from handlers.help import help_command
from handlers.trending import trending
from handlers.search import search
from handlers.token import token

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.exception(
        "Unhandled exception",
        exc_info=context.error,
    )

    if update and getattr(update, "effective_message", None):
        await update.effective_message.reply_text(
            "⚠️ An unexpected error occurred.\nPlease try again later."
        )


def create_application() -> Application:
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    app.add_handler(
        CommandHandler(
            "trending",
            trending,
        )
    )

    app.add_handler(
        CommandHandler(
            "search",
            search,
        )
    )

    app.add_handler(
        CommandHandler(
            "token",
            token,
        )
    )

    app.add_error_handler(error_handler)

    return app
  def main() -> None:
    logger.info("Starting Solix Telegram Bot...")

    app = create_application()

    app.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
