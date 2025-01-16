from aiogram import Router, types,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
from datetime import datetime

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    instagram_username = State()
    rating = State()
    extra_comments = State()
    visit_date = State()

rating_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1', callback_data='rating:1'),
        InlineKeyboardButton(text='2', callback_data='rating:2'),
        InlineKeyboardButton(text='3', callback_data='rating:3'),
        InlineKeyboardButton(text='4', callback_data='rating:4'),
        InlineKeyboardButton(text='5', callback_data='rating:5'),
    ]
])

def cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='cancel', callback_data='cancel')],
    ])

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS database (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        instagram_username TEXT,
        rating INTEGER,
        extra_comments TEXT,
        visit_date TEXT
    )''')
    conn.commit()
    conn.close()

@review_router.callback_query(F.data=='review')
async def start_review(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('What is your name?', reply_markup=cancel_keyboard())
    await state.set_state(RestaurantReview.name)

@review_router.message(RestaurantReview.name)
async def process_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer("What is your Instagram username?", reply_markup=cancel_keyboard())
    await state.set_state(RestaurantReview.instagram_username)

@review_router.message(RestaurantReview.instagram_username)
async def process_instagram_username(m: types.Message, state: FSMContext):
    await state.update_data(instagram_username=m.text)
    await m.answer('Please rate our restaurant:', reply_markup=rating_kb)
    await state.set_state(RestaurantReview.rating)


@review_router.callback_query(RestaurantReview.rating)
async def process_rating(call: types.CallbackQuery, state: FSMContext):
    rating = int(call.data.split(':')[1])
    await state.update_data(rating=rating)
    await call.message.answer("Do you have any extra comments?", reply_markup=cancel_keyboard())
    await state.set_state(RestaurantReview.extra_comments)

@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(m: types.Message, state: FSMContext):
    await state.update_data(extra_comments=m.text)
    await m.answer("What was the date of your visit? (Optional, format: YYYY-MM-DD)", reply_markup=cancel_keyboard())
    await state.set_state(RestaurantReview.visit_date)

@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(m: types.Message, state: FSMContext):
    visit_date = m.text.strip()
    if visit_date:
        try:
            datetime.strptime(visit_date, '%Y-%m-%d')
        except ValueError:
            await m.answer("Invalid date format. Please use YYYY-MM-DD.")
            return
    else:
        visit_date = None

    data = await state.get_data()
    save_review(data, visit_date)
    await m.answer("Thank you for your review! Your feedback has been saved.")
    await state.clear()

def save_review(data, visit_date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO database (name, instagram_username, rating, extra_comments, visit_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['instagram_username'], data['rating'], data['extra_comments'], visit_date))
    conn.commit()
    conn.close()

@review_router.callback_query(F.data=='cancel')
async def cancel_review(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Review process cancelled.", reply_markup=None)
    await state.clear()

init_db()
