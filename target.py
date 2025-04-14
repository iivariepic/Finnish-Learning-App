# File name: target.py
# Author: Iivari Anttila
# Description: A class for a target (a thing that can be learned in this app, like a vocabulary targetTypes or a grammar point)

class Target:
    def __init__(self,
                 english_translations:list[str],
                 finnish_translations:list[str],
                 target_id:int):

        self.__english_translations = english_translations
        self.__finnish_translations = finnish_translations
        self.__id = target_id

    @property
    def english_translations(self):
        return self.__english_translations

    @property
    def finnish_translations(self):
        return self.__finnish_translations

    @property
    def target_id(self):
        return self.__id

    def __str__(self):
        return f"{self.english_translations[0]} | {self.finnish_translations[0]}"