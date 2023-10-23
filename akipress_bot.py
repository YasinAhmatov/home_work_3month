# # from aiogram import Bot,Dispatcher,types,executor
# # from dotenv import load_dotenv
# # from bs4 import BeautifulSoup
# # import os
# # from logging import basicConfig, INFO
# # import requests


# # load_dotenv('.env')

# # basicConfig(level=INFO)
# # bot = Bot(os.environ.get('token'))
# # dp = Dispatcher(bot)

# # @dp.message_handler(commands='start')
# # async def start(message:types.Message):
# #     await message.answer(f"привет {message.from_user.full_name}")


# # @dp.message_handler(commands='news')
# # async def start(message:types.Message):
# #     await message.answer(f"отправляю новости с сайта...")

# #     url = "https://akipress.org/"

# #     reponse = requests.get(url=url)
# #     print(reponse)
# #     soup = BeautifulSoup(reponse.text, 'lxml')
# #     # print(soup)

# #     all_news = soup.find_all('a',class_='newslink')
# #     # print(all_nesws)

# #     n= 0
# #     for news in all_news:
# #         n += 1
# #         print(f'{n} {news.text}')
# #         await message.answer(f"{n}) {news.text}")





# # executor.start_polling(dp,skip_updates=True)



# import os
# import requests
# from lxml import html
# from aiogram import Bot, Dispatcher, types,executor
# from dotenv import load_dotenv

# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(bot)

# NATIONAL_BANK_URL = "https://www.nbkr.kg/index.jsp?lang=RUS"

# def parse_exchange_rates():
#     response = requests.get(NATIONAL_BANK_URL)
#     tree = html.fromstring(response.text)
#     currency_elements = tree.xpath("//div[@class='rates']/div[@class='currency']")
#     exchange_rates = {}

#     for element in currency_elements:
#         currency_name = element.text.strip()
#         rate = element.getnext().text.strip()
#         exchange_rates[currency_name] = rate

#     return exchange_rates

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer("Добро пожаловать! Введите валюту для обмена (USD, EURO, RUB, KZT):")

# @dp.message_handler(lambda message: message.text in ["USD", "EURO", "RUB", "KZT"])
# async def choose_currency(message: types.Message):
#     currency = message.text
#     await message.answer(f"Вы выбрали валюту: {currency}. Теперь введите сумму для обмена:")

# @dp.message_handler(lambda message: message.text.isdigit())
# async def exchange_amount(message: types.Message):
#     currency = message.reply_markup.inline_keyboard[0][0].text.split()[-1]
#     amount = int(message.text)
    
#     exchange_rates = parse_exchange_rates()

#     if currency in exchange_rates:
#         rate = exchange_rates[currency]
#         converted_amount = round(amount / float(rate), 2)
#         await message.answer(f"{amount} {currency} = {converted_amount} сом по курсу {rate}")
#     else:
#         await message.answer("Извините, информация о данной валюте недоступна.")


# executor.start_polling(dp, skip_updates=True)




import os
import requests
from lxml import html
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
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
