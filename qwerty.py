import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv 
import os

load_dotenv('.env')

bot = Bot(os.environ.get("TOKEN2"))
bot = Bot(token="6473469214:AAFrQDHtpBvM4I2al_QWq4DlU2EmuCInRdc")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect('dolcevita_bot.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        id_user INTEGER,
        phone_number TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS address (
        id_user INTEGER,
        address_longitude REAL,
        address_latitude REAL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        title TEXT,
        address_destination TEXT,
        date_time_order TEXT
    )
''')
conn.commit()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user
    cursor.execute("SELECT * FROM users WHERE id_user=?", (user.id,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        cursor.execute("INSERT INTO users (first_name, last_name, username, id_user) VALUES (?, ?, ?, ?)",
                       (user.first_name, user.last_name, user.username, user.id))
        conn.commit()

    keyboard = types.InlineKeyboardMarkup()
    button_send_number = types.InlineKeyboardButton(text="Отправить номер", callback_data="send_number")
    button_send_location = types.InlineKeyboardButton(text="Отправить локацию", callback_data="send_location")
    button_order_food = types.InlineKeyboardButton(text="Заказать еду", callback_data="order_food")
    keyboard.add(button_send_number, button_send_location, button_order_food)

    await message.answer(f"Здравствуйте, {user.full_name}!", reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data == "send_number")
async def send_number(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, "Пожалуйста, отправьте свой номер телефона")

    @dp.message_handler(lambda message: message.contact is not None, content_types=types.ContentTypes.CONTACT)
    async def handle_contact(message: types.Message):
        contact = message.contact
        user_id = message.from_user.id
        phone_number = contact.phone_number

        cursor.execute("UPDATE users SET phone_number = ? WHERE id_user = ?", (phone_number, user_id))
        conn.commit()

@dp.callback_query_handler(lambda query: query.data == "send_location")
async def send_location(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, "Пожалуйста, отправьте свою локацию")
    
    @dp.message_handler(lambda message: message.location is not None, content_types=types.ContentTypes.LOCATION)
    async def handle_location(message: types.Message):
        location = message.location
        user_id = message.from_user.id
        latitude = location.latitude
        longitude = location.longitude

        cursor.execute("INSERT INTO address (id_user, address_latitude, address_longitude) VALUES (?, ?, ?)",
                       (user_id, latitude, longitude))
        conn.commit()


@dp.callback_query_handler(lambda query: query.data == "order_food")
async def order_food(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, "Пожалуйста, введите ваш заказ")

    @dp.message_handler(lambda message: message.text)
    async def handle_order(message: types.Message):
        user_id = message.from_user.id
        order = message.text
        date_time_order = str(message.date)

        cursor.execute("INSERT INTO orders (title, address_destination, date_time_order) VALUES (?, ?, ?)",
                       (order, "", date_time_order))
        conn.commit()


executor.start_polling(dp)
