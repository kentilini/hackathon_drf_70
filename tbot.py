import telebot
import logging
import urllib.request
from person import Person
from telebot import types

API_TOKEN = '273095775:AAG0JALdAib4xobarKMge1e9DuaWJcmUXC4'
HELP_MESSAGE = "Пришлите мне фотографию преподователя МФТИ и я попытаюсь определить кто это и дать информацию о нём"

bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, HELP_MESSAGE)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Я не понимаю Вас.\n" + HELP_MESSAGE)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        attached_file = bot.download_file(file_info.file_path)

        person = get_answer()
        bot.reply_to(message, person.getString())

    except Exception as e:
        bot.reply_to(message, e)

def get_answer():
    return Person("Овчинкин Владимир Александрович",
                  "http://wikimipt.org/wiki/%D0%9E%D0%B2%D1%87%D0%B8%D0%BD%D0%BA%D0%B8%D0%BD_%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80%D0%BE%D0%B2%D0%B8%D1%87",
                    4.48,
                    4.63,
                    4.09,
                    3.52,
                    4.57)


bot.polling(none_stop=True, interval=3, timeout=3)