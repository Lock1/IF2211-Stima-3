import StringMatching
import DateRegex
import re
import datetime

keyword = ["hapus", "deadline", "selesai", "tambah", "kapan", "apa", "fitur", "bantuan"]
kataPenting = ["kelompok", "meet", "mata kuliah"]
kataDurasi = ["bulan", "minggu", "hari", "antara"]
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


def isArrayMatchFound(sourceArray, targetString):
    for pattern in sourceArray:
        if StringMatching.KMP(targetString.lower(), pattern):
            return True
    return False

def isDateArrayAndDateTimeEqual(dateArray, dateTime):
    isDayMatch = (dateArray[0] == dateTime.day)
    isMonthMatch = (dateArray[1] == dateTime.month)
    isYearMatch = (dateArray[2] == dateTime.year)
    return isDayMatch and isMonthMatch and isYearMatch

def isDateTimeEqual(dateTime1, dateTime2):
    isDayMatch = (dateTime1.day == dateTime2.day)
    isMonthMatch = (dateTime1.month == dateTime2.month)
    isYearMatch = (dateTime1.year == dateTime2.year)
    return isDayMatch and isMonthMatch and isYearMatch




# ----- evaluateString() return list -----
# In descending order
# ["add", Full task string]    -> "tambah", kT + date - kTP
# ["see-specific", [Task list]]-> "deadline" + kD + number / "deadline" + date + date
# ["see", [Task list]]         -> "apa" + "deadline" / "kapan" + "deadline"
# ["update", Full task string] -> "deadline" + taskDatabase + date
# ["done", Full task string]   -> "selesai" + taskDatabase
# ["delete", Full task string] -> "hapus" + taskDatabase
# ["help", None]               -> "bantuan", "fitur"
# ["search-fail", TaskString]  -> Database lookup failed, TaskString is "add", "see", "delete", etc
# ["recommend", [Keyword]]     -> No exact keyword match found, [Keyword] list of nearest keyword
# [None, None]                 -> No matching query

def evaluateString(targetString):
    queryResult = [None, None]

    # Adding branch
    if StringMatching.KMP(targetString.lower(), "tambah") or isArrayMatchFound(kataTugas, targetString):
        tempString = targetString
        for tidakPenting in kataTidakPenting:
            tempString = tempString.replace(tidakPenting, " ")
        dateArray = DateRegex.getDate(tempString)
        if dateArray != None:
            # TODO : Relative
            queryResult[0] = "add"
            queryResult[1] = [dateArray, DateRegex.stripDate(tempString)]
            database.append([dateArray, DateRegex.stripDate(tempString)])

    # Updating and list branch
    elif StringMatching.KMP(targetString.lower(), "deadline"):
        # List deadline
        if isArrayMatchFound(kataDurasi, targetString.lower()):
            resultDateFilter = []
            currentDate = datetime.datetime.now()
            numberRegex = re.search("[0-9]+", targetString)
            dateArray = DateRegex.getDate(targetString.lower())
            # Duration checking
            if StringMatching.KMP(targetString.lower(), "hari") and StringMatching.KMP(targetString.lower(), "ini"):
                for databaseEntry in database:
                    if isDateArrayAndDateTimeEqual(databaseEntry[0], currentDate):
                        dateString = DateRegex.dateArrayToString(databaseEntry[0])
                        mergedDateString = databaseEntry[1] + " " + DateRegex.dateArrayToString(dateString)
                        resultDateFilter.append(mergedDateString)

            elif StringMatching.KMP(targetString.lower(), "hari") and numberRegex != None:
                numberInterval = numberRegex.span()
                daySpan = int(targetString[numberInterval[0]:numberInterval[1]])
                for i in range(daySpan+1):
                    for databaseEntry in database:
                        if isDateArrayAndDateTimeEqual(databaseEntry[0], currentDate):
                            dateString = DateRegex.dateArrayToString(databaseEntry[0])
                            mergedDateString = databaseEntry[1] + " " + DateRegex.dateArrayToString(dateString)
                            resultDateFilter.append(mergedDateString)
                    currentDate += datetime.timedelta(days=1)

            elif StringMatching.KMP(targetString.lower(), "minggu") and numberRegex != None:
                numberInterval = numberRegex.span()
                # Multiplied by 7
                daySpan = 7*int(targetString[numberInterval[0]:numberInterval[1]])
                for i in range(daySpan+1):
                    for databaseEntry in database:
                        if isDateArrayAndDateTimeEqual(databaseEntry[0], currentDate):
                            dateString = DateRegex.dateArrayToString(databaseEntry[0])
                            mergedDateString = databaseEntry[1] + " " + DateRegex.dateArrayToString(dateString)
                            resultDateFilter.append(mergedDateString)
                    currentDate += datetime.timedelta(days=1)

            elif StringMatching.KMP(targetString.lower(), "bulan") and numberRegex != None:
                numberInterval = numberRegex.span()
                # Multiplied by 30
                daySpan = 30*int(targetString[numberInterval[0]:numberInterval[1]])
                for i in range(daySpan+1):
                    for databaseEntry in database:
                        if isDateArrayAndDateTimeEqual(databaseEntry[0], currentDate):
                            dateString = DateRegex.dateArrayToString(databaseEntry[0])
                            mergedDateString = databaseEntry[1] + " " + DateRegex.dateArrayToString(dateString)
                            resultDateFilter.append(mergedDateString)
                    currentDate += datetime.timedelta(days=1)

            elif len(dateArray) > 0:
                removedString = DateRegex.removeOneDate(targetString.lower())
                secondDateArray = DateRegex.getDate(removedString)
                if len(secondDateArray) > 0:
                    isDateIntervalValid = False
                    for i in range(2,-1, -1):
                        if dateArray[i] < secondDateArray[i]:
                            isDateIntervalValid = True
                            break

                    if not isDateIntervalValid:
                        tempArray = secondDateArray
                        secondDateArray = dateArray
                        dateArray = tempArray

                    dateIter = datetime.datetime(dateArray[2], dateArray[1], dateArray[0])
                    targetDate = datetime.datetime(secondDateArray[2], secondDateArray[1], secondDateArray[0]+1)
                    while not isDateTimeEqual(dateIter, targetDate):
                        for databaseEntry in database:
                            if isDateArrayAndDateTimeEqual(databaseEntry[0], dateIter):
                                dateString = DateRegex.dateArrayToString(databaseEntry[0])
                                mergedDateString = databaseEntry[1] + " " + DateRegex.dateArrayToString(dateString)
                                resultDateFilter.append(mergedDateString)
                        dateIter += datetime.timedelta(days=1)

            # Result of finding specific duration
            if len(resultDateFilter) > 0:
                queryResult[0] = "see-specific"
                queryResult[1] = resultDateFilter
            else:
                queryResult[0] = "search-failed"
                queryResult[1] = "see-specific"

        elif StringMatching.KMP(targetString.lower(), "kapan"):
            # Single entry searching
            resultDatabaseQuery = databaseLookup(targetString.lower())
            if resultDatabaseQuery != None:
                queryResult[0] = "see"
                dateString = DateRegex.dateArrayToString(database[resultDatabaseQuery[0]][0])
                queryResult[1] = resultDatabaseQuery[1] + " " + DateRegex.dateArrayToString(dateString)
            else:
                queryResult[0] = "search-failed"
                queryResult[1] = "see"

        elif StringMatching.KMP(targetString.lower(), "apa"):
            # All entry
            queryResult[0] = "see"
            queryResult[1] = database

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
            else:
                queryResult[0] = "search-failed"
                queryResult[1] = "update"

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
        else:
            queryResult[0] = "search-failed"
            if StringMatching.KMP(targetString.lower(), "hapus"):
                queryResult[1] = "delete"
            else:
                queryResult[1] = "done"

    # Help branch
    elif StringMatching.KMP(targetString.lower(), "fitur") or StringMatching.KMP(targetString.lower(), "bantuan"):
        queryResult[0] = "help"

    # No keyword match
    else:
        availableRecommendation = []
        for word in keyword:
            if StringMatching.matchingPercentage(targetString.lower(), word) > 0.6:
                availableRecommendation.append(word)

        if len(availableRecommendation) > 0:
            queryResult[0] = "recommend"
            queryResult[1] = availableRecommendation

    return queryResult


# Testing
while 1:
    temp = input()
    print(evaluateString(temp))
