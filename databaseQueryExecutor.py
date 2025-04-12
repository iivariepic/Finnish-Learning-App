# File name: databaseQueryExecutor.py
# Author: Iivari Anttila
# Description: A class for handling the execution of queries for the database
from databaseConnectionHandler import DatabaseConnectionHandler

class DatabaseQueryExecutor:
    def __init__(self, connection_handler: DatabaseConnectionHandler):
        self.connection_handler = connection_handler

    def execute_query(self, query: str, params=None):
        cursor = self.connection_handler.cursor
        if cursor:
            try:
                if params:
                    if not isinstance(params, (tuple, list)):
                        params = (params,)
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Return rows if the QUERY was SELECT
                if query.upper().strip("\n").startswith("SELECT"):
                    rows = cursor.fetchall()
                    return rows

                # Commit only queries that are not SELECT
                else:
                    cursor.connection.commit()

            except sqlite3.Error as error:
                print(f"Query Execution Error: {error}")
        else:
            print("No connection established with the database")
