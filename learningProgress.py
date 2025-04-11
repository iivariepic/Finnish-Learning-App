# File name: learningProgress.py
# Author: Iivari Anttila
# Description: A class for a learning progress, where the level and due date of a word are stored
import datetime
from target import Target

class LearningProgress:
    def __init__(self, target:Target, level:int, due_date:datetime.datetime):
        self.__target:Target = target
        self.__level = level
        self.__due_date:datetime.datetime = due_date

    @property
    def target(self):
        return self.__target

    @property
    def level(self):
        return self.__level

    @property
    def due_date(self):
        return self.__due_date.date()

    def __level_up(self):
        self.__level += 1

    def __level_down(self):
        self.__level -= 1

    def __calculate_next_date(self):
        today = datetime.datetime.now()
        new_interval = 2 ** self.level
        self.__due_date = today + datetime.timedelta(days=new_interval)

    def update_progress(self, correct:bool):
        if correct:
            self.__level_up()
        else:
            self.__level_down()
        self.__calculate_next_date()