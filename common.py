import logging

from telegram import Bot


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
