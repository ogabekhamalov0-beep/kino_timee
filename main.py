import os
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# Render uchun soxta port ochish (Port xatosini yo'qotadi)
async def handle(request):
    return web.Response(text="Bot is running!")

async def run_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# Tokenni Render Variables-dan olish
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ma'lumotlar bazasini sozlash
def init_db():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS movies (id TEXT PRIMARY KEY, file_id TEXT)")
    conn.commit()
    conn.close()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}!\nBu botni Ogʻabek Hamalov yaratdi.")

async def main():
    init_db()
    await run_server() # Portni ishga tushiramiz
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
