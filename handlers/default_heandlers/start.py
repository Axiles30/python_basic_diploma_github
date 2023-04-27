from telebot.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, Update

from loader import bot

@bot.message_handler(commands=['start'])
def send_welcome(message):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    low_btn = InlineKeyboardButton(text='Low', callback_data='lowprice', )
    high_btn = InlineKeyboardButton(text='High', callback_data='high')
    custom_btn = InlineKeyboardButton(text='Custom', callback_data='custom')
    history = InlineKeyboardButton(text='History', callback_data='history')
    inline_markup.add(low_btn, high_btn, custom_btn, history)
    bot.send_message(message.chat.id, 'Этот бот занимается поиском отелей.\n'
                                      '\nНажмите Low если хотите получить отели по самым низким ценам.\n'
                                      '\nНажмите High если хотите получить отели по самым высоким ценам.\n'
                                      '\nНажмите Custom  Диапазон значений выборки (цена от и до, расстояние от и до, срок от и до и так далее).'
                                      'Количество единиц категории (товаров/услуг), которые необходимо вывести (не больше заранее определённого программно максимума).\n'
                                      '\nНажмите History После ввода команды выводится краткая история запросов пользователя (последние десять запросов).', reply_markup=inline_markup)
    return inline_markup
#
# markup = ReplyKeyboardMarkup()
# high_btn = KeyboardButton(text='/high')
# custom_btn = KeyboardButton(text='/custom')
# history = KeyboardButton(text='/history')
# markup.add(low_btn, high_btn, custom_btn, history)