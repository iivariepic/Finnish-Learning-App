# File name: user.py
# Author: Iivari Anttila
# Description: A class for a user
from learningProgress import LearningProgress

class User:
    def __init__(self, id:int, first_name:str,
                 learning_progresses:list[LearningProgress] = []):
        self.__id = id
        self.__first_name = first_name
        self.__learning_progresses:list = learning_progresses

    @property
    def user_id(self):
        return self.__id

    @property
    def first_name(self):
        return  self.__first_name

    @property
    def learning_progresses(self):
        return self.__learning_progresses

    def add_learning_progress(self, learning_progress:LearningProgress):
        self.__learning_progresses.append(learning_progress)

    def __str__(self):
        return f"{self.user_id}: {self.first_name}"