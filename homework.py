
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    print("Ошибка: токен бота не найден.")
else:
    print("Токен бота успешно загружен!")

from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

if bot_token is None:
    print("Ошибка: токен бота не найден.")
else:
    bot = Bot(token=bot_token)
    print("Бот успешно подключен!")
