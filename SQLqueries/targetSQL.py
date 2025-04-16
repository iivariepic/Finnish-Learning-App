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

GET_WORD_INFORMATION = "SELECT Part_Of_Speech FROM Word WHERE TargetID = ?;"
GET_GRAMMAR_POINT_INFORMATION = "SELECT * FROM Grammar_Point WHERE TargetID = ?;"
GET_PHRASE_INFORMATION = """
SELECT WordID, GrammarID
FROM Phrase 
JOIN Phrase_Grammar ON Phrase.TargetID = Phrase_Grammar.PhraseID
JOIN Phrase_Word ON Phrase.TargetID = Phrase_Word.PhraseID
WHERE Phrase.TargetID = ?"""

GET_WORD_CONJUGATIONS = """
SELECT Conjugation.ID
FROM Conjugation
WHERE Conjugation.WordID = ?;"""

GET_GRAMMAR_CONJUGATIONS = """
SELECT Conjugation.ID
FROM Conjugation
WHERE Conjugation.GrammarID = ?
"""

GET_NOT_LEARNED_TARGETS = """
SELECT Target.ID
FROM Target
LEFT JOIN Learning_Progress 
    ON Target.ID = Learning_Progress.TargetID 
    AND Learning_Progress.UserID = ?
WHERE Learning_Progress.TargetID IS NULL;
"""

GET_GRAMMAR_PHRASES = """
SELECT TargetID
FROM Phrase 
JOIN Phrase_Grammar ON Phrase.TargetID = Phrase_Grammar.PhraseID
WHERE Phrase_Grammar.GrammarID = ?
"""

GET_WORD_PHRASES = """
SELECT TargetID
FROM Phrase 
JOIN Phrase_Word ON Phrase.TargetID = Phrase_Word.PhraseID
WHERE Phrase_Word.WordID = ?
"""

GET_CONJUGATION = """
SELECT Finnish_Translation, Conjugation_Type, Comparison_Degree, Tense, GrammarID
FROM Conjugation
WHERE Conjugation.ID = ?
"""