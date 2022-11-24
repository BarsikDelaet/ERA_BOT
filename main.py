__author__ = "Барсуков М.О."

import telebot
import config
import time
from telebot import types
from func_buking.booking import Booking
from message_text import MessageText

bot = telebot.TeleBot(config.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])  # Обработка первого сообщения
def message_star(message):
    """Приветствие. Отправка на создание брони."""
    sticker = open('stickers/hello_sticker.tgs', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    pc_button = types.KeyboardButton('Забронировать ПК')
    tabel_button = types.KeyboardButton('Забронировать столик')
    markup.add(pc_button, tabel_button)

    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, MessageText.MSG_HELLO, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Забронировать ПК')  # Бронирование ПК
def booking_pc(message):
    """Передача сообщения для бронирования ПК"""
    giv_pc = Booking(bot)
    giv_pc.pc_name(message)


@bot.message_handler(func=lambda message: message.text == 'Забронировать столик')  # Бронирование столика
def booking_pc(message):
    """Передача сообщения для бронирования столика"""
    giv_tb = Booking(bot)
    giv_tb.tb_name(message)


@bot.message_handler()  # Обработка других сообщений
def message_all(message):
    """Перевод к основному функционалу бота(бронирование)"""
    print(message.chat.id)
    if message.text.lower() in MessageText.MSG_OTHER:  # Реакция на сообщения: Привет, Hi...
        sticker = open('stickers/hello_sticker.tgs', 'rb')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        pc_button = types.KeyboardButton('Забронировать ПК')
        tabel_button = types.KeyboardButton('Забронировать столик')
        markup.add(pc_button, tabel_button)

        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, MessageText.MSG_HELLO, reply_markup=markup)
    # elif message.chat.id == 573154086:
    #     msg = bot.send_message(message.chat.id, 'Ты кто?')
    #     time.sleep(1)
    #     bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text='Привет Господин')

    else:  # Реакция на не записанные варианты сообщений
        sticker = open('stickers/understand.tgs', 'rb')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        pc_button = types.KeyboardButton('Забронировать ПК')
        tabel_button = types.KeyboardButton('Забронировать столик')
        markup.add(pc_button, tabel_button)

        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, MessageText.MSG_UNDERSTAND, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)  # Обработка InlineKeyboard
def callback_inline(call):
    """Обработка кнопок 'Уточнить детали', 'Бронь принята'"""
    print(call.message.message_id)
    if call.data.split()[0] == 'accept_booking':  # Бронь принята, осведомляем клиента
        markup_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        pc_button = types.KeyboardButton('Забронировать ПК')
        tabel_button = types.KeyboardButton('Забронировать столик')
        markup_keyboard.add(pc_button, tabel_button)

        markup_inline = types.InlineKeyboardMarkup()
        tg_era = types.InlineKeyboardButton('Telegram', url='https://t.me/eragaming76')
        vk_era = types.InlineKeyboardButton('ВКонтакте', url='https://vk.com/eragaming76')
        """site_era = types.InlineKeyboardButton('Сайт ERA', url='https://era')"""
        markup_inline.row(tg_era, vk_era)
        """markup_inline.row(site_era)"""

        stickers = open('stickers/accept_booking.tgs', 'rb')

        bot.edit_message_reply_markup(config.MY_ID, call.message.message_id, reply_markup=None)
        bot.send_message(call.data.split()[1], MessageText.MSG_ACCEPT_BOOKING, reply_markup=markup_keyboard)
        bot.send_sticker(call.data.split()[1], stickers, reply_markup=markup_inline)
    elif call.data.split()[0] == 'wait_booking':  # Связь по деталям брони, осведомляем клиента
        markup = types.InlineKeyboardMarkup()
        accept_booking = types.InlineKeyboardButton('Бронь принята',
                                                    callback_data=f'accept_booking {call.data.split()[1]}')
        markup.row(accept_booking)
        bot.edit_message_reply_markup(config.MY_ID, call.message.message_id, reply_markup=markup)
        bot.send_message(call.data.split()[1], MessageText.MSG_FEEDBACK)


while True:  # Бесконечный цикл проверки
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)
