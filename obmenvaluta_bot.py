import os
import requests
from lxml import html
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from logging import basicConfig,INFO

load_dotenv('.env')

basicConfig(level=INFO)
bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
NATIONAL_BANK_URL = "https://www.nbkr.kg/index.jsp?lang=RUS"

def parse_exchange_rates():
    response = requests.get(NATIONAL_BANK_URL)
    tree = html.fromstring(response.text)
    currency_elements = tree.xpath("//div[@class='rates']/div[@class='currency']")
    exchange_rates = {}

    for element in currency_elements:
        currency_name = element.text.strip()
        rate = element.getnext().text.strip()
        exchange_rates[currency_name] = rate

    return exchange_rates

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Введите сумму сомов (KGS) для обмена:")

@dp.message_handler(lambda message: message.text.isdigit())
async def exchange_amount(message: types.Message):
    kgs_amount = int(message.text)
    
    exchange_rates = parse_exchange_rates()

    if "USD" in exchange_rates:
        usd_rate = float(exchange_rates["USD"])
        usd_amount = round(kgs_amount / usd_rate, 2)
        await message.answer(f"{kgs_amount} KGS = {usd_amount} USD по курсу {usd_rate}")

    if "EURO" in exchange_rates:
        euro_rate = float(exchange_rates["EURO"])
        euro_amount = round(kgs_amount / euro_rate, 2)
        await message.answer(f"{kgs_amount} KGS = {euro_amount} EURO по курсу {euro_rate}")

    if "RUB" in exchange_rates:
        rub_rate = float(exchange_rates["RUB"])
        rub_amount = round(kgs_amount / rub_rate, 2)
        await message.answer(f"{kgs_amount} KGS = {rub_amount} RUB по курсу {rub_rate}")

    if "KZT" in exchange_rates:
        kzt_rate = float(exchange_rates["KZT"])
        kzt_amount = round(kgs_amount / kzt_rate, 2)
        await message.answer(f"{kgs_amount} KGS = {kzt_amount} KZT по курсу {kzt_rate}")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)