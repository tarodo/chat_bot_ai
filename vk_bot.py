import os
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from main import detect_intent_text


def dialogflow_answer(event, vk_api):
    response = detect_intent_text(PROJECT_ID, event.user_id, event.text)
    if response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]
    vk_session = vk_api.VkApi(token=os.environ["VK_BOT_TOKEN"])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialogflow_answer(event, vk_api)