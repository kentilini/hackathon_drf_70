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
        return "Я считаю, что это " + self.name + \
               "\nЗнания: " + str(self.knowledge) + \
               "\nНавыки преподавания: " + str(self.teaching_skills) + \
               "\nВ общении: " + str(self.in_person) + \
               "\nХалявность: " + str(self.how_easy) + \
               "\nСуммарно: " + str(self.total) + \
               "\nПодробнее можно узнать по ссылке: " + self.link