import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Замените YOUR_RAPIDAPI_KEY на ваш ключ API сервиса Hotels на RapidAPI
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"

# Функция для отправки запроса к API сервиса Hotels
def api_request(method_endswith, params, method_type):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
    }
    try:
        response = requests.request(method_type, url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который поможет найти отели в нужном городе. Введите название города, например: Рига")

# Обработчик сообщений
def search_hotels(update, context):
    try:
        city_name = update.message.text
        params = {
            "query": city_name,
            "locale": "ru_RU",
            "adults1": 1,
            "pageNumber": 1
        }
        search_results = api_request("locations/v1/search", params, "GET")
        if search_results is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="К сожалению, не удалось найти информацию о городе. Попробуйте еще раз.")
            return
        location_id = search_results["suggestions"][0]["entities"][0]["destinationId"]
        params = {
            "destinationId": location_id,
            "pageSize": 5,
            "adults1": 1,
            "pageNumber": 1
        }
        properties_results = api_request("properties/v2/list", params, "GET")
        if properties_results is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="К сожалению, не удалось найти отели в данном городе. Попробуйте еще раз.")
            return
        hotels = properties_results["data"]["body"]["searchResults"]["results"]
        if not hotels
