# File name: word.py
# Author: Iivari Anttila
# Description: A class for a word
from target import Target
from word.conjugation import Conjugation

class Word(Target):
    def __init__(self,
                 english_translations:list[str],
                 finnish_translations:list[str],
                 target_id:int,
                 part_of_speech:str,
                 initial_conjugations:list[Conjugation] = []):

        super().__init__(english_translations, finnish_translations, target_id)
        self.__part_of_speech = part_of_speech
        self.__conjugations = initial_conjugations

    @property
    def conjugations(self):
        return self.__conjugations

    @property
    def part_of_speech(self):
        return self.__part_of_speech

    def add_conjugation(self, conjugation:Conjugation):
        if conjugation.type not in self.conjugations:
            self.__conjugations.append(conjugation)