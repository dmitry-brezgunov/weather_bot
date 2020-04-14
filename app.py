import os
import time
import telebot
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENWEATHER_TOKEN = os.getenv('OPENWEATHER_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    greeting = f'Привет, {username}! \n \n'
    bot.send_message(message.from_user.id, greeting)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as e:
        print(f">>>>>> error: {e}")
        time.sleep(5)
