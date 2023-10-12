from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pytube import YouTube
from dotenv import load_dotenv 
import os
import logging
import sqlite3

conn = sqlite3.connect('users.db')  # Connect to the database or create a new one
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS downloads (
                  download_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  username TEXT,
                  full_name TEXT,
                  download_type TEXT,
                  download_url TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (user_id)
                )''')
conn.commit()

load_dotenv('.env')

bot = Bot(os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    cursor.execute('INSERT INTO downloads (user_id, username, full_name) VALUES (?, ?, ?)', (user_id, username, full_name))
    conn.commit()  
    
    await message.answer(f"""Здравствуйте, {full_name}
Я вам помогу скачать аудио или видео с YouTube""")
class DownloadAudio(StatesGroup):
    download = State()

class DownloadVideo(StatesGroup):
    download = State()

def download(url, type):
    yt = YouTube(url)
    if type == "audio":
        yt.streams.filter(only_audio=True).first().download("audio", f"{yt.title}.mp3")
        return f"{yt.title}.mp3"
    elif type == "video":
        yt.streams.filter(progressive=True, file_extension="mp4").first().download("video", f"{yt.title}.mp4")
        return f"{yt.title}.mp4"

@dp.message_handler(text = ["Аудио", "аудио", "Audio", "audio"])
async def audio(message: types.Message):
    await message.answer("Отправьте ссылку на видео и я вам отправлю его в mp3")
    await DownloadAudio.download.set()

@dp.message_handler(text = ["Видео", "видео", "Video", "video"])
async def video(message: types.Message):
    await message.answer("Отправьте ссылку на видео в ютубе и я вам его отправлю")
    await DownloadVideo.download.set()

def record_download(user_id, download_type, download_url):
    cursor.execute('INSERT INTO downloads (user_id, download_type, download_url) VALUES (?, ?, ?)',
                   (user_id, download_type, download_url))
    conn.commit()

@dp.message_handler(state=DownloadAudio.download)
async def download_audio(message: types.Message, state: FSMContext):
    try:
        title = download(message.text, "audio")
        audio = open(f"audio/{title}", "rb")
        await message.answer("Скачиваем файл, ожидайте...")
        try:
            await message.answer("Все скачалось, вот держи")
            await bot.send_audio(message.chat.id, audio)
            
            # Record the download in the database
            user_id = message.from_user.id
            download_url = message.text
            record_download(user_id, "audio", download_url)
        except:
            await message.answer("Произошла ошибка, попробуйте позже")
        await state.finish()
    except:
        await message.answer("Неверная ссылка на видео")
        await state.finish()



@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp)