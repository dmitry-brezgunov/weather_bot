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
    greeting = f'Привет, {username}! Введи название города и я расскажу тебе о погоде в нем.'
    bot.send_message(message.from_user.id, greeting)

def get_weather(place):
    params = {"appid": OPENWEATHER_TOKEN, "q": place, "lang": "ru", "units": "metric"}
    api_result = requests.get('http://api.openweathermap.org/data/2.5/weather', params)
    api_response = api_result.json()
    if api_response['code'] == 404:
        return f'Извини, я не нашел такого города. Проверь, правильно ли введено название.'
    condition = api_response['weather']['description']
    temp = round(api_response['main']['temp'])
    feel_temp = round(api_response['main']['feels_like'])
    pressure = api_response['main']['pressure']//133.3224*100
    humidity = api_response['main']['humidity']
    wind = api_response['wind']['speed']
    return f"Сейчас в {place} {temp}°С, ощущается как {feel_temp}°С, {condition}.\n"\
           f"Давление {pressure} мм. ртутного столба. Влажность воздуха {humidity}.\n"\
           f"Скорость ветра {wind} м/с."

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    weather = get_weather(message.text)
    bot.send_message(message.from_user.id, weather)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as e:
        print(f"Бот упал с ошибкой: {e}")
        time.sleep(5)
