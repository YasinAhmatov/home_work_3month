from aiogram import Bot, Dispatcher,types,executor
from config import token4
from logging import basicConfig, INFO

bot = Bot(token=token4)
dp =Dispatcher(bot)
basicConfig(level=INFO) 


courses_keyboards = [
    types.KeyboardButton("Beckend"),
    types.KeyboardButton("Frontend"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("UX/UI"),
]
courses_button= types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_keyboards)


@dp.message_handler(commands='start')
async def start (message:types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}", reply_markup=courses_button)
    print(message)






@dp.message_handler(text="Курсы")
async def get_courses(message:types.Message):
    await message.answer("Выверите курсы:", reply_markup=courses_button)

@dp.message_handler(text='Beckend')
async def beckend(message:types.Message):
    await message.answer("""Backend — это внутренняя часть сайта и сервера и т.д
Стоимость 10000 сом в месяц
Обучение: 5 месяц
""")

@dp.message_handler(text='Frontend')
async def frontend(message:types.Message):
    await message.answer("""Frontend\nзанимается разработкой пользовательского интерфейса, то есть той части сайта или приложения, которую видят посетители страницы
Стоимость 10000 сом в месяц
Обучение: 5 месяц""")

@dp.message_handler(text='Android')
async def android(message:types.Message):
    await message.answer("""Android\nразработчик создает приложения для устройств на операционной системе Android
Стоимость 10000 сом в месяц
Обучение: 7 месяц""")

@dp.message_handler(text='IOS')
async def ios(message:types.Message):
    await message.answer("""IOS\nразработчик создает приложения для устройств Apple
Стоимость 10000 сом в месяц
Обучение: 7 месяц""")

@dp.message_handler(text='UX/UI')
async def uxui(message:types.Message):
    await message.answer("""ux/ui - это дизайн сайта
Стоимость 10000 сом в месяц
Обучение: 3 месяц""")






executor.start_polling(dp)