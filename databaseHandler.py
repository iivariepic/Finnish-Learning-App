# File name: databaseHandler.py
# Author: Iivari Anttila
# Description: A class for handling the database, all database interactions go through this class
import sqlite3

from databaseConnectionHandler import DatabaseConnectionHandler
from databaseQueryExecutor import DatabaseQueryExecutor
from dataMapper import DataMapper
from user import User

class DatabaseHandler:
    def __init__(self, database_name="Finnish_Language_App.sqlite3"):
        self.__connection_handler = DatabaseConnectionHandler(database_name)
        self.__query_executor = DatabaseQueryExecutor(self.__connection_handler)
        self.__data_mapper = DataMapper(self.__query_executor)

    def form_all_users(self) -> list[User]:
        self.__connection_handler.connect()
        from SQLqueries.userSQL import GET_USERS
        id_list = self.__query_executor.execute_query(GET_USERS)
        result = []
        for id in id_list:
            result.append(self.__data_mapper.map_user_from_id(id[0]))
        self.__connection_handler.close()
        return result

    def get_user_from_id(self, user_id) -> User:
        self.__connection_handler.connect()
        user = self.__data_mapper.map_user_from_id(user_id)
        self.__connection_handler.close()
        return user

    def get_not_learned_targets(self, user_id):
        self.__connection_handler.connect()
        from SQLqueries.targetSQL import GET_NOT_LEARNED_TARGETS
        targets = self.__query_executor.execute_query(GET_NOT_LEARNED_TARGETS, user_id)
        result = []
        for target in targets:
            result.append(self.__data_mapper.map_target_from_id(target[0]))
        self.__connection_handler.close()
        return result



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