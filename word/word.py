# File name: word.py
# Author: Iivari Anttila
# Description: A class for a word
from target import Target
from conjugation import Conjugation

class Word(Target):
    def __init__(self,
                 english_translations:list[str],
                 finnish_translations:list[str],
                 initial_conjugations:list[Conjugation]):
        super().__init__(english_translations, finnish_translations)
        self.__conjugations = []

    @property
    def conjugations(self):
        return self.__conjugations

    def add_conjugation(self, conjugation:Conjugation):
        if conjugation.type not in self.conjugations:
            self.__conjugations.append(conjugation)