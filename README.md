# Чат-бот в телеграм и vk
Бот для общения с пользователями. Позволяет с помощью сервиса Dialogflow обучить бота для ответа на вопросы от пользователей

Бот работает одновременно в телеграм и вкотакте. Готов к деплою на heroku.

## Env
Необходимы следующие переменные окружения:
- BOT_TOKEN - str, токен от [BotFather](https://t.me/botfather)
- BOT_REPORT_TOKEN - str, токен для бота-логгера
- GOOGLE_APPLICATION_CREDENTIALS - str, путь до файла с кредами [Google](https://cloud.google.com/docs/authentication/getting-started)
- GOOGLE_PROJECT_ID - str, ID проекта из [консоли](https://console.cloud.google.com/home) Google
- QUESTIONS_FILE  - str, путь до файла для обучения чат-бота
- VK_BOT_TOKEN - str, токен для диалога с группой в vk ![img_1.png](img_1.png)
- CHAT_ID - str, telegram id админа для логов

## Обучение
Обучить бота можно с помощью load_intent.py
```
python load_intent.py
```

### Файл для обучения
В файле в виде JSON хранятся данные для обучения в виде
```
{
    themme - str: {
        questions: [question - str],
        answer: str
    }
}
```

## Локальный запуск
1. Создать файл `.env` из `.env.Exmaple`
2. `pip install -r requirements.txt`
3. run:
   1. Telegram: `python main.py`
   2. VK: `python vk_bot.py`

## Запуск на heroku
Создать app на [heroku](https://www.heroku.com/) и добавить переменные в Settings -> Config Vars