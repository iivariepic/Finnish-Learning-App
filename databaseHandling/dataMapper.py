# File name: dataMapper.py
# Author: Iivari Anttila
# Description: A class for mapping data to form classes from them
from databaseHandling.databaseQueryExecutor import DatabaseQueryExecutor
from targetTypes.grammarPoint import GrammarPoint
from targetTypes.conjugation import Conjugation
from targetTypes.phrase import Phrase
from targetTypes.word import Word
from user import User
from learningProgress import LearningProgress
from datetime import datetime

class DataMapper:
    def __init__(self, query_executor: DatabaseQueryExecutor):
        self.query_executor = query_executor

    @staticmethod
    def sort_translations(translations: list[tuple]) -> list:
        # Sort translations so that the translation with the highest priority is first
        sorted_translations = sorted(translations, key=lambda x: x[1], reverse=True)
        return [translation[0] for translation in sorted_translations]

    def map_user_from_id(self, user_id):
        from SQLqueries.userSQL import GET_FIRST_NAME_FROM_ID

        first_name = self.query_executor.execute_query(GET_FIRST_NAME_FROM_ID, user_id)[0][0]
        learning_progresses = self.map_learning_progresses_from_id(user_id)

        return User(user_id, first_name, learning_progresses)

    def map_learning_progresses_from_id(self, user_id):
        from SQLqueries.userSQL import GET_USER_LEARNING_PROGRESSES

        learning_data = self.query_executor.execute_query(GET_USER_LEARNING_PROGRESSES, user_id)
        result = []

        for data in learning_data:
            date = datetime.strptime(data[2], "%Y-%m-%d").date()
            target = self.map_target_from_id(data[0])
            result.append(LearningProgress(target, data[1], date))

        return result

    def check_user_id(self, user_id):
        # Function to check if user id exists
        from SQLqueries.userSQL import GET_FIRST_NAME_FROM_ID

        data = self.query_executor.execute_query(GET_FIRST_NAME_FROM_ID, user_id)
        return data == []

    def map_target_from_id(self, target_id):
        from SQLqueries.targetSQL import (
            GET_TARGET_ENGLISH_TRANSLATIONS,
            GET_TARGET_FINNISH_TRANSLATIONS,
            GET_WORD_INFORMATION,
            GET_GRAMMAR_POINT_INFORMATION,
            GET_PHRASE_INFORMATION,
            )

        english_translations = self.query_executor.execute_query(GET_TARGET_ENGLISH_TRANSLATIONS, target_id)
        finnish_translations = self.query_executor.execute_query(GET_TARGET_FINNISH_TRANSLATIONS, target_id)

        english_translations = self.sort_translations(english_translations)
        finnish_translations = self.sort_translations(finnish_translations)

        word_data = self.query_executor.execute_query(GET_WORD_INFORMATION, target_id)
        grammar_data = self.query_executor.execute_query(GET_GRAMMAR_POINT_INFORMATION, target_id)
        phrase_data = self.query_executor.execute_query(GET_PHRASE_INFORMATION, target_id)

        if word_data:
            conjugations = self.get_word_conjugations(target_id)
            return Word(english_translations, finnish_translations, target_id, word_data[0][0], conjugations)

        elif grammar_data:
            return GrammarPoint(english_translations, finnish_translations, target_id, grammar_data[0])

        elif phrase_data:
            words = [self.map_target_from_id(data[0]) for data in phrase_data]
            grammars = [self.map_target_from_id(data[1]) for data in phrase_data]
            return Phrase(
                english_translations,
                finnish_translations,
                target_id,
                words,
                grammars,
            )


    def get_word_conjugations(self, word_id) -> list[Conjugation]:
        from SQLqueries.targetSQL import GET_WORD_CONJUGATIONS
        conjugation_data = self.query_executor.execute_query(GET_WORD_CONJUGATIONS, word_id)
        conjugation_objects = []

        for row in conjugation_data:
            finnish_translation, conjugation_type, comparison_degree, tense, grammar_id = row

            required_grammar = None
            if grammar_id is not None:
                required_grammar = self.map_target_from_id(grammar_id)

            conjugation_objects.append(Conjugation(
                finnish_translation = finnish_translation,
                conjugation_type = conjugation_type,
                comparison_degree = comparison_degree,
                tense = tense,
                required_grammar = required_grammar,
            ))

        return conjugation_objects