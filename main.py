import logging
import os

from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from google.cloud import dialogflow

logger = logging.getLogger("homework")
logger.setLevel(logging.DEBUG)

strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)

handler_st = logging.StreamHandler()
handler_st.setFormatter(formatter)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте',
    )


def detect_intent_text(project_id, session_id, text, language_code="ru") -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    response = detect_intent_text("bot-speach-dvmn", update.effective_user.id, update.message.text)
    update.message.reply_text(response)


def main(bot_token) -> None:
    """Start the bot."""
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    main(BOT_TOKEN)
