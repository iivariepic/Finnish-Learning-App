# File name: target.py
# Author: Iivari Anttila
# Description: A class for a target (a thing that can be learned in this app, like a vocabulary word or a grammar point)

class Target:
    def __init__(self,
                 english_translations:list[str],
                 finnish_translations:list[str]):

        self.__english_translations = english_translations
        self.__finnish_translations = finnish_translations

    @property
    def english_translations(self):
        return self.__english_translations

    @property
    def finnish_translation(self):
        return self.__finnish_translations