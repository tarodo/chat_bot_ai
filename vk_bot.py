import os
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

#
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         print('Новое сообщение:')
#         if event.to_me:
#             print('Для меня от: ', event.user_id)
#         else:
#             print('От меня для: ', event.user_id)
#         print('Текст:', event.text)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_session = vk_api.VkApi(token=os.environ["VK_BOT_TOKEN"])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)