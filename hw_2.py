from aiogram import Bot, Dispatcher,types,executor
from config import token3
from logging import basicConfig, INFO

bot = Bot(token=token3)
dp =Dispatcher(bot)
basicConfig(level=INFO)

start_keyboards = [
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Объекты"),
    types.KeyboardButton("Контакты"),
]
start_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboards)

@dp.message_handler(commands='start')
async def start (message:types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}, вас приветствует строительная компания Визион Групп", reply_markup=start_button)
    print(message)

@dp.message_handler(text= "О нас")
async def about(message:types.Message):
    await message.answer("Мы - развивающаяся компания, которая предлагает своим клиентам широкий выбор квартир в объектах расположенных во всех наиболее привлекательных районах городов Ош и Джалал-Абад. У нас максимально выгодные условия, гибкий (индивидуальный) подход при реализации жилой и коммерческой недвижимости. Мы занимаем лидирующие позиции по количеству объектов по югу Кыргызстана. Наша миссия: Мы обеспечиваем население удобным жильем для всей семьи, проявляя лояльность и индивидуальный подход и обеспечивая высокий уровень обслуживания. Мы обеспечиваем бизнес подходящим коммерческим помещением, используя современные решения и опыт профессионалов своего дела.")

@dp.message_handler(text= "Объекты")
async def objects(message:types.Message):
   
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_1260,h_708/https://vg-stroy.com/wp-content/uploads/2022/01/dji_0392-scaled-1.jpeg")
    await message.reply("""ЖК Малина-Лайф
г.Ош, ул Монуева 19

Сроки начала строительства: 11
Сроки завершения строительства: 2
Жилой комплекс «Малина Лайф» – эксклюзивный проект бизнес-класса c отличной экологией и богатой инфраструктурой. В шаговой доступности находится вся инфраструктура города Ош: гипермаркеты «Фрунзе» и «Глобус», рынок «Келечек», река «Ак-Буура» и набережная для прогулок всей семьей. Также, на расстоянии двухсот метров расположены парк им. Навои и проспект Масалиева – одна из основных автомагистралей города. Любители престижа и высокого уровня жизни оценят уникальный архитектурный облик и безупречно продуманные планировочные решения квартир.""") 
   


    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_633,h_1280/https://vg-stroy.com/wp-content/uploads/2022/01/2022-02-09-14.22.54.jpg")
    await message.answer("""ЖК «Томирис»
г. Ош, ул. Аматова 1 (ориентир - Драм. театр)

Коммерческие помещения: Есть;

Жилой комплекс «Томирис» – современное жилье бизнес-класса в центре города Ош. Жилой комплекс находится в одном из престижнейших мест в городе с великолепной инфраструктурой и хорошей экологией – рядом расположен парк им. Т Салтыганова, стадион им. А. Суюмбаева, Национальный драматический театр им. С. Ибраимова, банки и полностью отсутствует промышленное производство.""")

    
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_1260,h_708/https://vg-stroy.com/wp-content/uploads/2022/01/dji_0289-scaled-1.jpeg")
    await message.answer(""" ЖК «Черемушки»
г.Ош, ул. Урицкого 15Б

Жилой дом "Черемушки" – современное жилье комфорт класса находится в спальном районе города Ош, где открывается неповторимый вид на Сулайман-Тоо. Богатая инфраструктура и отличная экология - рядом расположены детские сады, областной роддом, школы, парк "Ататюрк" и ВУЗы.""")
   
   
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_1000,h_562/https://vg-stroy.com/wp-content/uploads/2022/01/frunze.jpeg") 
    await message.answer(""" ЖК «Фрунзе»
г.Ош, Ленина 170

Жилой комплекс «Фрунзенский» – стильная новостройка в тихом районе центральной части города, где нет ощущения суеты центра и большого количества людей. От жилого комплекса до Мэрии и центральной площади города менее 1 км. На расстоянии 400 метров находится парк им. Токтогула. Также рядом расположены школы, магазины, рестораны, кафе и многое другое.""")
    

@dp.message_handler(text= "Контакты")
async def contacts(message:types.Message):
    await message.answer("""г.Ош, ул.Аматова 1, Бизнес центр Томирис

contact@vg-stroy.com
+996 709 620088
+996 772 620088
+996 550 620088""")
    
executor.start_polling(dp)
