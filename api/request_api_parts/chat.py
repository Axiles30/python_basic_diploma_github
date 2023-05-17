from telebot.types import Message

from loader import bot
from states.contact_information import CityInformation


@bot.message_handler(state=CityInformation.id_city)
def get_property_id(message: Message, gaia_id=str, city_search=str, city_count_search=int) -> None:
    """Получение ID Отеля"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["id_city"] = message.text
        # запрашиваем у пользователя количество отелей, которое он хочет получить
        bot.send_message(message.from_user.id, "Сколько отелей вы хотите получить?")
        # меняем состояние пользователя на ожидание ввода количества отелей
        bot.set_state(message.from_user.id, CityInformation.hotel_count, message.chat.id)

@bot.message_handler(state=CityInformation.hotel_count)
def get_hotel_count(message: Message) -> None:
    """Получение количества отелей"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["hotel_count"] = int(message.text)
    bot.set_state(message.from_user.id, CityInformation.hotel_count, message.chat.id)
    # здесь вы можете добавить код для выполнения запроса на API отелей, используя
    # количество отелей, которое ввел пользователь, например:
    # ...
    # "resultsSize": data["hotel_count"],
    # ...
    # после этого, вы можете продолжить реализацию функции, например:
    # ...
    # response = requests.request("POST", url, json=payload, headers=headers)
    # print(response.status_code)
    # data = response.json()
    # ...