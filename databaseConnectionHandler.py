# File name: databaseConnectionHandler.py
# Author: Iivari Anttila
# Description: A class for handling the database connection
import sqlite3

class DatabaseConnectionHandler:
    def __init__(self, database_name="Finnish_Language_App.sqlite3"):
        self.__database = database_name
        self.__connection = None
        self.__cursor = None

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    def connect(self):
        if not self.cursor:
            try:
                self.__connection = sqlite3.connect(self.__database)
                self.__cursor = self.__connection.cursor()
            except sqlite3.Error as error:
                print(f"Database Connection Error: {error}")

    def close(self):
        if self.__connection:
            self.__connection.close()
            self.__cursor = None