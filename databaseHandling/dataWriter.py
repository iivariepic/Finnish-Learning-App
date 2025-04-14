# File name: dataWriter.py
# Author: Iivari Anttila
# Description: A class for mapping data to form classes from them
from databaseHandling.databaseQueryExecutor import DatabaseQueryExecutor
from user import User
from target import Target
from learningProgress import LearningProgress
from datetime import datetime

class DataWriter:
    def __init__(self, query_executor: DatabaseQueryExecutor):
        self.query_executor = query_executor

    def add_user(self, user:User):
        from SQLqueries.writeSQL import NEW_USER
        parameters = [user.user_id, user.first_name]
        self.query_executor.execute_query(NEW_USER, parameters)

    def save_user_changes(self, user:User):
        from SQLqueries.writeSQL import CHANGE_USERNAME
        parameters = [user.first_name, user.user_id]
        self.query_executor.execute_query(CHANGE_USERNAME, parameters)

    def add_learning_progress(self, user:User, learning_progress:LearningProgress):
        from SQLqueries.writeSQL import CREATE_LEARNING_PROGRESS
        parameters = [
            learning_progress.due_date.strftime("%Y-%m-%d"),
            0,
            user.user_id,
            learning_progress.target.target_id
        ]
        self.query_executor.execute_query(CREATE_LEARNING_PROGRESS, parameters)

    def save_learning_progress_changes(self, user:User, learning_progess:LearningProgress):
        from SQLqueries.writeSQL import UPDATE_LEARNING_PROGRESS
        parameters = [
            learning_progess.level,
            learning_progess.due_date.strftime("%Y-%m-%d"),
            user.user_id,
            learning_progess.target.target_id
        ]
        self.query_executor.execute_query(UPDATE_LEARNING_PROGRESS)