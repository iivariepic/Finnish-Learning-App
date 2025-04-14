# File name: databaseHandler.py
# Author: Iivari Anttila
# Description: A class for handling the database, all database interactions go through this class

from databaseHandling.databaseConnectionHandler import DatabaseConnectionHandler
from databaseHandling.databaseQueryExecutor import DatabaseQueryExecutor
from databaseHandling.dataMapper import DataMapper
from databaseHandling.dataWriter import DataWriter
from user import User
from learningProgress import LearningProgress

class DatabaseHandler:
    def __init__(self, database_name="Finnish_Language_App.sqlite3"):
        self.__connection_handler = DatabaseConnectionHandler(database_name)
        self.__query_executor = DatabaseQueryExecutor(self.__connection_handler)
        self.__data_mapper = DataMapper(self.__query_executor)
        self.__data_writer = DataWriter(self.__query_executor)

    @staticmethod
    def connect_to_database(function):
        def wrapper(self, *args, **kwargs):
            self.__connection_handler.connect()
            try:
                return function(self, *args, **kwargs)
            finally:
                self.__connection_handler.close()

        return wrapper

    @connect_to_database
    def form_all_users(self) -> list[User]:
        from SQLqueries.userSQL import GET_USERS
        id_list = self.__query_executor.execute_query(GET_USERS)
        result = []

        for id in id_list:
            result.append(self.__data_mapper.map_user_from_id(id[0]))

        return result

    @connect_to_database
    def get_user_from_id(self, user_id) -> User:
        user = self.__data_mapper.map_user_from_id(user_id)
        return user

    @connect_to_database
    def new_user(self, new_user:User):
        if self.__data_mapper.check_user_id(new_user.user_id):
            self.__data_writer.add_user(new_user)
        else:
            print("User with ID already exists")

    @connect_to_database
    def change_user(self, changed_user:User):
        self.__data_writer.save_user_changes(changed_user)

    @connect_to_database
    def new_learning_progress(self, user:User, new_learning_progress:LearningProgress):
        self.__data_writer.add_learning_progress(user, new_learning_progress)

    @connect_to_database
    def change_learning_progress(self, user:User, learning_progress:LearningProgress):
        self.__data_writer.save_learning_progress_changes(user, learning_progress)

    @connect_to_database
    def get_not_learned_targets(self, user_id):
        from SQLqueries.targetSQL import GET_NOT_LEARNED_TARGETS
        targets = self.__query_executor.execute_query(GET_NOT_LEARNED_TARGETS, user_id)
        result = []
        for target in targets:
            result.append(self.__data_mapper.map_target_from_id(target[0]))

        return result

    @connect_to_database
    def get_next_user_id(self):
        i = 1
        while True:
            if self.__data_mapper.check_user_id(i):
                return i
            i += 1

    @connect_to_database
    def delete_user_id(self, user_id):
        from SQLqueries.writeSQL import DELETE_USER_ID
        self.__query_executor.execute_query(DELETE_USER_ID, user_id)


## Some testing
if __name__ == "__main__":
    db = DatabaseHandler()

    conflicting_user = User(1, "Iivari")
    db.new_user(conflicting_user)
    modification_to_user = User(1, "Iivari2")
    db.change_user(modification_to_user)

    users = db.form_all_users()
    for user in users:
        print(user)
        for learning_progress in user.learning_progresses:
            print(learning_progress)

        unlearned = db.get_not_learned_targets(user.user_id)
        print(unlearned)

    modification_to_user = User(1, "Iivari")
    db.change_user(modification_to_user)
    print(db.get_next_user_id())
    print(db.get_next_target_id())
