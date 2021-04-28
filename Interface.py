import StringMatching
import DateRegex
import re

keyword = ["hapus", "deadline", "selesai"]
kataPenting = ["kelompok", "meet", "mata kuliah"]
kataDurasi = ["bulan", "minggu", "hari"]
kataTugas = ["kuis", "ujian", "tucil", "tubes", "praktikum", "laporan"]
kataTidakPenting = ["pada", "tentang", "ke", "jadi", "tambah"]

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
# ["see", [Task list]]         -> "apa" + "deadline" / "kapan" + "deadline"
# ["update", Full task string] -> "deadline" + taskDatabase + date
# ["done", Full task string]   -> "selesai" + taskDatabase
# ["delete", Full task string] -> "hapus" + taskDatabase
# ["help", None]               -> "bantuan", "fitur"
# [None, None]                 -> No matching query

def evaluateString(targetString):
    queryResult = [None, None]

    # Adding branch
    if StringMatching.KMP(targetString.lower(), "tambah") or isArrayRegexFound(kataTugas, targetString):
        tempString = targetString
        for tidakPenting in kataTidakPenting:
            tempString = tempString.replace(tidakPenting, " ")
        dateArray = DateRegex.getDate(tempString)
        if dateArray != None:
            queryResult[0] = "add"
            queryResult[1] = [dateArray, DateRegex.stripDate(tempString)]
            database.append([dateArray, DateRegex.stripDate(tempString)])

    # Updating and list branch
    elif StringMatching.KMP(targetString.lower(), "deadline"):
        # List all deadline
        if StringMatching.KMP(targetString.lower(), "apa") or StringMatching.KMP(targetString.lower(), "kapan"):
            # tempString = targetString
            # for tidakPenting in kataTidakPenting:
            #     tempString = tempString.replace(tidakPenting, " ")
            # dateArray = DateRegex.getDate(tempString)
            # tempString = DateRegex.stripDate(tempString)

            # resultDatabaseQuery = databaseLookup(tempString)
            # if resultDatabaseQuery != None and dateArray != None:
            #     database[resultDatabaseQuery[0]][0] = dateArray
            queryResult[0] = "see"
            queryResult[1] = database
                # queryResult[1] = resultDatabaseQuery[1] + " " + DateRegex.dateArrayToString(dateArray)

        # Updating task
        else:
            tempString = targetString
            for tidakPenting in kataTidakPenting:
                tempString = tempString.replace(tidakPenting, " ")
            dateArray = DateRegex.getDate(tempString)
            tempString = DateRegex.stripDate(tempString)

            resultDatabaseQuery = databaseLookup(tempString)
            if resultDatabaseQuery != None and dateArray != None:
                database[resultDatabaseQuery[0]][0] = dateArray
                queryResult[0] = "update"
                queryResult[1] = resultDatabaseQuery[1] + " " + DateRegex.dateArrayToString(dateArray)

    # Solved task and delete branch
    elif StringMatching.KMP(targetString.lower(), "selesai") or StringMatching.KMP(targetString.lower(), "hapus"):
        tempString = targetString
        for tidakPenting in kataTidakPenting:
            tempString = tempString.replace(tidakPenting, " ")
        tempString = DateRegex.stripDate(tempString)

        resultDatabaseQuery = databaseLookup(tempString)
        if resultDatabaseQuery != None:
            if StringMatching.KMP(targetString.lower(), "hapus"):
                queryResult[0] = "delete"
            else:
                    queryResult[0] = "done"
            dateString = DateRegex.dateArrayToString(database[resultDatabaseQuery[0]][0])
            queryResult[1] = resultDatabaseQuery[1] + " " + dateString
            database.pop(resultDatabaseQuery[0])

    # Help branch
    elif StringMatching.KMP(targetString.lower(), "fitur") or StringMatching.KMP(targetString.lower(), "bantuan"):
        queryResult[0] = "help"

    # TODO : Recommendation
    return queryResult


# Testing
while 1:
    temp = input()
    print(evaluateString(temp))
