# File name: targetTypes.py
# Author: Iivari Anttila
# Description: A class for a targetTypes
from target import Target
from targetTypes.conjugation import Conjugation

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

    def conjugations_string(self):
        result = ""
        first_loop: bool = True
        for conjugation in self.conjugations:
            if not first_loop:
                result += "\n"
            else:
                first_loop = False

            result = conjugation.english_string()
            result += conjugation.finnish_translation.capitalize()

        if result == "":
            result = "No conjugations available"
        return result