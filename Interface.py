import StringMatching
import DateRegex
import re

keyword = ["hapus", "deadline", "selesai"]
kataPenting = ["kelompok", "meet", "mata kuliah"]
kataDurasi = ["bulan", "minggu", "hari"]
kataTugas = ["kuis", "ujian", "tucil", "tubes", "praktikum", "laporan"]
kataTidakPenting = ["pada", "tentang", "ke"]

database = []
# Entry -> [DateArray, FullString], ex [[20, 10, 2021], "Laporan Stima"]

# --- Minor functions ---

def databaseLookup(targetString):
    for i in range(len(database)):
        fullString = database[i][1]
        splittedString = fullString.split(" ")
        for word in splittedString:
            if StringMatching.KMP(targetString.lower(), word.lower()):
                return [i, fullString]
    return None


def isArrayRegexFound(sourceArray, targetString):
    for pattern in sourceArray:
        if re.search(pattern, targetString.lower()) != None:
            return True
    return False







# ----- evaluateString() return list -----
# In descending order
# ["add", Full task string]    -> "tambah", kT + date - kTP
# ["update", Full task string] -> "deadline" + taskDatabase + date
# ["done", Full task string]   -> "selesai" + taskDatabase
# ["delete", Full task string] -> "hapus" + taskDatabase
# ["see", [Task list]]         -> "deadline"
# ["help", None]               -> "bantuan", "fitur"
# [None, None]                 -> No matching query

def evaluateString(targetString):
    resultingQuery = [None, None]

    # Adding branch
    if StringMatching.KMP(targetString.lower(), "tambah") or isArrayRegexFound(kataTugas, targetString):
        tempString = targetString
        for tidakPenting in kataTidakPenting:
            tempString = tempString.replace(tidakPenting, " ")
        dateArray = DateRegex.getDate(tempString)
        if dateArray != None:
            resultingQuery[0] = "add"
            resultingQuery[1] = [dateArray, DateRegex.stripDate(tempString)]
            # TODO : Add to database

    # Updating branch
    elif StringMatching.KMP(targetString.lower(), "deadline"):
        tempString = targetString
        for tidakPenting in kataTidakPenting:
            tempString = tempString.replace(tidakPenting, " ")
        dateArray = DateRegex.getDate(tempString)
        tempString = DateRegex.stripDate(tempString)

        resultDatabaseQuery = databaseLookup(tempString)
        if resultDatabaseQuery != None and dateArray != None:
            database[resultDatabaseQuery[0]][0] = dateArray
            resultingQuery[0] = "update"
            resultingQuery[1] = resultDatabaseQuery[1] + " " + DateRegex.dateArrayToString(dateArray)

    # TODO : Recommendation
    return resultingQuery


# Testing
temp = input()
print(evaluateString(temp))
