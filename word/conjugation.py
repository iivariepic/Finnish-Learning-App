# File name: conjugation.py
# Author: Iivari Anttila
# Description: Conjugation for a word
from grammarPoint.grammarPoint import GrammarPoint
from user import User

class Conjugation:
    def __init__(self,
                 finnish_translation:str,
                 type:str,
                 comparison_degree:str = None,
                 tense:str = None,
                 required_grammar:GrammarPoint = None,
    ):
        self.__finnish_translation = finnish_translation
        # Type means something like ("Third person", or "Inessive")
        self.__type = type
        # Comparison Degree is only for ajectives and means something like ("comparative", or "superlative")
        self.__comparison_degree = comparison_degree
        # Tense is only for verbs and means something like ("past", "present")
        self.__tense = tense
        # Required Grammar Point is used if the user needs to learn a grammar point before using the Conjugation
        self.__required_grammar = required_grammar


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