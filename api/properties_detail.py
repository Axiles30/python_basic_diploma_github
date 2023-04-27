import json

import requests
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

response = requests.request("POST", url, json=payload, headers=headers, timeout=10)


data = response.json()

with open('properties_detail.json', 'w') as file:
	json.dump(data, file, indent=4)

with open('properties_detail.json', 'r') as file:
	data = json.load(file)

print(response.text)