from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from logging import basicConfig, INFO
import os, requests, asyncio, aioschedule

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
basicConfig(level=INFO)

async def send_btc_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')
    if price:
        return f"Цена биткоина {price}$"
    else:
        return "Не удалось получить цену биткоина"

async def scheduler():
    while True:
        message = await send_btc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(2)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

@dp.message_handler(commands='btc')
async def start_btc_monitoring(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await message.answer("Мониторинг стоимости биткоина начат. Вы будете получать обновления каждые 10 секунд.")
    await scheduler()

async def on_startup(dp):
    # Запускаем планировщик задач
    aioschedule.every(2).seconds.do(scheduler)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)