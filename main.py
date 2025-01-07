import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
import logging

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    # message.from_user.id
    await message.answer(f"Привет, {name}")

from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, types
from asyncio import run
from aiogram.filters import Command
import random

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()

names = ('name','aidar','igor')


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f'hello{message.from_user.first_name}')


@dp.message(Command("my_info"))
async def start(message: types.Message):
    await message.answer(f'ur first_name:{message.from_user.first_name}/nur id:{message.from_user.id}/nur username:@{message.from_user.username}')


@dp.message(Command("random"))
async def start(message: types.Message):
    await message.answer(random.choice(names))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())


async def main():
    await dp.start_polling(bot)





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())









