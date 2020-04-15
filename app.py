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
    condition = api_response['weather'][0]['description']
    temp = round(api_response['main']['temp'])
    feel_temp = round(api_response['main']['feels_like'])
    pressure = round(api_response['main']['pressure']*100//133.3224)
    humidity = api_response['main']['humidity']
    wind = api_response['wind']['speed']
    return f"Сейчас {temp}°С, ощущается как {feel_temp}°С, {condition}.\n"\
           f"Давление {pressure} мм. ртутного столба. Влажность воздуха {humidity}%.\n"\
           f"Скорость ветра {wind} м/с."

def weather_recomendations(api_response):
    if api_response['weather'][0]['id'] in [731, 751, 761, 762, 771, 781]:
        recomendation = "На улице ужасная погода, сиди дома."
    elif api_response['main']['feels_like'] < -20:
        recomendation = "На улице очень холодно. Может лучше остаться дома?"
    elif api_response['weather'][0]['id'] in [602, 613, 621, 622]:
        recomendation = "На улице метель. Может лучше остаться дома?."
    elif api_response['main']['feels_like'] < 0:
        recomendation = "На улице холодно, одевайся теплее."
    elif api_response['weather'][0]['id'] in range(200, 233):
        recomendation = "На улице гроза. Может лучше остаться дома?"
    elif api_response['weather'][0]['id'] in [502, 503, 504, 522, 531]:
        recomendation = "На улице ливень. Может лучше остаться дома?"
    elif api_response['weather'][0]['id'] in [500, 501, 520, 521]:
        recomendation = "На улице дождь, не забудь взять зонт."
    elif api_response['main']['feels_like'] < 15:
        recomendation = "На улице прохладно, лучше надень куртку."
    elif api_response['main']['feels_like'] < 25 and api_response['weather'][0]['id'] in range(800, 805):
        recomendation = "На улице хорошая погода, самое время для прогулки."
    elif api_response['main']['feels_like'] < 35 and api_response['weather'][0]['id'] == 800:
        recomendation = "На улице жарко и солнечно, старайся держаться тени."
    elif api_response['main']['feels_like'] < 35:
        recomendation = "На улице жарко, можно надеть шорты."
    else:
        recomendation = "На улице очень жарко, старайся пить больше воды."
    return recomendation

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text
    params = {"appid": OPENWEATHER_TOKEN, "q": city, "lang": "ru", "units": "metric"}
    api_result = requests.get('http://api.openweathermap.org/data/2.5/weather', params)
    api_response = api_result.json()
    if api_response['cod'] == "404":
        bot.send_message(message.from_user.id,
                         'Извини, я не нашел такого города. Проверь, правильно ли введено название.')
    elif api_response['cod'] == "429":
        bot.send_message(message.from_user.id,
                         'Превышено максимальное количетсво запрос к API. Попробуйте позже.')
    else:
        forcast = weather_forcast(api_response)
        recomendation = weather_recomendations(api_response)
        bot.send_message(message.from_user.id, forcast)
        bot.send_message(message.from_user.id, recomendation)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as e:
        print(f"Бот упал с ошибкой: {e}.")
        time.sleep(5)
