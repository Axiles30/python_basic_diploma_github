import types

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message

from loader import bot
import json
import os
import requests

from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_information import UserInfoState, CityInformation
from telebot.types import Message

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message: Message) -> None:
    bot.send_message(message.chat.id, 'Неизвестная команда. Попробуйте еще раз.')

@bot.message_handler(commands=['buttons'])
def send_welcome(message) :
	markup = ReplyKeyboardMarkup()
	inline_markup = InlineKeyboardMarkup()
	low_btn = InlineKeyboardButton(text='/low')
	high_btn = KeyboardButton(text='/high')
	custom_btn = KeyboardButton(text='/custom')
	history = KeyboardButton(text='/history')
	markup.add(low_btn, high_btn, custom_btn, history)
	inline_markup.add(low_btn)
	bot.send_message(message.chat.id, 'Что умеет бот', reply_markup=markup)

@bot.message_handler(commands = ['buttons'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт хабра", reply_markup = markup)

