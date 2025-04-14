# File name: phrase.py
# Author: Iivari Anttila
# Description: A Phrase
from target import Target
from targetTypes.word import Word
from targetTypes.grammarPoint import GrammarPoint

class Phrase(Target):
    def __init__(self,
                 english_equivalent:list[str],
                 finnish_equivalent:list[str],
                 target_id:int,
                 contains_words:list[Word],
                 contains_grammar:list[GrammarPoint]):
        super().__init__(english_equivalent, finnish_equivalent, target_id)
        self.__words = contains_words
        self.__grammar = contains_grammar

    @property
    def words(self):
        return self.__words

    def grammar(self):
        return self.__grammar