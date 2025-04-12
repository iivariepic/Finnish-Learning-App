# File name: databaseHandler.py
# Author: Iivari Anttila
# Description: A class for handling the database, all database interactions go through this class
import sqlite3
from user import User

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
        try:
            self.__connection = sqlite3.connect(self.database)
            self.__cursor = self.__connection.cursor()
        except sqlite3.Error as error:
            print(f"Database Connection Error: {error}")

    def __execute_query(self, query:str):
        if self.cursor:
            try:
                self.cursor.execute(query)

                # Return rows if the QUERY was SELECT
                if query.upper().startswith("SELECT", 0, 30):
                    rows = self.cursor.fetchall()
                    return rows

                # Commit only queries that are not SELECT
                else:
                    cursor.commit()

            except sqlite3.Error as error:
                print(f"Query Execution Error: {error}")

        else:
            print("No connection established with the database")

    def __close_connection(self):
        if self.connection:
            self.__connection.close()
            self.__cursor = None

    def get_users(self):
        from SQLqueries.getUsers import GET_USERS

        self.__connect()
        data = self.__execute_query(GET_USERS)
        result = []
        self.__close_connection()

        for user in data:
            result.append(User(user[0], user[1], []))

        return result




## Some testing
if __name__ == "__main__":
    db = DatabaseHandler()
    users = db.get_users()

    print(users[0].first_name)
