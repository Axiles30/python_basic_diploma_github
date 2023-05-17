import json

import requests
from telebot.handler_backends import StatesGroup, State
from telebot.types import Message

# from api.request_api_parts.locations_search import gaia_id
from loader import bot

states_dict = {}
# all_property_dicts = {'data' : []}

class MyStates(StatesGroup):
    # Just name variables differently
    city = State() # creating instances of State class is enough from now
    hotels = State()
    upper_limit = State()
    lower_limit = State()
    check_in_date = State()
    check_out_date = State()

# @bot.callback_query_handler(func=lambda call: call.data == 'lowprice')
# def handle_lowprice_query(call: CallbackQuery):
#     get_city(call.message)

@bot.message_handler(commands=['go'])
def get_city(message: Message) -> None:
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} '
                                           f'в каком городе будем искать отели?')


@bot.message_handler(state=MyStates.city)
def hotel_count(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id,
                         'Теперь введите количество отелей которые хотите увидеть.')
        bot.set_state(message.from_user.id, MyStates.hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
            states_dict['city'] = data['city']
    else:
        bot.send_message(message.from_user.id, 'Город можно вводить только буквами.')
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": f"{data['city']}",
                   "locale": "en_US",
                   "langid": "1033",
                   "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == requests.codes.ok:
        # print(f'Response status {response.status_code}ок')
        data = response.json()
        with open('database\json_files\locations_search.json', 'w') as file:
            json.dump(data, file, indent=4)

        with open('database\json_files\locations_search.json', 'r') as file:
            data = json.load(file)

    else:
        print('Ошибка при выполнении запроса')

    gaia_id = data['sr'][0]['gaiaId']
    states_dict['gaiaId'] = gaia_id
@bot.message_handler(state=MyStates.hotels)
def get_hotel_count(message: Message) -> None:
        bot.send_message(message.from_user.id,
                         'Теперь введите верхнюю границу стоимости за ночь в долларах.')
        bot.set_state(message.from_user.id, MyStates.upper_limit, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_count'] = int(message.text)
            states_dict['hotel_count'] = data['hotel_count']
            # all_property_dicts['data'].append(states_dict)

        with open('database\json_files\city_and_hotels_count.json', 'w') as file:
             json.dump(states_dict, file, indent=4)

@bot.message_handler(state=MyStates.upper_limit)
def upper_limit(message: Message) -> None:

        bot.send_message(message.from_user.id,
                         'Теперь введите нижнюю границу стоимости за ночь в долларах.')
        bot.set_state(message.from_user.id, MyStates.lower_limit, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['upper_limit'] = int(message.text)
            states_dict['upper_limit'] = data['upper_limit']

@bot.message_handler(state=MyStates.lower_limit)
def lower_limit(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Теперь введите желаемую дату заезда.(в формате число-месяц-год, 15-06-23)')
    bot.set_state(message.from_user.id, MyStates.check_in_date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['lower_limit'] = int(message.text)
        states_dict['lower_limit'] = data['lower_limit']
        # print(states_dict)

@bot.message_handler(state=MyStates.check_in_date)
def check_in_date(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Теперь введите дату выезда.(в формате число-месяц-год, 30-06-23)')
    bot.set_state(message.from_user.id, MyStates.check_out_date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_in_date'] = message.text
        states_dict['check_in_date'] = data['check_in_date']
        print('Срока 87: ',states_dict['check_in_date'])

@bot.message_handler(state=MyStates.check_out_date)
def check_out_date(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_out_date'] = message.text
        states_dict['check_out_date'] = data['check_out_date']
        print('Срока 94: ',states_dict['check_out_date'])
    with open('database\json_files\city_and_hotels_count.json', 'w') as file:
        json.dump(states_dict, file, indent=4)
        print('Срока 97: ',states_dict)
    with open('database\json_files\city_and_hotels_count.json', 'r') as file:
        data = json.load(file)

    check_in_date = data["check_in_date"]
    day_in, month_in, year_in = check_in_date.split('-')
    day_in = int(day_in)
    month_in = int(month_in)
    year_in = int(year_in)

    check_out_date = data["check_out_date"]
    day_out, month_out, year_out = check_out_date.split('-')
    day_out = int(day_out)
    month_out = int(month_out)
    year_out = int(year_out)

    data["check_in_date"] = {'day': day_in, 'month': month_in, 'year': year_in}
    data["check_out_date"] = {'day': day_out, 'month': month_out, 'year': year_out}
    with open('database\json_files\city_and_hotels_count.json', 'w') as file:
        json.dump(data, file, indent=4)
    with open('database\json_files\city_and_hotels_count.json', 'r') as file:
        data = json.load(file)
    city = data['city']
    gaia_id = data['gaiaId']
    hotel_count = data["hotel_count"]
    upper_limit = data["upper_limit"]
    lower_limit = data["lower_limit"]
    day_in = data["check_in_date"]["day"]
    month_in = data["check_in_date"]["month"]
    year_in = data["check_in_date"]["year"]
    day_out = data["check_out_date"]["day"]
    month_out = data["check_out_date"]["month"]
    year_out = data["check_out_date"]["year"]
    print(type(hotel_count), hotel_count,
          type(upper_limit), upper_limit,
          type(lower_limit), lower_limit,
          type(day_in), day_in,
          type(month_in), month_in,
          type(year_in), year_in,
          type(day_out), day_out,
          type(month_out), month_out,
          type(year_out), year_out)
    property_search(message,gaia_id, city, hotel_count,  upper_limit, lower_limit, day_in, month_in, year_in, day_out, month_out, year_out)
def property_search(message: Message, gaia_id = str, city = str, hotel_count = int,
                     upper_limit = int, lower_limit = int, day_in = int,
                     month_in = int, year_in = int, day_out = int, month_out = int, year_out= int):

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": f'{gaia_id}'},
        "checkInDate": {
            "day": day_in,
            "month": month_in,
            "year": year_in
        },
        "checkOutDate": {
            "day": day_out,
            "month": month_out,
            "year": year_out
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": hotel_count,
        "sort": "PRICE_HIGH_TO_LOW",
        "filters": {"price": {
            "max": upper_limit,
            "min": lower_limit
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print('Строка 139: ', response.status_code)
    # logging.debug(response.status_code)
    data = response.json()
    # print(data)
    with open('database\json_files\properties_list.json', 'w') as file:
        json.dump(data, file, indent=4)

    all_property_dicts = {'city': f"{city}", 'data': []}
    x = 0
    dict_id = 0

    for i in range(hotel_count):
        with open('database\json_files\properties_list.json', 'r') as file:
            data = json.load(file)
        property_id = data['data']['propertySearch']['properties'][i]['id']
        property_name = data['data']['propertySearch']['properties'][i]['name']
        property_image = data['data']['propertySearch']['properties'][i]['propertyImage']['image']['url']
        price_per_day = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][0]['lineItems'][0]['price']['formatted']
        property_all_price = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][1]['lineItems'][0]['value']
        property_dict = {'id': property_id, 'name': property_name, 'image': property_image,'price_per_day': price_per_day, 'price_all': property_all_price}
        dict_id += 1

        all_property_dicts['data'].append(property_dict)


    with open("database\json_files\search_five_hotels.json", 'w') as file:
        json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
        x += 1

    with open('database\json_files\search_five_hotels.json', 'r') as file:
        data = json.load(file)
    media_group = []

    # Перебрать отели в данных
    for hotel in data["data"]:
        # Получить изображение отеля
        photo_url = hotel['image']
        # Получить название и цену отеля
        caption = f"{hotel['name']}\n{hotel['price_per_day']}\n{hotel['price_all']}"
        # Добавить фото и описание в список медиа-сообщений
        media_group.append({'type': 'photo', 'media': photo_url, 'caption': caption})
        print(media_group)
        # logging.debug(media_group)
        bot.send_photo(message.chat.id, hotel['image'], hotel['name'])
        bot.send_message(message.chat.id, f"Стоимость за ночь : {hotel['price_per_day']}")
        bot.send_message(message.chat.id, f"Общая стоимость : {hotel['price_all']}")




