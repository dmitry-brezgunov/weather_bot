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

def weather_forcast(api_response):
    if api_response['cod'] == "404":
        return f'Извини, я не нашел такого города. Проверь, правильно ли введено название.'
    condition = api_response['weather'][0]['description']
    temp = round(api_response['main']['temp'])
    feel_temp = round(api_response['main']['feels_like'])
    pressure = api_response['main']['pressure']//133.3224*100
    humidity = api_response['main']['humidity']
    wind = api_response['wind']['speed']
    return f"Сейчас {temp}°С, ощущается как {feel_temp}°С, {condition}.\n"\
           f"Давление {pressure} мм. ртутного столба. Влажность воздуха {humidity}%.\n"\
           f"Скорость ветра {wind} м/с."

def weather_recomendations(api_response):
    if api_response['weather'][0]['id'] in [731, 751, 761, 762, 771, 781]:
        return "На улице ужасная погода, сиди дома."
    elif api_response['main']['temp'] < -20:
        return "На улице очень холодно. Может лучше остаться дома?"
    elif api_response['weather'][0]['id'] in [602, 613, 621, 622]:
        return "На улице метель. Может лучше остаться дома?."
    elif api_response['main']['temp'] < 0:
        return "На улице холодно, одевайся теплее."
    elif api_response['weather'][0]['id'] in range(200, 233):
        return "На улице гроза. Может лучше остаться дома?"
    elif api_response['weather'][0]['id'] in [502, 503, 504, 522, 531]:
        return "На улице ливень. Может лучше остаться дома?"
    elif api_response['weather'][0]['id'] in [500, 501, 520, 521]:
        return "На улице дождь, не забудь взять зонт."
    elif api_response['main']['temp'] < 15:
        return "На улице прохладно, лучше надень куртку."
    elif api_response['main']['temp'] < 25 and api_response['weather'][0]['id'] in range(800, 805):
        return "На улице хорошая погода, самое время для прогулки."
    elif api_response['main']['temp'] < 35 and api_response['weather'][0]['id'] == 800:
        return "На улице жарко и солнечно, старайся держаться тени."
    elif api_response['main']['temp'] < 35:
        return "На улице жарко, можно надеть шорты."
    else:
        return "На улице очень жарко, старайся пить больше воды."

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text
    params = {"appid": OPENWEATHER_TOKEN, "q": city, "lang": "ru", "units": "metric"}
    api_result = requests.get('http://api.openweathermap.org/data/2.5/weather', params)
    api_response = api_result.json()
    bot.send_message(message.from_user.id, weather_forcast(api_response))
    bot.send_message(message.from_user.id, weather_recomendations(api_response))

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as e:
        print(f"Бот упал с ошибкой: {e}.")
        time.sleep(5)
