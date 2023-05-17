import json

import requests
from telebot.types import Message

from properties_list import property_id

url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": f"{property_id}"
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "bb9597ea42mshb69177d742fd63fp168fe1jsne7d3e84fcb47",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
with open('../../database/json_files/city_and_hotels_count.json', 'r') as file:
    data = json.load(file)
    all_property_dicts = {'city' : f'{data["city"]}', 'data' : []}


response = requests.request("POST", url, json=payload, headers=headers, timeout=10)
data = response.json()
with open('../../database/json_files/properties_detail.json', 'w') as file:
    json.dump(data, file, indent=4)

# with open('properties_detail.json', 'r') as file:
#     data = json.load(file)
    # property_gallery = data['data']['propertyInfo']['propertyGallery']['images'][0]['image']['url']
    # print(property_gallery)

for i in range(10):
    with open('../../database/json_files/properties_detail.json', 'r') as file:
        data = json.load(file)
    property_id = data['data']['propertyInfo']['summary']['id']
    property_name = data['data']['propertyInfo']['summary']['name']
    property_image = data['data']['propertyInfo']['propertyGallery']['images'][i]['image']['url']
    property_description = data['data']['propertyInfo']['propertyGallery']['images'][i]['image']['description']
    property_dict = {'id' : property_id, 'name' : property_name, 'image' : property_image, 'description' : property_description}
    # dict_id += 1

    all_property_dicts['data'].append(property_dict)
    # else:
    #     print("Ошибка: результаты должны быть числом")

    with open("../../database/json_files/one_hotel_details.json", 'w') as file :
        json.dump(all_property_dicts, file, indent=4, separators=(',', ':'))
        # x += 1

    with open('../../database/json_files/one_hotel_details.json', 'r') as file :
        data = json.load(file)

# print(property_gallery)
