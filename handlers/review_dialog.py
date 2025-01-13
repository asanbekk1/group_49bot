from  aiogram import Bot,Dispatcher,Router,F
from aiogram import types
from aiogram .fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup


review_router = Router()


class RestaurantReview(StatesGroup):
    name = State()
    instagram_username = State()
    rate = State()
    extra_comments = State()



@review_router.callback_query(F.date == 'review')
async def start_review(call:types.CallbackQuery,state:FSMContext):
    await call.message.answer('what is ur name?')
    await state.set_state(RestaurantReview.name)


@review_router.message(RestaurantReview.name)
async def process_name(m:types.CallbackQuery,state:FSMContext):
    await state.update_data(name=m.text)
    await m.answer("what it ur inst username?")
    await state.set_state(RestaurantReview.instagram_username)


@review_router.message(RestaurantReview.instagram_username)
async def process_name(m:types.CallbackQuery,state:FSMContext):
    await state.update_data(name=m.text)
    await m.answer('how would u rate our cafe?')
    await state.set_state(RestaurantReview.rate)


@review_router.message(RestaurantReview.rate)
async def process_name(m:types.CallbackQuery,state:FSMContext):
    if m.text.isdigit():
        if int(m.text) <= 5:
            await state.update_data(rate=m.text)
            await m.answer("ur extra comments?")
            await state.set_state(RestaurantReview.extra_comments)
        else:
            await m.answer("write only between 1 and 5!!!")
    else:
        await m.answer("write only digits!!!")


@review_router.message(RestaurantReview.extra_comments)
async def process_name(m:types.Message,state:FSMContext):
    await state.update_data(rate=m.text)
    data = await state.get_data()
    await m.answer(f'name:{data["name"]}/ninstagram:{data["instagram_username"]}/nrate:{data["rate"]}/extra_comments:{data['extra']}')
    await state.clear()


