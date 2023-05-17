import json
from pprint import pprint
import typing as t
from states import contact_information
import requests

with open('database\json_files\city_and_hotels_count.json', 'r') as file:
    data = json.load(file)
    # print(data)

url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q":f"{data['city']}",
               "locale":"en_US",
               "langid":"1033",
               "siteid":"300000001"}

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
# print(gaia_id)

#
# for item in data["sr"]:
#     print(item["regionNames"]["fullName"])
# print(type(lowprice_search))