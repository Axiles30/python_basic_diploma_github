from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
# @bot.message_handler(state=None)
# def bot_echo(message: Message):
#     bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
#                           f"{message.text}")

# import telebot
#
#
# bot = telebot.TeleBot('5225115438:AAFZYynSqHf9AT1Fdp39haWePrAznPcldIE')
#
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message) :
#     if message.text == "Привет" or message.text == "привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help" :
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else :
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
#
#
#
# bot.polling(none_stop=True, interval=0)