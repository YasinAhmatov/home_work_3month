import logging
from aiogram import Bot, Dispatcher, types

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token="6396642163:AAH5mVSwGC7kMlBLJ2jFvjb7LLTvJ0tRWR0")

# Создаем диспетчер и передаем в него объект бота
dp = Dispatcher(bot)

# Клавиатура главного меню
menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(types.KeyboardButton("О нас"))
menu_keyboard.add(types.KeyboardButton("Объекты"))
menu_keyboard.add(types.KeyboardButton("Контакты"))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Выберите интересующий пункт меню:", reply_markup=menu_keyboard)

# Обработчики кнопок меню
@dp.message_handler(lambda message: message.text in ["О нас", "Объекты", "Контакты"])
async def process_menu(message: types.Message):
    if message.text == "О нас":
        # Здесь можно добавить код для получения информации с сайта https://vg-stroy.com/about/
        pass
    elif message.text == "Объекты":
        # Здесь можно добавить код для получения информации о всех объектах
        pass
    elif message.text == "Контакты":
        # Здесь можно добавить код для отправки контактов
        pass

if __name__ == '__main__':
    from aiogram import executor

executor.start_polling(dp, skip_updates=True)
