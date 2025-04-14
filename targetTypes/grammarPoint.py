# File name: grammarPoint.py
# Author: Iivari Anttila
# Description: A Grammar Point Target
from target import Target

class GrammarPoint(Target):
    def __init__(self,
                 english_equivalent:list[str],
                 finnish_equivalent:list[str],
                 target_id:int,
                 teaching_text:str):
        super().__init__(english_equivalent, finnish_equivalent, target_id)
        self.__teaching_text = teaching_text

    @property
    def teaching_text(self):
        return self.__teaching_text