import json
from pprint import pprint

import requests

from handlers.custom_heandlers.lowprice import city

url = "https://hotels4.p.rapidapi.com/properties/v2/list"

payload = {'currency': 'USD',
           'eapid': 1,
           'locale': '',
           'siteId': 300000001,
           'destination': {
               'regionId': '2302' # id из первого запроса
           },
           'checkInDate': {'day': 5, 'month': 12, 'year': 2023},
           'checkOutDate': {'day': 10, 'month': 12, 'year': 2023},
           'rooms': [{'adults': 1}],
           'resultsStartingIndex': 0,
           'resultsSize': 5,
           'sort': 'PRICE_LOW_TO_HIGH',
           'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
           }
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)
data = response.json()
with open('properties_list.json', 'w') as file:
	json.dump(data, file, indent=4)




all_property_dicts = {'city' : 'Milan', 'data' : []}
x = 0
dict_id = 0


for i in range(payload['resultsSize']):
		with open('properties_list.json', 'r') as file :
			data = json.load(file)
		property_id = data['data']['propertySearch']['properties'][i]['id']
		property_name = data['data']['propertySearch']['properties'][i]['name']
		property_image = data['data']['propertySearch']['properties'][i]['propertyImage']['image']['url']
		property_price = data['data']['propertySearch']['properties'][i]['price']['displayMessages'][1]['lineItems'][0]['value']
		property_dict = {'id': property_id, 'name' : property_name, 'image' : property_image, 'price' : property_price}
		dict_id += 1

		all_property_dicts['data'].append(property_dict)

with open('search_five_hotels.json', 'w') as file:
	json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
	x += 1


with open('search_five_hotels.json', 'r') as file:
		data = json.load(file)

# for hotel in data['data']:
# 	x += 1
# 	print(f"{hotel['name']} : {hotel['price']}\n{hotel['image']}\n")


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

# Отправить группу медиа-сообщений
print(media_group)