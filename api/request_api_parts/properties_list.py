import json
from pprint import pprint

import requests

# from handlers.custom_heandlers.lowprice import city
# city_input = input('Город: ')
# hotels_count = int(input('Количество отелей: '))

with open('../../database/json_files/city_and_hotels_count.json', 'r') as file:
    data = json.load(file)

checkindate = data["check_in_date"]
day_in, month_in, year_in = checkindate.split('-')

checkoutdate = data["check_out_date"]
day_out, month_out, year_out = checkoutdate.split('-')

with open('../../database/json_files/city_and_hotels_count.json', 'r') as file:
    data = json.load(file)
upper_limit = data['upper_limit']
lower_limit = data['lower_limit']

with open('../../database/json_files/locations_search.json', 'r') as file:
    data = json.load(file)
gaia_id = data['sr'][0]['gaiaId']

with open('../../database/json_files/city_and_hotels_count.json', 'r') as file:
    data = json.load(file)

hotels_count = data['hotel_count']
url = "https://hotels4.p.rapidapi.com/properties/v2/list"

payload = {
        "currency" : "USD",
        "eapid" : 1,
        "locale" : "ru_RU",
        "siteId" : 300000001,
        "destination" : {"regionId" : f"{gaia_id}"},
        "checkInDate" : {
            "day" : int(day_in),
            "month" : int(month_in),
            "year" : int(year_in)
        },
        "checkOutDate" : {
            "day" : int(day_out),
            "month" : int(month_out),
            "year" : int(year_out)
        },
        "rooms" : [
            {
                "adults" : 2,
                "children" : [{"age" : 5}, {"age" : 7}]
            }
        ],
        "resultsStartingIndex" : 0,
        "resultsSize" : hotels_count,
        "sort" : "PRICE_LOW_TO_HIGH",
        "filters" : {"price" : {
            "max" : upper_limit,
            "min" : lower_limit
        }}
    }
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

# print(payload)

response = requests.request("POST", url, json=payload, headers=headers)
# print(response)
data = response.json()
with open('../../database/json_files/properties_list.json', 'w') as file:
    json.dump(data, file, indent=4)

with open('../../database/json_files/properties_list.json', 'r') as file:
    data = json.load(file)
    property_id = data['data']['propertySearch']['properties'][1]['id']

# print(property_id)
#
#
#
#
# all_property_dicts = {'city' : f'{data["city"]}', 'data' : []}
# x = 0
# dict_id = 0
#
#
# for i in range(data["hotels"]):
# 		with open('properties_list.json', 'r') as file :
# 			data = json.load(file)
# 		property_id = data['data']['propertySearch']['properties'][i]['id']
# 		property_name = data['data']['propertySearch']['properties'][i]['name']
# 		property_image = data['data']['propertySearch']['properties'][i]['propertyImage']['image']['url']
# 		property_price = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][1]['lineItems'][0]['value']
# 		property_dict = {'id': property_id, 'name' : property_name, 'image' : property_image, 'price' : property_price}
# 		dict_id += 1
#
# 		all_property_dicts['data'].append(property_dict)
#
# with open('search_five_hotels.json', 'w') as file:
# 	json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
# 	x += 1
#
#
# with open('search_five_hotels.json', 'r') as file:
# 		data = json.load(file)
#
# # for hotel in data['data']:
# # 	x += 1
# # 	print(f"{hotel['name']} : {hotel['price']}\n{hotel['image']}\n")
#
#
# # Создать список медиа-сообщений
# media_group = []
#
# # Перебрать отели в данных
# for hotel in data["data"]:
#     # Получить изображение отеля
#     photo_url = hotel['image']
#     # Получить название и цену отеля
#     caption = f"{hotel['name']}\n{hotel['price']}"
#
#     # Добавить фото и описание в список медиа-сообщений
#     media_group.append({'type': 'photo', 'media': photo_url, 'caption': caption})
#
# # Отправить группу медиа-сообщений
# print(media_group)
