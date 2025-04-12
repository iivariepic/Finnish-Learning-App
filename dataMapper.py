# File name: databaseMapper.py
# Author: Iivari Anttila
# Description: A class for mapping data to form classes from them
from databaseQueryExecutor import DatabaseQueryExecutor
from word.word import Word
from user import User
from target import Target
from learningProgress import LearningProgress

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
            target = self.map_target_from_id(data[0])
            result.append(LearningProgress(target, data[1], data[2]))

        return result

    def map_target_from_id(self, target_id):
        from SQLqueries.targetSQL import (
            GET_TARGET_ENGLISH_TRANSLATIONS,
            GET_TARGET_FINNISH_TRANSLATIONS,
            GET_WORD_INFORMATION,
            GET_GRAMMAR_POINT_INFORMATION,
            GET_PHRASE_INFORMATION,
            GET_WORD_CONJUGATIONS
        )

        english_translations = self.query_executor.execute_query(GET_TARGET_ENGLISH_TRANSLATIONS, target_id)
        finnish_translations = self.query_executor.execute_query(GET_TARGET_FINNISH_TRANSLATIONS, target_id)

        english_translations = self.sort_translations(english_translations)
        finnish_translations = self.sort_translations(finnish_translations)

        word_data = self.query_executor.execute_query(GET_WORD_INFORMATION, target_id)

        if word_data:
            conjugations = self.query_executor.execute_query(GET_WORD_CONJUGATIONS, target_id)
            conjugation_objects = [Conjugation(*conjugation) for conjugation in conjugations]
            return Word(english_translations, finnish_translations, target_id, word_data[0], conjugation_objects)