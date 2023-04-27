from telebot.handler_backends import State, StatesGroup



class CityInformation(StatesGroup):
    price_range = State()
    date_range = State()
    city = State()
    city_count = State()
    id_city = State()
    property_id = State()
    property_details = State()

class UserInfoState(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()
