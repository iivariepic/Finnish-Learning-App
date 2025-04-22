# File name: conjugation.py
# Author: Iivari Anttila
# Description: Conjugation for a targetTypes
from targetTypes.grammarPoint import GrammarPoint
from user import User

class Conjugation:
    def __init__(self,
                 conjugation_id:int,
                 finnish_translation:str,
                 conjugation_type:str,
                 comparison_degree:str = None,
                 tense:str = None,
                 required_grammar:GrammarPoint = None,
                 ):
        self.__conjugation_id = conjugation_id
        self.__finnish_translation = finnish_translation
        # Type means something like ("Third person", or "Inessive")
        self.__type = conjugation_type
        # Comparison Degree is only for ajectives and means something like ("comparative", or "superlative")
        self.__comparison_degree = comparison_degree
        # Tense is only for verbs and means something like ("past", "present")
        self.__tense = tense
        # Required Grammar Point is used if the user needs to learn a grammar point before using the Conjugation
        self.__required_grammar = required_grammar

    @property
    def conjugation_id(self):
        return self.__conjugation_id

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

    @property
    def required_grammar(self):
        return self.__required_grammar

    def check_required_grammar(self, user:User):
        # Check if the required grammar is at least in "level 1" learned
        grammar_id = self.required_grammar.target_id
        for learning_progress in user.learning_progresses:
            if learning_progress.target.target_id == grammar_id:
                return True

        return False

    def english_string(self) -> str:
        result = "("
        if self.tense:
            result += self.tense.capitalize() + ", "
        if self.comparison_degree:
            result += self.comparison_degree.capitalize() + ", "
        result += self.type.capitalize()
        result += ") "
        return result