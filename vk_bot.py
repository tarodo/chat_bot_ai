import os
import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_connect import detect_intent_text
from log_config import get_logger


def send_answer(event, vk_api):
    response = detect_intent_text(event.user_id, event.text)

    if response:
        vk_api.messages.send(
            user_id=event.user_id, message=response, random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    logger = get_logger("vk_bot", os.getenv("BOT_REPORT_TOKEN"), os.getenv("TG_ADMIN_CHAT_ID"))

    vk_session = vk_api.VkApi(token=os.environ["VK_BOT_TOKEN"])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(event, vk_api)
