# File name: userSQL.py
# Author: Iivari Anttila
# Description: SQL Queries related to users

GET_USERS = """
SELECT ID FROM User;
"""

GET_FIRST_NAME_FROM_ID = "SELECT First_Name FROM User WHERE User.ID = ?"

GET_USER_LEARNING_PROGRESSES = """
SELECT TargetID, Level, Next_Due_Date FROM Learning_Progress
WHERE Learning_Progress.UserID = ?;
"""