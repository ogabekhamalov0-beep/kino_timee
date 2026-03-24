import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Tokenni Render Variables-dan olish
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ma'lumotlar bazasini sozlash
def init_db():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id TEXT PRIMARY KEY,
            file_id TEXT
        )
    """)
    conn.commit()
    conn.close()

# Start buyrug'i
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"Salom {message.from_user.full_name}!\n"
        "Kino kodini yuboring yoki admin bo'lsangiz yangi kino yuklang.\n\n"
        "Bu botni Ogʻabek Hamalov yaratdi."
    )

# Kino kodini qabul qilish
@dp.message(F.text.isdigit())
async def get_movie(message: types.Message):
    code = message.text
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM movies WHERE id = ?", (code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        await message.answer_video(result[0], caption=f"Kino kodi: {code}")
    else:
        await message.answer("Kechirasiz, bu kod bilan kino topilmadi.")

# Admin uchun kino yuklash (Video yuborilganda)
@dp.message(F.video)
async def add_movie(message: types.Message):
    # Bu yerda admin ID-sini tekshirishni qo'shishingiz mumkin
    file_id = message.video.file_id
    await message.answer(f"Kino qabul qilindi. Endi unga kod bering (faqat raqam yuboring):")
    
    # Kodni kutish uchun vaqtincha saqlash (oddiyroq usulda)
    @dp.message(F.text.isdigit())
    async def save_code(msg: types.Message):
        movie_code = msg.text
        try:
            conn = sqlite3.connect("movies.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movies (id, file_id) VALUES (?, ?)", (movie_code, file_id))
            conn.commit()
            conn.close()
            await msg.answer(f"Muvaffaqiyatli saqlandi! Kod: {movie_code}")
        except sqlite3.IntegrityError:
            await msg.answer("Bu kod bilan allaqachon kino mavjud. Boshqa kod bering.")

async def main():
    init_db()
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
            
