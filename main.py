import logging
import os

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from google.cloud import dialogflow


class MyLogsHandler(logging.Handler):
    def __init__(self, tg_token: str, chat_id: str):
        super().__init__()
        self.token = tg_token
        self.chat_id = chat_id

    def emit(self, record):
        log_bot = Bot(token=self.token)
        log_bot.send_message(self.chat_id, self.format(record))


def get_logger(logger_name, bot_reporter_token, chat_id):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)

    handler_st = logging.StreamHandler()
    handler_st.setFormatter(formatter)

    if bot_reporter_token and chat_id:
        strfmt = "%(asctime)s :: %(levelname)s :: %(message)s"
        datefmt = "%d.%m %H:%M:%S"
        formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)

        handler_tg = MyLogsHandler(bot_reporter_token, chat_id)
        handler_tg.setFormatter(formatter)

        logger.addHandler(handler_st)
        logger.addHandler(handler_tg)

    return logger


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

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def dialogflow_answer(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    response = detect_intent_text(PROJECT_ID, update.effective_user.id, update.message.text)
    if response:
        update.message.reply_text(response)


def main(bot_token) -> None:
    """Start the bot."""
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dialogflow_answer))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    logger = get_logger("tg_bot", os.getenv("BOT_REPORT_TOKEN"), os.getenv("CHAT_ID"))
    bot_token = os.environ["BOT_TOKEN"]
    PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]
    main(bot_token)
