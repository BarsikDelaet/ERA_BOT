"""Функция бронирования."""
__author__ = "Барсуков М.О."


from func_buking.servis import Service
from message_text import MessageText
from telebot import types
import config


class Booking(Service):

    """Бронирование ПК"""
    def pc_name(self, message):  # Спрашиваем имя клиента
        self.booking_data.clear()
        hide_board = types.ReplyKeyboardRemove()
        self.bot.send_message(message.chat.id, MessageText.MSG_NAME, reply_markup=hide_board)
        self.bot.register_next_step_handler(message, self.pc_time)

    def pc_time(self, message):  # Время бронирования
        self.booking_data.append(message.text)
        self.bot.send_message(message.chat.id, MessageText.MSG_TIME)
        self.bot.register_next_step_handler(message, self.pc_number)

    def pc_number(self, message):  # Номер для связи
        self.booking_data.append(message.text)
        self.bot.send_message(message.chat.id, MessageText.MSG_NUMBER)
        self.bot.register_next_step_handler(message, self.pc_people)

    def pc_people(self, message):  # Кол-во человек
        self.booking_data.append(message.text)
        self.bot.send_message(message.chat.id, MessageText.MSG_PEOPLE_PC)
        self.bot.register_next_step_handler(message, self.pc_addition)

    def pc_addition(self, message):  # Дополнительные данные
        self.booking_data.append(message.text)
        check_split = message.text.split()
        for i in check_split:
            if i.isdigit():
                i = int(i)
                if i not in range(0, 40) and i not in range(100, 110):
                    del self.booking_data[-1]
                    self.bot.send_message(message.chat.id, MessageText.MSG_PC_BIG_DIGIT)
                    self.bot.send_message(message.chat.id, MessageText.MSG_ADDITION_PC)
                    self.bot.register_next_step_handler(message, self.pc_addition)
                    return
        self.bot.send_message(message.chat.id, MessageText.MSG_ADDITION_PC)
        self.bot.register_next_step_handler(message, self.pc_test)

    def pc_test(self, message):  # Просим проверить записанные данные
        self.booking_data.append(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        yes_button = types.KeyboardButton('Да')
        no_button = types.KeyboardButton('Нет')
        markup.add(yes_button, no_button)

        self.bot.send_message(message.chat.id, f"""Бронь ПК 
Имя: <b>{self.booking_data[0]}</b>
Время: <b>{self.booking_data[1]}</b>
Кол-во человек: <b>{self.booking_data[3]}</b>
Номер ПК/др. данные: <b>{self.booking_data[4]}</b>
Ваш номер: <b>{self.booking_data[2]}</b>

Всё правильно?""", parse_mode='html', reply_markup=markup)
        self.bot.register_next_step_handler(message, self.pc_answer)

    def pc_answer(self, message):  # Действия после ответа клиента о бронировании
        if message.text.lower() == "да":  # Отправляем записанные данные на акк клуба
            markup = types.InlineKeyboardMarkup()
            wait_booking = types.InlineKeyboardButton('Уточнить детали',
                                                      callback_data=f'wait_booking {message.chat.id}')
            accept_booking = types.InlineKeyboardButton('Бронь принята',
                                                        callback_data=f'accept_booking {message.chat.id}')
            markup.row(wait_booking, accept_booking)

            hide_board = types.ReplyKeyboardRemove()

            sticker = open('stickers/answer_yes.tgs', 'rb')

            self.bot.send_message(config.MY_ID, f"""Бронь ПК 
Имя: <b>{self.booking_data[0]}</b>
Время: <b>{self.booking_data[1]}</b>
Номер ПК/кол-во человек: <b>{self.booking_data[3]}</b>
Номер тел.: <b>{self.booking_data[2]}</b>""", parse_mode='html', reply_markup=markup)
            self.bot.send_sticker(message.chat.id, sticker, reply_markup=hide_board)  # Ответ клиенту после подтверждения
            self.bot.send_message(message.chat.id, MessageText.MSG_WAIT_BOOKING)
        elif message.text.lower() == "нет":  # Просим ввести данные заново
            self.booking_data.clear()
            hide_board = types.ReplyKeyboardRemove()
            self.bot.send_message(message.chat.id, MessageText.MSG_NAME, reply_markup=hide_board)
            self.bot.register_next_step_handler(message, self.pc_time)
        else:  # Если ответили неправильно
            self.bot.send_message(message.chat.id, MessageText.MSG_YES_OR_NO)
            self.bot.register_next_step_handler(message, self.pc_answer)

    """Бронирование Столика"""
    def tb_name(self, message):  # Спрашиваем имя клиента
        self.booking_data.clear()
        hide_board = types.ReplyKeyboardRemove()
        self.bot.send_message(message.chat.id, MessageText.MSG_NAME, reply_markup=hide_board)
        self.bot.register_next_step_handler(message, self.tb_time)

    def tb_time(self, message):  # Время бронирования
        self.booking_data.append(message.text)
        self.bot.send_message(message.chat.id, MessageText.MSG_TIME)
        self.bot.register_next_step_handler(message, self.tb_number)

    def tb_number(self, message):  # Номер для связи
        self.booking_data.append(message.text)
        self.bot.send_message(message.chat.id, MessageText.MSG_NUMBER)
        self.bot.register_next_step_handler(message, self.tb_people)

    def tb_people(self, message):  # Кол-во человек и доп. данные
        self.booking_data.append(message.text)
        self.bot.send_message(message.chat.id, MessageText.MSG_PEOPLE_TB)
        self.bot.register_next_step_handler(message, self.tb_test)

    def tb_test(self, message):  # Просим проверить записанные данные
        self.booking_data.append(message.text)
        check_split = message.text.split()
        for i in check_split:
            if i.isdigit():
                i = int(i)
                if i not in range(0, 60):
                    del self.booking_data[-1]
                    self.bot.send_message(message.chat.id, MessageText.MSG_TB_BIG_DIGIT)
                    self.bot.send_message(message.chat.id, MessageText.MSG_PEOPLE_TB)
                    self.bot.register_next_step_handler(message, self.tb_test)
                    return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        yes_button = types.KeyboardButton('Да')
        no_button = types.KeyboardButton('Нет')
        markup.add(yes_button, no_button)

        self.bot.send_message(message.chat.id, f"""Бронь Столика 
Имя: <b>{self.booking_data[0]}</b>
Время: <b>{self.booking_data[1]}</b>
Количество персон: <b>{self.booking_data[3]}</b>
Ваш номер: <b>{self.booking_data[2]}</b>

Всё правильно?""", parse_mode='html', reply_markup=markup)
        self.bot.register_next_step_handler(message, self.tb_answer)

    def tb_answer(self, message):  # Действия после ответа клиента о бронировании
        if message.text.lower() == "да":  # Если Да то отправляем ERA Tg
            markup = types.InlineKeyboardMarkup()
            wait_booking = types.InlineKeyboardButton('Уточнить детали',
                                                      callback_data=f'wait_booking {message.chat.id}')
            accept_booking = types.InlineKeyboardButton('Бронь принята',
                                                        callback_data=f'accept_booking {message.chat.id}')
            markup.row(wait_booking, accept_booking)

            hide_board = types.ReplyKeyboardRemove()

            sticker = open('stickers/answer_yes.tgs', 'rb')

            self.bot.send_message(config.MY_ID, f"""Бронь столика 
Имя: <b>{self.booking_data[0]}</b>
Время: <b>{self.booking_data[1]}</b>
Количество персон: <b>{self.booking_data[3]}</b>
Номер тел.: <b>{self.booking_data[2]}</b>""", parse_mode='html', reply_markup=markup)
            self.bot.send_sticker(message.chat.id, sticker, reply_markup=hide_board)  # Ответ клиенту после подтверждения
            self.bot.send_message(message.chat.id, MessageText.MSG_WAIT_BOOKING)
        elif message.text.lower() == "нет":
            self.booking_data.clear()
            hide_board = types.ReplyKeyboardRemove()
            self.bot.send_message(message.chat.id, MessageText.MSG_NAME, reply_markup=hide_board)
            self.bot.register_next_step_handler(message, self.tb_time)
        else:
            self.bot.send_message(message.chat.id, MessageText.MSG_YES_OR_NO)
            self.bot.register_next_step_handler(message, self.tb_answer)
