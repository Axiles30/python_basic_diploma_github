from telebot.handler_backends import State, StatesGroup



class TravelInformation(StatesGroup):
    city = State()
    hotels = State()
    id_city = State()
    property_id = State()
    property_details = State()
    upper_limit = State()
    lower_limit = State()
    check_in_date = State()
    check_out_date = State()

