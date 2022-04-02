import os

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from log_config import get_logger
from dialogflow_connect import detect_intent_text


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf"Здравствуйте",
    )


def send_answer(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    response = detect_intent_text(
        update.effective_user.id, update.message.text
    )
    response_text = update.message.text
    if response:
        response_text = response

    update.message.reply_text(response_text)


def main() -> None:
    """Start the bot."""
    bot_token = os.environ["TG_BOT_TOKEN"]
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, send_answer)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    logger = get_logger("tg_bot", os.getenv("BOT_REPORT_TOKEN"), os.getenv("TG_ADMIN_CHAT_ID"))

    main()
