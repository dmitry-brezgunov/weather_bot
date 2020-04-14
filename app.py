import os
import time
import telebot
import requests
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

def get_weather():
    params = {"appid": "OPENWEATHER_TOKEN", "q": "Moscow", "lang": "ru", "units": "metric"}
    api_result = requests.get('https://api.openweathermap.org/data/2.5/weather', params)
    api_response = api_result.json()
    return f"Сейчас в Москве {api_response.get('main').get('temp')} градусов"

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, f"Привет, сейчас я расскажу тебе погоду в Москве")
    get_weather()

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as e:
        print(f">>>>>> error: {e}")
        time.sleep(5)
