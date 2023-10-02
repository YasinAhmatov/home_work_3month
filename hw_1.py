import random
from aiogram import Bot,Dispatcher,types,executor
from config import token2

bot = Bot(token = token2)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer('Привет я рандом бот,загадываю случайное число если хотите поиграть то нажмите /go')

@dp.message_handler(commands=['go'])
async def start(message:types.Message):
    await message.answer('Я загадал число от 1 до 3 попробуйте угадать')


@dp.message_handler()
async def guess_number(message:types.Message):
    try:
         target_number = random.randint(1,3)
         user_target = int(message.text)

         if user_target != target_number:
             await message.answer_photo("https://media.makeameme.org/created/sorry-you-lose.jpg")
         elif user_target == target_number:
             await message.answer_photo("https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg")
    except:
        await message.reply('Пожалуйста введите число от 1 до 3 !!!')

executor.start_polling(dp)