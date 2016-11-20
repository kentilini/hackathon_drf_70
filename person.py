class Person:
    name = "Овчинкин Владимир Александрович"
    link = "http://wikimipt.org/wiki/%D0%9E%D0%B2%D1%87%D0%B8%D0%BD%D0%BA%D0%B8%D0%BD_%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80%D0%BE%D0%B2%D0%B8%D1%87"
    knowledge = 4.48
    teaching_skills = 4.63
    in_person = 4.09
    how_easy = 3.52
    total = 4.57

    def __init__(self, name, link, knowledge, teaching_skills, in_person, how_easy, total):
        self.name = name
        self.link = link
        self.knowledge = knowledge
        self.teaching_skills = teaching_skills
        self.in_person = in_person
        self.how_easy = how_easy
        self.total = total

    def getString(self):
        return "Я считаю, что это " + self.name + \
               "\nЗнания: " + str(self.knowledge) + \
               "\nНавыки преподавания: " + str(self.teaching_skills) + \
               "\nВ общении: " + str(self.in_person) + \
               "\nХалявность: " + str(self.how_easy) + \
               "\nСуммарно: " + str(self.total) + \
               "\nПодробнее можно узнать по ссылке: " + self.link