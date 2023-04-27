import json
import os
import requests

from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_information import UserInfoState, CityInformation
from telebot.types import Message


@bot.message_handler(commands=['go'])
def city(message: Message) -> None:
    """Получение города от пользователя"""
    bot.set_state(message.from_user.id, CityInformation.city, message.chat.id)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username} в каком городе будем искать отели?')


@bot.message_handler(state=CityInformation.city)
def get_id_city(message: Message) -> None:
    """Получение ID города"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        city_search = data['city']
    bot.set_state(message.from_user.id, CityInformation.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Произвожу поиск в городе: {message.text}')
    print(data['city'])
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": f"{data['city']}", "locale": "en_US", "langid": "1033", "siteid": "300000001"}
        headers = {
            "X-RapidAPI-Key": f"{os.getenv('RAPID_API_KEY')}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.status_code)
        # print(response.text)

        if response.status_code == requests.codes.ok:
            # print(f'Response status {response.status_code}ок')
            data = response.json()
            with open('api\locations_search.json', 'w') as file:
                json.dump(data, file, indent=4)
            with open('api\locations_search.json', 'r') as file:
                data = json.load(file)
        else:
            print('Ошибка при выполнении запроса')
    data = data

    gaia_id = data['sr'][0]['gaiaId']
    get_property_id(message, gaia_id, city_search)


@bot.message_handler(state=CityInformation.id_city)
def get_property_id(message: Message, gaia_id=str, city_search=str) -> None:
    """Получение ID Отеля"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id_city'] = message.text
    bot.set_state(message.from_user.id, CityInformation.id_city, message.chat.id)
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": f"{gaia_id}"},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2023
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2023
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 5,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 5000,
            "min": 150
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.status_code)
    data = response.json()
    # print(data)
    with open('api\properties_list.json', 'w') as file:
        json.dump(data, file, indent=4)

    all_property_dicts = {'city': f"{city_search}", 'data': []}
    x = 0
    dict_id = 0

    for i in range(payload['resultsSize']):
        with open('api\properties_list.json', 'r') as file:
            data = json.load(file)
        property_id = data['data']['propertySearch']['properties'][i]['id']
        property_name = data['data']['propertySearch']['properties'][i]['name']
        property_image = data['data']['propertySearch']['properties'][i]['propertyImage']['image']['url']
        property_price = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][1]['lineItems'][0][
            'value']
        property_dict = {'id': property_id, 'name': property_name, 'image': property_image, 'price': property_price}
        dict_id += 1

        all_property_dicts['data'].append(property_dict)

    with open("api\search_five_hotels.json", 'w') as file:
        json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
        x += 1

    with open('api\search_five_hotels.json', 'r') as file:
        data = json.load(file)
    # for hotel in data['data'] :
    #     x += 1
    # print(f"{hotel['name']} : {hotel['price']}\n{hotel['image']}\n")
    # Создать список медиа-сообщений
    media_group = []

    # Перебрать отели в данных
    for hotel in data["data"]:
        # Получить изображение отеля
        photo_url = hotel['image']
        # Получить название и цену отеля
        caption = f"{hotel['name']}\n{hotel['price']}"
        # Добавить фото и описание в список медиа-сообщений
        media_group.append({'type': 'photo', 'media': photo_url, 'caption': caption})
        print(media_group)
        bot.send_photo(message.chat.id, hotel['image'], hotel['name'])
        bot.send_message(message.chat.id, hotel['price'])

@bot.message_handler(commands=['test'])
def city(message: Message) -> None:
    """Получение города от пользователя"""
    bot.set_state(message.from_user.id, CityInformation.city, message.chat.id)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username} в каком городе будем искать отели?')

@bot.message_handler(state=CityInformation.city)
def get_id_city(message: Message) -> None:
    """Получение ID города"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        city_search = data['city']
    bot.set_state(message.from_user.id, CityInformation.date_range, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите диапазон дат в формате "дд.мм.гггг-дд.мм.гггг"')

@bot.message_handler(state=CityInformation.date_range)
def get_date_range(message: Message) -> None:
    """Получение диапазона дат"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['date_range'] = message.text
        date_range = data['date_range']
    bot.set_state(message.from_user.id, CityInformation.price_range, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите диапазон цен в формате "минимальная цена-максимальная цена"')

@bot.message_handler(state=CityInformation.price_range)
def get_price_range(message: Message) -> None:
    """Получение диапазона цен"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_range'] = message.text
        price_range = data['price_range']
    bot.send_message(message.from_user.id, f'Ищу отели в городе {data["city"]} с {data["date_range"]} по цене от {data["price_range"]}')
    # Здесь можно добавить вызов функции поиска отелей с указанными параметрами


@bot.message_handler(state=CityInformation.city)
def get_id_city(message: Message) -> None:
    """Получение ID города"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data :
        data['city'] = message.text
        city_search = data['city']
    bot.set_state(message.from_user.id, CityInformation.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Произвожу поиск в городе: {message.text}')
    print(data['city'])
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q" : f"{data['city']}","locale":"en_US", "langid" : "1033", "siteid" : "300000001"}
        headers = {
            "X-RapidAPI-Key" : f"{os.getenv('RAPID_API_KEY')}",
            "X-RapidAPI-Host" : "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.status_code)
        # print(response.text)

        if response.status_code == requests.codes.ok :
            # print(f'Response status {response.status_code}ок')
            data = response.json()
            with open('api\locations_search.json', 'w') as file:
                json.dump(data, file, indent=4)
            with open('api\locations_search.json', 'r') as file:
                data = json.load(file)
        else :
            print('Ошибка при выполнении запроса')
    data = data

    gaia_id  = data['sr'][0]['gaiaId']
    get_property_id(message, gaia_id, city_search)


@bot.message_handler(state=CityInformation.id_city)
def get_property_id(message: Message, gaia_id = str, city_search = str) -> None:
    """Получение ID Отеля"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data :
        data['id_city'] = message.text
    bot.set_state(message.from_user.id, CityInformation.id_city, message.chat.id)
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency" : "USD",
        "eapid" : 1,
        "locale" : "ru_RU",
        "siteId" : 300000001,
        "destination" : {"regionId" : f"{gaia_id}"},
        "checkInDate" : {
            "day" : 10,
            "month" : 10,
            "year" : 2023
        },
        "checkOutDate" : {
            "day" : 15,
            "month" : 10,
            "year" : 2023
        },
        "rooms" : [
            {
                "adults" : 2,
                "children" : [{"age" : 5}, {"age" : 7}]
            }
        ],
        "resultsStartingIndex" : 0,
        "resultsSize" : 5,
        "sort" : "PRICE_LOW_TO_HIGH",
        "filters" : {"price" : {
            "max" : 5000,
            "min" : 150
        }}
    }
    headers = {
        "content-type" : "application/json",
        "X-RapidAPI-Key" : "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
        "X-RapidAPI-Host" : "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.status_code)
    data = response.json()
    # print(data)
    with open('api\properties_list.json', 'w') as file :
        json.dump(data, file, indent=4)


    all_property_dicts = {'city' : f"{city_search}", 'data' : []}
    x = 0
    dict_id = 0

    for i in range(payload['resultsSize']) :
        with open('api\properties_list.json', 'r') as file :
            data = json.load(file)
        property_id = data['data']['propertySearch']['properties'][i]['id']
        property_name = data['data']['propertySearch']['properties'][i]['name']
        property_image = data['data']['propertySearch']['properties'][i]['propertyImage']['image']['url']
        property_price = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][1]['lineItems'][0][
            'value']
        property_dict = {'id' : property_id, 'name' : property_name, 'image' : property_image, 'price' : property_price}
        dict_id += 1

        all_property_dicts['data'].append(property_dict)

    with open("api\search_five_hotels.json", 'w') as file :
        json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
        x += 1

    with open('api\search_five_hotels.json', 'r') as file :
        data = json.load(file)
    # for hotel in data['data'] :
    #     x += 1
        # print(f"{hotel['name']} : {hotel['price']}\n{hotel['image']}\n")
        # Создать список медиа-сообщений
    media_group = []

        # Перебрать отели в данных
    for hotel in data["data"] :
        # Получить изображение отеля
        photo_url = hotel['image']
        # Получить название и цену отеля
        caption = f"{hotel['name']}\n{hotel['price']}"
        # Добавить фото и описание в список медиа-сообщений
        media_group.append({'type' : 'photo', 'media' : photo_url, 'caption' : caption})
        print(media_group)
        bot.send_photo(message.chat.id, hotel['image'], hotel['name'])
        bot.send_message(message.chat.id, hotel['price'])


# def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
#                 params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
#                 method_type  # Метод\тип запроса GET\POST
#                 ):
#     url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
#
#     # В зависимости от типа запроса вызываем соответствующую функцию
#     if method_type == 'GET':
#         return get_request(
#             url=url,
#             params=params
#         )
#     else:
#         return post_request(
#             url=url,
#             params=params
#         )
#
#
# def get_request(url, params):
#     try:
#         response = get(
#             url,
#             headers=...,
#             params=params,
#             timeout=15
#         )
#         if response.status_code == requests.codes.ok:
#             return response.json()
#     except ...
#         ...
#

# requests.get( ...timeout=10)
