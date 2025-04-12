# File name: conjugation.py
# Author: Iivari Anttila
# Description: Conjugation for a word

class Conjugation:
    def __init__(self,
                 finnish_translation:str,
                 type:str,
                 comparison_degree:str = None,
                 tense:str = None
    ):
        self.__finnish_translation = finnish_translation
        # Type means something like ("Third person", or "Inessive")
        self.__type = type
        # Comparison Degree is only for ajectives and means something like ("comparative", or "superlative")
        self.__comparison_degree = comparison_degree
        # Tense is only for verbs and means something like ("past", "present")
        self.__tense = tense


    @property
    def finnish_translation(self):
        return self.__finnish_translation

    @property
    def type(self):
        return self.__type

    @property
    def comparison_degree(self):
        if self.__comparison_degree is not None:
            return self.__comparison_degree

    @property
    def tense(self):
        if self.__tense is not None:
            return self.__tense