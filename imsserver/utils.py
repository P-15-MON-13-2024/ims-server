
from telebot.async_telebot import AsyncTeleBot
import asyncio
from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imsserver.settings')

bot = AsyncTeleBot(settings.TELEGRAM_TOKEN)
    
@bot.message_handler(commands=['start', 'hello'])
async def send_welcome(message):
    await bot.reply_to(message, "Howdy, how are you doing?")

def run_telegram_bot():
    asyncio.run(bot.polling())