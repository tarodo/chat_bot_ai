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


def dialogflow_answer(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    response = detect_intent_text(
        PROJECT_ID, update.effective_user.id, update.message.text
    )
    if response:
        update.message.reply_text(response)


def main(bot_token) -> None:
    """Start the bot."""
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, dialogflow_answer)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    logger = get_logger("tg_bot", os.getenv("BOT_REPORT_TOKEN"), os.getenv("CHAT_ID"))
    bot_token = os.environ["BOT_TOKEN"]
    PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]
    main(bot_token)
