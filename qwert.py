import logging
import random
import smtplib
import re
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# Ваш токен Telegram бота
BOT_TOKEN = '5884805064:AAFlp8YTTcfpFSrqCBPDG5Bpw4-BDPS9-bI'

# Настройки SMTP для отправки кода на почту
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Словарь для хранения кодов пользователей (user_id: code)
verification_codes = {}

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# Состояния для управления диалогом
class States:
    EMAIL = 'email'
    VERIFICATION = 'verification'

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    verification_code = generate_verification_code()
    verification_codes[user_id] = verification_code

    # Устанавливаем состояние "EMAIL" для пользователя
    await States.EMAIL.set()

    await message.answer("Для идентификации, введите вашу почту:")
    
@dp.message_handler(lambda message: message.text, state=States.EMAIL)
async def process_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    email = message.text

    if validate_email(email):
        verification_code = verification_codes.get(user_id)

        # Отправка кода на почту
        send_verification_code(email, verification_code)

        await state.update_data(email=email)

        await message.answer("Код отправлен на вашу почту. Введите код для идентификации:")
        await States.VERIFICATION.set()
    else:
        await message.answer("Неправильный формат почты. Введите корректный адрес почты:")

@dp.message_handler(lambda message: message.text, state=States.VERIFICATION)
async def process_verification_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_code = message.text
    data = await state.get_data()
    email = data.get('email')
    verification_code = verification_codes.get(user_id)

    if user_code == verification_code:
        await message.answer("Вы успешно идентифицировались!")
    else:
        await message.answer("Неправильный ввод. Введите код еще раз:")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
