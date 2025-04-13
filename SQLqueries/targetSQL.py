# File name: targetSQL.py
# Author: Iivari Anttila
# Description: SQL Queries related to targets

GET_TARGET_ENGLISH_TRANSLATIONS = """
SELECT English_Translation, isPrimary FROM Target_English_Translation
WHERE TargetID = ?
"""

GET_TARGET_FINNISH_TRANSLATIONS = """
SELECT Finnish_Translation, isPrimary FROM Target_Finnish_Translation
WHERE TargetID = ?
"""

GET_WORD_INFORMATION = "SELECT * FROM Word WHERE TargetID = ?;"
GET_GRAMMAR_POINT_INFORMATION = "SELECT * FROM Grammar_Point WHERE TargetID = ?;"
GET_PHRASE_INFORMATION = "SELECT * FROM Phrase WHERE TargetID = ?;"

GET_WORD_CONJUGATIONS = """
SELECT Finnish_Translation, Conjugation_Type, Comparison_Degree, Tense, GrammarID
FROM Conjugation
WHERE Conjugation.WordID = ?;"""


GET_NOT_LEARNED_TARGETS = """
SELECT Target.ID
FROM Target
LEFT JOIN Learning_Progress 
    ON Target.ID = Learning_Progress.TargetID 
    AND Learning_Progress.UserID = ?
WHERE Learning_Progress.TargetID IS NULL;
"""

NEXT_TARGET_ID = """
SELECT COUNT(DISTINCT ID) FROM Target;
"""