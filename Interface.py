import StringMatching
import DateRegex
import re

keyword = ["hapus", "deadline", "selesai"]
kataPenting = ["kelompok", "meet", "mata kuliah"]
kataDurasi = ["bulan", "minggu", "hari"]
kataTugas = ["kuis", "ujian", "tucil", "tubes", "praktikum", "laporan"]
kataTidakPenting = ["pada", "tentang", "ke"]


# ----- evaluateString() return list -----
# In descending order
# ["add", Full task string]    -> "tambah", kT + date - kTP
# ["update", Full task string] -> "deadline" + taskDatabase + date
# ["done", Full task string]   -> "selesai" + taskDatabase
# ["delete", Full task string] -> "hapus" + taskDatabase
# ["see", [Task list]]         -> "deadline"
# ["help", None]               -> "bantuan", "fitur"
# [None, None]                 -> No matching query


def isArrayRegexFound(sourceArray, targetString):
    for pattern in sourceArray:
        if re.search(pattern, targetString.lower()) != None:
            return True
    return False

def evaluateString(targetString):
    resultingQuery = [None, None]

    if re.search("tambah", targetString) != None or isArrayRegexFound(kataTugas, targetString):
        tempString = targetString
        for tidakPenting in kataTidakPenting:
            tempString = tempString.replace(tidakPenting, " ")
        dateArray = DateRegex.getDate(tempString)
        if dateArray != None:
            resultingQuery[0] = "add"
            resultingQuery[1] = [dateArray, DateRegex.stripDate(tempString)]
            # TODO : Add to database

    # TODO : Recommendation
    return resultingQuery


# Testing
temp = input()
print(evaluateString(temp))
