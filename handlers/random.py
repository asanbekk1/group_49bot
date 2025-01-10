from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram import types
from random import choice

random_router = Router()

@random_router.message(Command("random"))
async def start(message: types.Message):
    name_list = choice(['Jim', 'Jessie', 'Aisuluu', 'Suga'])
    await message.answer(f'Случайное имя:{name_list}')