import os
import time
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENWEATHER_TOKEN = os.getenv('OPENWEATHER_TOKEN')
URL = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/'


def send_message(chat_id, text):
    url = URL + 'sendMessage'
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def get_weather():
    params = {"appid": OPENWEATHER_TOKEN, "q": "Moscow", "units": "metric", "lang": "ru"}
    api_result = requests.get('https://api.openweathermap.org/data/2.5/weather', params)
    api_response = api_result.json()
    return f"Сейчас в Москве {api_response['main']['temp']} градусов"

@app.route('/' + TELEGRAM_TOKEN + '/', methods=['POST', 'GET'])
def main():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json["message"]["chat"]["id"]
        weather = get_weather()
        send_message(chat_id, weather)
    return {"ok": True}

if __name__ == '__main__':
    main()
