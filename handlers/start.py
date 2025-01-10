from aiogram import Bot, Dispatcher,Router
from aiogram.filters import Command
from aiogram import types

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.reply(f'Привет, {name}/n'
                        f'Мои комманды:')