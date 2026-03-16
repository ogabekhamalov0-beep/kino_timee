import telebot

TOKEN = "8763679121:AAEpG4mz4W4F73TOoZ-SPRf4Nft8Z4izLfs"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
    "🎬 Salom!\n\nKino kodini yuboring.\nBot sizga kinoni yuboradi.")

@bot.message_handler(func=lambda message: True)
def kino(message):
    if message.text == "1":
        bot.send_message(message.chat.id, "🎬 Kino topildi (keyin video qo'shamiz)")
    else:
        bot.send_message(message.chat.id, "❌ Bunday kino kodi yo'q")

print("Bot ishga tushdi...")
bot.polling()
