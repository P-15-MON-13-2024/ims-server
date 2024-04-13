
from telebot.async_telebot import AsyncTeleBot
import asyncio
from django.conf import settings
from dashboard.models import TelegramChatID, Sapien
import time 
from asgiref.sync import sync_to_async
import threading

bot = AsyncTeleBot(settings.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
async def send_welcome(message):
    await bot.reply_to(message, "Howdy, how are you doing?")

@sync_to_async
def findTelegramChatID(insti_id):
    return TelegramChatID.objects.filter(sapien__insti_id=insti_id).first()
@sync_to_async
def createTelegramChatID(sapien,chat_id):
    TelegramChatID(sapien=sapien, chat_id=chat_id).save() 
    return True

@sync_to_async
def findSapien(insti_id):
    return Sapien.objects.get(insti_id=insti_id)

async def telebot_notify_async(insti_id, message):
    object = await findTelegramChatID(insti_id)
    chat_id = object.chat_id
    await bot.send_message(chat_id=int(chat_id), text=message)

def telebot_notify_sync(insti_id, text):
    thread = threading.Thread(target=asyncio.run(telebot_notify_async(insti_id, text)))
    thread.start()
    thread.join()

@bot.message_handler(commands=['register'])
async def register_telegram_chat_id(message):
    chat_id = message.chat.id
    insti_id =message.text.split()[1]
    existing_chat_id = await findTelegramChatID(insti_id)
    if not existing_chat_id:
        sapien_instance = await findSapien(insti_id)
        await createTelegramChatID(sapien=sapien_instance, chat_id=chat_id)
        await telebot_notify_async(insti_id, "Registeration Successful")
        return
    await telebot_notify_async(insti_id, "You're already registered")

def run_telegram_bot():
    time.sleep(2)
    asyncio.run(bot.polling())