# -*- coding: utf-8 -*-
import telebot
import logging
import uuid
import webparser
import readfile
import traceback
from person import Person
from telebot import types

API_TOKEN = '277757979:AAEPrc9yqbSfZkQHti5q8Q0c8F0M-ttlbQs'
HELP_MESSAGE = "Пришлите мне фотографию преподователя МФТИ и я попытаюсь определить кто это. \n" \
               "А ещё Вы можете прислать мне имя преподователя и я попробую найти информацию о нём."

bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.inline_handler(func=lambda query: True)
def send_welcome(query):
    result = search_for(query.query)
    arr = []
    id = 1
    for person in result:
        arr.append(types.InlineQueryResultArticle(str(id), person['name'], types.InputTextMessageContent(person['name'])))
        id += 1
        print arr
    bot.answer_inline_query(query.id, arr)


@bot.message_handler(func=lambda message: True)
def search(message):
    result = search_for(message.text)
    print result
    if len(result) == 0:
        bot.send_message(message.chat.id, "Ничего не найдено.")
        return

    if len(result) == 1:
        person_map = result[0]
        person = Person(person_map.get('name', 'Not Provided'),
                        person_map.get('link', 'Not Provided'),
                        person_map.get('knowledge', 'Not Provided'),
                        person_map.get('teaching_skills', 'Not Provided'),
                        person_map.get('in_person', 'Not Provided'),
                        person_map.get('how_easy', 'Not Provided'),
                        person_map.get('total', 'Not Provided'))
        bot.send_message(message.chat.id, person.get_string())
        return

    markup = types.InlineKeyboardMarkup(3)
    markup.row(types.InlineKeyboardButton(text="Смотреть все результаты",
                                          switch_inline_query_current_chat=message.text))
    bot.send_message(message.chat.id, "Найдено несколько подходящих записей.\n", reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        attached_file = bot.download_file(file_info.file_path)
        path = str(uuid.uuid1())
        f = open(path, "wb")
        f.write(attached_file)
        f.close()

        best_match = readfile.get_best_match(path)
        if best_match is None:
            bot.reply_to(message, "К сожалению мы не можем узнать этого человека.")
            return
        print best_match
        person_map = webparser.get_prep_by_path(best_match.get(u"url"), best_match.get(u"name"))
        person = Person(person_map.get('name', 'Not Provided'),
                        person_map.get('link', 'Not Provided'),
                        person_map.get('knowledge', 'Not Provided'),
                        person_map.get('teaching_skills', 'Not Provided'),
                        person_map.get('in_person', 'Not Provided'),
                        person_map.get('how_easy', 'Not Provided'),
                        person_map.get('total', 'Not Provided'))
        bot.reply_to(message, person.get_string())

    except Exception as e:
        traceback.print_exc()
        error_uuid = uuid.uuid1()
        logger.error(str(e) + " " + str(error_uuid))
        bot.reply_to(message, "К сожалению мне не удалось обработать ваш запрос по технической причине, " +
                     "вашей проблеме присовен уникальный идентификатор: " + str(error_uuid))


def get_answer():
    return


def search_for(search_string):
    return webparser.get_prep_property_list(search_string)


bot.polling(none_stop=True, interval=3, timeout=3)
