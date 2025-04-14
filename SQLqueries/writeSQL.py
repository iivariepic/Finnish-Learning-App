# File name: writeSQL.py
# Author: Iivari Anttila
# Description: SQL Queries related to writing data

NEW_USER = """
INSERT INTO User(ID, First_Name)
VALUES(?, ?);
"""

CHANGE_USERNAME = """
UPDATE User
SET First_Name = ?
WHERE User.ID = ?
"""

CREATE_LEARNING_PROGRESS = """
INSERT INTO Learning_Progress(Next_Due_Date, Level, UserID, TargetID)
VALUES(?, ?, ?, ?, ?)
"""

UPDATE_LEARNING_PROGRESS = """
UPDATE Learning_Progress
SET Level = ?, Next_Due_Date = ?
WHERE UserID = ? AND TargetID = ?;
"""