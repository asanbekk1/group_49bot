from aiogram import Router
from aiogram.filters import Command
from aiogram import types


myinfo_router = Router()

@myinfo_router.message(Command("myinfo"))
async def start(message: types.Message):
    await message.answer(f'ur first_name:{message.from_user.first_name}/nur id:{message.from_user.id}/nur username:@{message.from_user.username}')

