# -*- coding: utf-8 -*-

class Person:
    def __init__(self, name, link, knowledge, teaching_skills, in_person, how_easy, total):
        self.name = name
        self.link = link
        self.knowledge = knowledge
        self.teaching_skills = teaching_skills
        self.in_person = in_person
        self.how_easy = how_easy
        self.total = total

    def get_string(self):
        return u"Я считаю, что это " + self.name + \
               u"\nЗнания: " + self.knowledge + \
               u"\nНавыки преподавания: " + self.teaching_skills + \
               u"\nВ общении: " + self.in_person + \
               u"\nХалявность: " + self.how_easy + \
               u"\nСуммарно: " + self.total + \
               u"\nПодробнее можно узнать по ссылке: " + self.link
