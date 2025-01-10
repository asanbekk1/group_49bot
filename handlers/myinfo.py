from aiogram import Bot, Dispatcher,Router
from aiogram.filters import Command
from aiogram import types

myinfo_router = Router()


@myinfo_router.message(Command("myinfo"))
async def start(message: types.Message):
    id = message.from_user.idz
    name = message.from_user.first_name
    nickname = message.from_user.username
    await message.answer(f'Ваше имя: {name}'
                        f'Ваш nickname: {nickname}'
                         f'Ваш id: {id}')
