# File name: databaseHandler.py
# Author: Iivari Anttila
# Description: A class for handling the database, all database interactions go through this class
import sqlite3

from SQLqueries.userSQL import GET_FIRST_NAME_FROM_ID
from user import User
from learningProgress import LearningProgress
from target import Target
from word.word import Word
from word.conjugation import Conjugation

class DatabaseHandler:
    def __init__(self, database_name = "Finnish_Language_App.sqlite3"):
        self.__database = database_name
        self.__connection = None
        self.__cursor = None

    @property
    def database(self):
        return self.__database

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    def __connect(self):
        if not self.cursor:
            try:
                self.__connection = sqlite3.connect(self.database)
                self.__cursor = self.__connection.cursor()
            except sqlite3.Error as error:
                print(f"Database Connection Error: {error}")


    def __execute_query(self, query: str, params=None):
        if self.cursor:
            try:
                if params:
                    if not isinstance(params, (tuple, list)):
                        params = (params,)
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)

                # Return rows if the QUERY was SELECT
                if query.upper().strip("\n").startswith("SELECT", 0, 30):
                    rows = self.cursor.fetchall()
                    return rows

                # Commit only queries that are not SELECT
                else:
                    self.cursor.connection.commit()  # Use connection.commit() instead of cursor.commit()

            except sqlite3.Error as error:
                print(f"Query Execution Error: {error}")

        else:
            print("No connection established with the database")


    def __close_connection(self):
        if self.connection:
            self.__connection.close()
            self.__cursor = None

    def form_all_users(self) -> list[User]:
        from SQLqueries.userSQL import GET_USERS
        self.__connect()
        id_list = list(self.__execute_query(GET_USERS))
        result = []

        for id in id_list:
            result.append(self.get_user_from_id(id[0]))
        self.__close_connection()
        return result


    def get_user_from_id(self, user_id) -> User:
        from SQLqueries.userSQL import GET_FIRST_NAME_FROM_ID
        self.__connect()
        first_name = self.__execute_query(GET_FIRST_NAME_FROM_ID, user_id)[0][0]
        learning_progresses = self.form_learning_progresses_from_id(user_id)
        self.__close_connection()
        return User(user_id, first_name, learning_progresses)


    def form_learning_progresses_from_id(self, user_id) -> list[LearningProgress]:
        from SQLqueries.userSQL import GET_USER_LEARNING_PROGRESSES
        self.__connect()

        result = []
        learning_data = self.__execute_query(GET_USER_LEARNING_PROGRESSES, user_id)

        for data in learning_data:
            target_id = data[0]
            level = data[1]
            due_date = data[2]

            target = self.form_target_from_id(target_id)

            result.append(LearningProgress(target, level, due_date))

        self.__close_connection()
        return result


    def form_target_from_id(self, target_id) -> Target:
        self.__connect()

        from SQLqueries.targetSQL import GET_TARGET_ENGLISH_TRANSLATIONS
        from SQLqueries.targetSQL import GET_TARGET_FINNISH_TRANSLATIONS
        from SQLqueries.targetSQL import GET_WORD_INFORMATION
        from SQLqueries.targetSQL import GET_GRAMMAR_POINT_INFORMATION
        from SQLqueries.targetSQL import GET_PHRASE_INFORMATION
        from SQLqueries.targetSQL import GET_WORD_CONJUGATIONS

        english_translations = self.__execute_query(GET_TARGET_ENGLISH_TRANSLATIONS, target_id)
        english_translations = DatabaseHandler.sort_translations(english_translations)
        finnish_translations = self.__execute_query(GET_TARGET_FINNISH_TRANSLATIONS, target_id)
        finnish_translations = DatabaseHandler.sort_translations(finnish_translations)

        # Figure out the target type
        word_data = self.__execute_query(GET_WORD_INFORMATION, target_id)
        grammar_data = self.__execute_query(GET_GRAMMAR_POINT_INFORMATION, target_id)
        phrase_data = self.__execute_query(GET_GRAMMAR_POINT_INFORMATION, target_id)

        # If the type is "Word"
        if word_data is not None:
            conjugations = self.__execute_query(GET_WORD_CONJUGATIONS, target_id)
            conjugation_objects = [Conjugation(*conjugation) for conjugation in conjugations]

            self.__close_connection()
            return Word(english_translations, finnish_translations, target_id,
                        word_data[0], conjugation_objects)


    def get_not_learned_targets(self, user_id):
        # Function to get all targets that a user has not learned yet
        self.__connect()
        from SQLqueries.targetSQL import GET_NOT_LEARNED_TARGETS
        targets = self.__execute_query(GET_NOT_LEARNED_TARGETS, user_id)

        result = []
        for target in targets:
            result.append(self.form_target_from_id(target[0]))
        self.__close_connection()
        return result


    @staticmethod
    def sort_translations(translations:list[tuple]):
        # Sort translations so that the translation with the priority is first
        sorted_translations = sorted(translations, key=lambda x: x[1], reverse=True)
        return [translation[0] for translation in sorted_translations]


## Some testing
if __name__ == "__main__":
    db = DatabaseHandler()
    users = db.form_all_users()
    for user in users:
        print(user)
        for learning_progress in user.learning_progresses:
            print(learning_progress)

        unlearned = db.get_not_learned_targets(user.user_id)
        print(unlearned)