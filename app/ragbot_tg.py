import os, logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler
)
from bot_handlers import (
    start, main_menu, handle_question
)
from bot_config import (
    MAIN_MENU, ASK_QUESTION, logger
)

def main():
    TOKEN = os.getenv("TG_TOKEN")
    if not TOKEN:
        logger.error("Telegram token not found!")
        raise RuntimeError("Telegram token is missing")

    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            ASK_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)

    logger.info("Starting bot...")
    application.run_polling()


if __name__ == '__main__':
    main()