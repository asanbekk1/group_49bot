from aiogram import Bot,Dispatcher,Router
from aiogram.filters import Command
from aiogram import types

start_router = Router()


kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Review',callback_data='review')]
])

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.reply(f'Привет, {name}', reply_markup=kb)