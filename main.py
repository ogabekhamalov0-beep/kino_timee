import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# MA'LUMOTLAR
TOKEN = "8763679121:AAHzxQs_CqIu1WZomFIe8H0vLBVTKqbO7rw"
ADMIN_ID = 8763679121  # Sizning ID raqamingiz
CHANNEL_ID = -1003803083665  # Kanal ID (oldiga -100 qo'shiladi)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ma'lumotlar bazasini yaratish
db = sqlite3.connect("kinolar.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS movies (code TEXT, file_id TEXT)")
db.commit()

# Vaqtinchalik xotira (Admin kino yuborganda kodini saqlab turish uchun)
admin_temp_data = {}

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Salom! **Kino Time** botiga xush kelibsiz.\nKino yaratuvchisi: **Ogʻabek Hamalov**\n\nKino kodini yuboring:")

# ADMIN UCHUN: Kino (video) qabul qilish
@dp.message(F.video & (F.from_user.id == ADMIN_ID))
async def get_video(message: types.Message):
    file_id = message.video.file_id
    admin_temp_data[message.from_user.id] = file_id
    await message.answer("Video qabul qilindi. Endi ushbu kino uchun kod kiriting:")

# ADMIN UCHUN: Kodni bazaga saqlash
@dp.message(F.text.isdigit() & (F.from_user.id == ADMIN_ID))
async def save_movie(message: types.Message):
    user_id = message.from_user.id
    if user_id in admin_temp_data:
        code = message.text
        file_id = admin_temp_data[user_id]
        
        cursor.execute("INSERT INTO movies (code, file_id) VALUES (?, ?)", (code, file_id))
        db.commit()
        
        del admin_temp_data[user_id]
        await message.answer(f"Muvaffaqiyatli saqlandi! Kod: {code}")
    else:
        # Agar admin bo'lmasa yoki shunchaki kod yozsa, kino qidiradi
        await search_movie(message)

# FOYDALANUVCHILAR UCHUN: Kino qidirish
async def search_movie(message: types.Message):
    code = message.text
    cursor.execute("SELECT file_id FROM movies WHERE code = ?", (code,))
    result = cursor.fetchone()
    
    if result:
        # Kinoni forward emas, balki file_id orqali yuborish
        await bot.send_video(
            chat_id=message.chat.id, 
            video=result[0], 
            caption=f"Kino kodi: {code}\n@kino_time_vaqti kanali uchun"
        )
    else:
        await message.answer("Bunday kodli kino topilmadi. Iltimos, kodni to'g'ri kiriting.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
