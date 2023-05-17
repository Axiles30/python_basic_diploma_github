import json

import requests

# with open('city_and_hotels_count.json', 'r') as file:
#     data = json.load(file)
#
# check_in_date = data["check_in_date"]
# day_in = check_in_date['day']
# month_in = check_in_date['month']
# year_in = check_in_date['year']
#
# check_out_date = data["check_out_date"]
# day_out = check_out_date['day']
# month_out = check_out_date['month']
# year_out = check_out_date['year']
#
# # Обновление значений
# data["check_in_date"] = {'day': int(day_in), 'month': int(month_in), 'year': int(year_in)}
# data["check_out_date"] = {'day': int(day_out), 'month': int(month_out), 'year': int(year_out)}
#
# with open('city_and_hotels_count.json', 'w') as file:
#     json.dump(data, file, indent=4)
#
# with open('city_and_hotels_count.json', 'r') as file:
#     data = json.load(file)
#     print(data["check_out_date"])

# import json
#
# with open('city_and_hotels_count.json', 'r') as file:
#     data = json.load(file)
#
# check_in_date = data["check_in_date"]
# day_in, month_in, year_in = check_in_date.split('-')
# day_in = int(day_in)
# month_in = int(month_in)
# year_in = int(year_in)
#
# check_out_date = data["check_out_date"]
# day_out, month_out, year_out = check_out_date.split('-')
# day_out = int(day_out)
# month_out = int(month_out)
# year_out = int(year_out)
#
#
# data["check_in_date"] = {'day': day_in, 'month': month_in, 'year': year_in}
# data["check_out_date"] = {'day': day_out, 'month': month_out, 'year': year_out}
# with open('city_and_hotels_count.json', 'w') as file:
#     json.dump(data, file, indent=4)
# with open('city_and_hotels_count.json', 'r') as file:
#     data = json.load(file)
#     print(data["check_out_date"])
#
# print(day_in)
# print(month_in)
# print(year_in)
#
# print(type(day_in))
# print(type(month_in))
# print(type(year_in))

# {
#     "city": "Paris",
#     "hotel_count": 3,
#     "upper_limit": 1000,
#     "lower_limit": 500,
#     "check_in_date": "15-06-2023",
#     "check_out_date": "30-06-2023"
# }

states_dict = {}

# with open('city_and_hotels_count.json', 'r') as file:
#     data = json.load(file)
#
# check_in_date = data["check_in_date"]
# day_in, month_in, year_in = check_in_date.split('-')
# day_in = int(day_in)
# month_in = int(month_in)
# year_in = int(year_in)
#
# check_out_date = data["check_out_date"]
# day_out, month_out, year_out = check_out_date.split('-')
# day_out = int(day_out)
# month_out = int(month_out)
# year_out = int(year_out)
#
# data["check_in_date"] = {'day': day_in, 'month': month_in, 'year': year_in}
# data["check_out_date"] = {'day': day_out, 'month': month_out, 'year': year_out}
# with open('city_and_hotels_count.json', 'w') as file:
#     json.dump(data, file, indent=4)
with open('../../database/json_files/city_and_hotels_count.json', 'r') as file:
    data = json.load(file)
city = data['city']
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

url = "https://hotels4.p.rapidapi.com/properties/v2/list"
payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001,
    "destination": {"regionId": '2302'},
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
    "sort": "PRICE_LOW_TO_HIGH",
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
# print('Строка 139: ', response.status_code)
# logging.debug(response.status_code)
data = response.json()
# print(data)
with open('../../database/json_files/properties_list.json', 'w') as file:
    json.dump(data, file, indent=4)

all_property_dicts = {'city': f"{city}", 'data': []}
x = 0
dict_id = 0

# print('Строка 151: ', type(hotel_count_search))
# print('Строка 152: ',type(payload["resultsSize"]))

# logging.debug(payload["resultsSize"])

# if isinstance(hotel_count_search, int):
for i in range(hotel_count):
    with open('../../database/json_files/properties_list.json', 'r') as file:
        data = json.load(file)
    property_id = data['data']['propertySearch']['properties'][i]['id']
    # print('Строка 157',property_id)
    property_name = data['data']['propertySearch']['properties'][i]['name']
    property_image = data['data']['propertySearch']['properties'][i]['propertyImage']['image']['url']
    property_price = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][1]['lineItems'][0][
        'value']
    property_dict = {'id': property_id, 'name': property_name, 'image': property_image, 'price': property_price}
    dict_id += 1

    all_property_dicts['data'].append(property_dict)
# else:
#     print("Ошибка: результаты должны быть числом")

with open("../../database/json_files/search_five_hotels.json", 'w') as file:
    json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
    x += 1

with open('../../database/json_files/search_five_hotels.json', 'r') as file:
    data = json.load(file)
for hotel in data['data']:
    x += 1
    # print(f"{hotel['name']} : {hotel['price']}\n{hotel['image']}\n")

media_group = []

# Перебрать отели в данных
for hotel in data["data"]:
    # Получить изображение отеля
    photo_url = hotel['image']
    # Получить название и цену отеля
    caption = f"{hotel['name']}\n{hotel['price']}"
    # Добавить фото и описание в список медиа-сообщений
    media_group.append({'type': 'photo', 'media': photo_url, 'caption': caption})
    # print(media_group)
    # logging.debug(media_group)
    # bot.send_photo(message.chat.id, hotel['image'], hotel['name'])
    # bot.send_message(message.chat.id, hotel['price'])