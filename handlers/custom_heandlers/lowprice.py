import json
import os
import requests
from loader import bot
from states.contact_information import UserInfoState, CityInformation
from telebot.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    CallbackQuery
from handlers.default_heandlers.start import send_welcome

"""
Команда /low
После ввода команды у пользователя запрашивается:
1. Услуга/товар, по которым будет проводиться поиск (самая низкая стоимость,
самые доступные авто, самое близкое местоположение и так далее).
2. Количество единиц категории (товаров/услуг), которое необходимо вывести (не
больше программно определённого максимума).
"""


@bot.callback_query_handler(func=lambda call: call.data == 'lowprice')
def handle_lowprice_query(call: CallbackQuery):
    city(call.message)


def city(message: Message) -> None:
    """Получение города от пользователя"""
    bot.send_message(message.chat.id, f'Привет, {message.chat.username} в каком городе будем искать отели?')
    bot.set_state(message.chat.id, CityInformation.city, message.chat.id)
    bot.register_next_step_handler(message, city_count)

    
def city_count(message: Message) -> int:
    """Получение количество городов от пользователя"""
    bot.send_message(message.chat.id, f'Сколько отелей вы хотите увидеть?')
    bot.set_state(message.chat.id, CityInformation.city_count, message.chat.id)
    bot.register_next_step_handler(message, get_city_count)
@bot.message_handler(state=CityInformation.city_count)
def get_city_count(message: Message) -> int:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city_count'] = message.text
        city_count_search = data['city_count']
        city_count_search = int(city_count_search)

    print("data['city_count']",data['city_count'])
    # print(type(city_count_search))
    get_property_id(message, city_count_search)
    bot.register_next_step_handler(message, get_id_city)


@bot.message_handler(state=CityInformation.city)
def get_id_city(message: Message) -> None:
    """Получение ID города"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data :
        data['city'] = message.text
        city_search = data['city']
    bot.send_message(message.from_user.id, f'Произвожу поиск в городе: {message.text}')
    bot.set_state(message.from_user.id, CityInformation.city, message.chat.id)
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
def get_property_id(message: Message, gaia_id = str, city_search = str, city_count_search = int) -> None:
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
        "resultsSize" : f"{city_count_search}",
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

    print(payload["resultsSize"])

    for i in range(payload["resultsSize"]) :
        with open('api\properties_list.json', 'r') as file:
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
    # Вот реализация:
    # photos = []
    # for j in range(c):
    #     photos.insert(j, post_media[j]['photo']['src_xxbig'])
    #     bot.send_media_group(channel_name, photos)
    #
    #
    # print(data)
    # property_id = data['data']['propertySearch']['properties'][0]['id']
    # print(property_id)
    # get_property_details(message, property_id)

# @bot.message_handler(state=CityInformation.property_details)
# def get_property_details(message: Message, property_id = str) -> None:
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data :
#         data['property_details'] = message.text
#     bot.set_state(message.from_user.id, CityInformation.property_details, message.chat.id)
#     url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
#     payload = {
#         "currency" : "USD",
#         "eapid" : 1,
#         "locale" : "en_US",
#         "siteId" : 300000001,
#         "propertyId" : f"{property_id}"
#     }
#     headers = {
#         "content-type" : "application/json",
#         "X-RapidAPI-Key" : "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
#         "X-RapidAPI-Host" : "hotels4.p.rapidapi.com"
#     }
#
#     response = requests.request("POST", url, json=payload, headers=headers)
#
#     data = response.json()
#
#     with open('api\properties_detail.json', 'w') as file :
#         json.dump(data, file, indent=4)
#
#     with open('api\properties_detail.json', 'r') as file :
#         data = json.load(file)
#
#     property_gallery = data['data']['propertyInfo']['propertyGallery']['images'][0]['image']['url']
#     for item in data["data"]['propertyInfo']['summary']:
#         print(item['name'])
    # bot.send_message(message.chat.id, property_gallery)
    # print(property_gallery)

