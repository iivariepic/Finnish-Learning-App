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

    def next_user_id(self):
        from SQLqueries.userSQL import GET_NEXT_ID
        data = self.query_executor.execute_query(GET_NEXT_ID)
        if data is None:
            return 1
        else:
            return str(data[0][0] + 1)

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
            teaching_text = grammar_data[0][0].replace("\\n", "\n")
            return GrammarPoint(english_translations, finnish_translations, target_id, teaching_text)

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

        for conjugation_id in conjugation_data:
            conjugation_objects.append(
                self.map_conjugation_from_id(conjugation_id)
            )

        return conjugation_objects

    def get_grammar_conjugations(self, grammar_id) -> list[Conjugation]:
        from SQLqueries.targetSQL import GET_GRAMMAR_CONJUGATIONS
        conjugation_data = self.query_executor.execute_query(GET_GRAMMAR_CONJUGATIONS, grammar_id)
        conjugation_objects = []

        for conjugation_id in conjugation_data:
            conjugation_objects.append(
                self.map_conjugation_from_id(conjugation_id)
            )

        return conjugation_objects

    def get_word_phrases(self, word_id):
        from SQLqueries.targetSQL import GET_WORD_PHRASES
        phrase_ids = self.query_executor.execute_query(
            GET_WORD_PHRASES, word_id
        )
        result = []
        for phrase_id in phrase_ids:
            result.append(self.map_target_from_id(phrase_id[0]))

        return result

    def get_grammar_phrases(self, grammar_id):
        from SQLqueries.targetSQL import GET_GRAMMAR_PHRASES
        phrase_ids = self.query_executor.execute_query(
            GET_GRAMMAR_PHRASES, grammar_id
        )
        result = []
        for phrase_id in phrase_ids:
            result.append(self.map_target_from_id(phrase_id[0]))

        return result


    def map_conjugation_from_id(self, conjugation_id):
        from SQLqueries.targetSQL import GET_CONJUGATION
        data = self.query_executor.execute_query(GET_CONJUGATION, conjugation_id)

        finnish_translation, conjugation_type, comparison_degree, tense, grammar_id = data[0]

        required_grammar = None
        if grammar_id is not None:
            required_grammar = self.map_target_from_id(grammar_id)

        return Conjugation(
            conjugation_id=conjugation_id,
            finnish_translation=finnish_translation,
            conjugation_type=conjugation_type,
            comparison_degree=comparison_degree,
            tense=tense,
            required_grammar=required_grammar,
        )

    def get_conjugation_word(self, conjugation_id):
        from SQLqueries.targetSQL import GET_CONJUGATION_WORD
        data = self.query_executor.execute_query(GET_CONJUGATION_WORD, conjugation_id)
        return self.map_target_from_id(data[0][0])
