from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from bot_config import database


dish_router = Router()


class DishForm(StatesGroup):
    category = State()
    name = State()
    price = State()
    description = State()
    portion_sizes = State()
    photo = State()


categories = [
    'Первое', 'Второе', 'Пицца', 'Горячие напитки',
    'Холодные напитки', 'Салаты', 'Горячительные напитки'
]


def category_keyboard():
    keyboard = [
        [InlineKeyboardButton(text=category, callback_data=f'category:{category}')] for category in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dish_router.message(Command('newdish'))
async def start_adding_dish(m: types.Message, state: FSMContext):
    await m.answer("Выберите категорию блюда:", reply_markup=category_keyboard())
    await state.set_state(DishForm.category)


@dish_router.callback_query(DishForm.category)
async def category_selected(call: types.CallbackQuery, state: FSMContext):
    category = call.data.split(':')[1]
    await state.update_data(category=category)
    await call.message.answer(f"Вы выбрали категорию: {category}. Теперь введите название блюда.")
    await state.set_state(DishForm.name)


@dish_router.message(DishForm.name)
async def process_name(m: types.Message, state: FSMContext):
    name = m.text
    await state.update_data(name=name)
    await m.answer("Введите цену блюда (например, 200.50):")
    await state.set_state(DishForm.price)


@dish_router.message(DishForm.price)
async def process_price(m: types.Message, state: FSMContext):
    try:
        price = float(m.text)
        await state.update_data(price=price)
        await m.answer("Введите описание блюда:")
        await state.set_state(DishForm.description)
    except ValueError:
        await m.answer("Некорректная цена. Пожалуйста, введите цену в формате числа (например, 200.50):")


@dish_router.message(DishForm.description)
async def process_description(m: types.Message, state: FSMContext):
    description = m.text
    await state.update_data(description=description)
    await m.answer("Введите варианты порций (например, маленькая, средняя, большая):")
    await state.set_state(DishForm.portion_sizes)


@dish_router.message(DishForm.portion_sizes)
async def process_portion_sizes(m: types.Message, state: FSMContext):
    portion_sizes = m.text
    await state.update_data(portion_sizes=portion_sizes)

    await m.answer("Пожалуйста, отправьте фото блюда.")
    await state.set_state(DishForm.photo)


@dish_router.message(DishForm.photo, content_types=types.ContentType.PHOTO)
async def process_photo(m: types.Message, state: FSMContext):
    if m.photo:
        file = await m.photo[-1].download()
        photo_path = file.name

        await state.update_data(photo=photo_path)

        await m.answer("Фото успешно загружено! Теперь блюдо будет добавлено.")

        data = await state.get_data()

        database.save_dish(
            data['name'],
            data['price'],
            data['description'],
            data['category'],
            data['portion_sizes'],
            photo_path
        )

        await m.answer(f"Блюдо '{data['name']}' успешно добавлено в меню!")

        await state.clear()
    else:
        await m.answer("Пожалуйста, отправьте фото блюда.")


@dish_router.message(Command('list_dishes'))
async def list_dishes(m: types.Message):
    dishes = database.get_dishes(sort_by='name', order='ASC')

    if dishes:
        response = ""
        for dish in dishes:
            name = dish[1]
            category = dish[2]
            price = dish[3]
            description = dish[4]
            portion_sizes = dish[5]
            image_url = dish[6]

            response += f"Блюдо: {name}\nКатегория: {category}\nЦена: {price} руб\nОписание: {description}\nПорции: {portion_sizes}\n"

            if image_url:
                response += f"Фото: {image_url}\n"
            response += "\n"
        await m.answer(response)
    else:
        await m.answer("Нет блюд в меню.")
