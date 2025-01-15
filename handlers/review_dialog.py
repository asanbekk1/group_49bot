from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    instagram_username = State()
    rate = State()
    extra_comments = State()

@review_router.callback_query(F.data == 'review')
async def start_review(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('What is your name?')
    await state.set_state(RestaurantReview.name)

@review_router.message(RestaurantReview.name)
async def process_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer("What is your Instagram username?")
    await state.set_state(RestaurantReview.instagram_username)

@review_router.message(RestaurantReview.instagram_username)
async def process_instagram_username(m: types.Message, state: FSMContext):
    await state.update_data(instagram_username=m.text)
    await m.answer('How would you rate our cafe? (1-5)')
    await state.set_state(RestaurantReview.rate)

@review_router.message(RestaurantReview.rate)
async def process_rate(m: types.Message, state: FSMContext):
    if m.text.isdigit():
        rate = int(m.text)
        if 1 <= rate <= 5:
            await state.update_data(rate=rate)
            await m.answer("Do you have any extra comments?")
            await state.set_state(RestaurantReview.extra_comments)
        else:
            await m.answer("Please rate between 1 and 5!")
    else:
        await m.answer("Please write a number between 1 and 5.")

@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(m: types.Message, state: FSMContext):
    await state.update_data(extra_comments=m.text)
    data = await state.get_data()
    await m.answer(f"Name: {data['name']}\nInstagram: {data['instagram_username']}\nRating: {data['rate']}\nExtra Comments: {data['extra_comments']}")
    await state.clear()
