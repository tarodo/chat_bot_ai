import os

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from common import get_logger


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf"Здравствуйте",
    )


def detect_intent_text(project_id, session_id, text, language_code="ru") -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


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
