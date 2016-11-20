# -*- coding: utf-8 -*-
import telebot
import logging
import uuid
import webparser
from person import Person
from telebot import types

API_TOKEN = '277757979:AAEPrc9yqbSfZkQHti5q8Q0c8F0M-ttlbQs'
HELP_MESSAGE = "Пришлите мне фотографию преподователя МФТИ и я попытаюсь определить кто это."

bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.inline_handler(func=lambda query: True)
def send_welcome(query):
    r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
    r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
    bot.answer_inline_query(query.id, [r, r2])

@bot.message_handler(func=lambda message: True)
def search(message):
    result = search_for(message.text)
    markup = types.InlineKeyboardMarkup(3)
    markup.row(types.InlineKeyboardButton(text="Смотреть все результаты",
                                          switch_inline_query_current_chat=result.name))
    bot.send_message(message.chat.id, "Найдено несколько подходящих записей.\n", reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        attached_file = bot.download_file(file_info.file_path)

        person = get_answer()
        bot.reply_to(message, person.get_string())

    except Exception as e:
        error_uuid = uuid.uuid1()
        logger.error(str(e) + " " + str(error_uuid))
        bot.reply_to(message, "К сожалению мне не удалось обработать ваш запрос по технической причине, " +
                     "вашей проблеме присовен уникальный идентификатор: " + str(error_uuid))

def get_answer():
    return Person("Овчинкин Владимир Александрович",
                  "http://wikimipt.org/wiki/%D0%9E%D0%B2%D1%87%D0%B8%D0%BD%D0%BA%D0%B8%D0%BD_%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80%D0%BE%D0%B2%D0%B8%D1%87",
                    4.48,
                    4.63,
                    4.09,
                    3.52,
                    4.57)

def search_for(search_string):
    return webparser.get_prep_list(search_string)

bot.polling(none_stop=True, interval=3, timeout=3)