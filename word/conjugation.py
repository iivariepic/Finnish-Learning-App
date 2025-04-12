# File name: conjugation.py
# Author: Iivari Anttila
# Description: Conjugation for a word
class Conjugation:
    def __init__(self, finnish_translation:str, type:str):
        self.__finnish_translation = finnish_translation
        self.__type = type # Type means something like ("Third person", or "Inessive")

    @property
    def finnish_translation(self):
        return self.__finnish_translation

    @property
    def type(self):
        return self.__type