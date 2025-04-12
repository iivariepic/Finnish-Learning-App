import sqlite3


class DatabaseHandler:
    def __init__(self):
        self.database = "Finnish_Language_App.sqlite3"

    def __execute_query(self, query:str):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Commit only methods that are not SELECT
        if not query.upper().startswith("SELECT", 0, 30):
            cursor.commit()

        connection.close()

        return rows