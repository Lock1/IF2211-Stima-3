import re

monthString = ["januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"]

def getSlashedDate(stringSource):
    resultingDate = []
    stringSource = stringSource.replace("/", " ")
    regexResult = re.search("(.|)[0-9] (.|)[0-9] [0-9][0-9][0-9][0-9]", stringSource)
    if regexResult != None:
        # Get index
        matchedIndexTuple = regexResult.span()

        # Casting to date
        resultingDate.append(int(stringSource[matchedIndexTuple[0]:matchedIndexTuple[0]+2]))
        resultingDate.append(int(stringSource[matchedIndexTuple[0]+3:matchedIndexTuple[0]+5]))

        # Get year
        regexResult = re.search(" [0-9][0-9][0-9][0-9]", stringSource)
        matchedIndexTuple = regexResult.span()
        resultingDate.append(int(stringSource[matchedIndexTuple[0]:matchedIndexTuple[0]+5]))
    return resultingDate


def getStringDate(stringSource, monthFound):
    resultingDate = []
    regexResult = re.search("(.|)[0-9] (.|)(.|)(.|)(.|)(.|)(.|)(.|)(.|)(.|) [0-9][0-9][0-9][0-9]", stringSource)
    if regexResult != None:
        # Get index
        matchedIndexTuple = regexResult.span()

        # Casting to date
        resultingDate.append(int(stringSource[matchedIndexTuple[0]:matchedIndexTuple[0]+2]))
        resultingDate.append(int(monthString.index(monthFound) + 1))
        regexResult = re.search("[0-9][0-9][0-9][0-9]", stringSource)
        matchedIndexTuple = regexResult.span()
        resultingDate.append(int(stringSource[matchedIndexTuple[0]:matchedIndexTuple[0]+4]))
    return resultingDate


def getDate(stringSource):
    # Get first occuring
    removedString = stringSource.replace("/", " ")
    regexStringDate = re.search("(.|)[0-9] (.|)(.|)(.|)(.|)(.|)(.|)(.|)(.|)(.|) [0-9][0-9][0-9][0-9]", removedString)
    regexSlashDate = re.search("(.|)[0-9] (.|)[0-9] [0-9][0-9][0-9][0-9]", removedString)

    slashDateInterval = []
    if regexSlashDate != None:
        slashDateInterval = regexSlashDate.span()

    stringDateInterval = []
    if regexStringDate != None:
        stringDateInterval = regexStringDate.span()

    # Interval selection
    selectedInterval = ""
    if len(stringDateInterval) > 0 and len(slashDateInterval) > 0:
        if stringDateInterval[0] < slashDateInterval[0]:
            selectedInterval = "string based"
        else:
            selectedInterval = "slash based"
    elif len(stringDateInterval) > 0:
        selectedInterval = "string based"
    elif len(slashDateInterval) > 0:
        selectedInterval = "slash based"

    if len(selectedInterval) > 0:
        # Date/Month/Year
        if selectedInterval == "slash based":
            if re.search("/", stringSource) != None:
                return getSlashedDate(stringSource)

        # Date MonthString Year
        else:
            for month in monthString:
                if re.search(month.lower(), stringSource.lower()) != None:
                    return getStringDate(stringSource, month)

    return []


def stripDate(stringSource):
    strippedString = stringSource
    # Remove month
    for month in monthString:
        strippedString = strippedString.replace(month, " ")

    # Remove slash & number
    strippedString = strippedString.replace("/", " ")
    for i in range(10):
        strippedString = strippedString.replace(str(i), " ")

    # Remove multiple space
    strippedString = " ".join(strippedString.split())
    return strippedString


def dateArrayToString(dateArray):
    resultString = str(dateArray)
    resultString = resultString.replace(", ", "/")
    resultString = resultString.replace("[", "")
    resultString = resultString.replace("]", "")
    return resultString


def removeOneDate(targetString):
    removedString = targetString
    removedString = removedString.replace("/", " ")
    regexStringDate = re.search("(.|)[0-9] (.|)(.|)(.|)(.|)(.|)(.|)(.|)(.|)(.|) [0-9][0-9][0-9][0-9]", removedString)
    regexSlashDate = re.search("(.|)[0-9] (.|)[0-9] [0-9][0-9][0-9][0-9]", removedString)

    slashDateInterval = []
    if regexSlashDate != None:
        slashDateInterval = regexSlashDate.span()

    stringDateInterval = []
    if regexStringDate != None:
        stringDateInterval = regexStringDate.span()

    # Interval selection
    selectedInterval = []
    if len(stringDateInterval) > 0 and len(slashDateInterval) > 0:
        if stringDateInterval[0] < slashDateInterval[0]:
            selectedInterval = stringDateInterval
        else:
            selectedInterval = slashDateInterval
    elif len(stringDateInterval) > 0:
        selectedInterval = stringDateInterval
    elif len(slashDateInterval) > 0:
        selectedInterval = slashDateInterval

    # Removing date
    if len(selectedInterval) > 0:
        removedString = ""
        for i in range(len(targetString)):
            if selectedInterval[0] <= i and i < selectedInterval[1]:
                removedString += " "
            else:
                removedString += targetString[i]

    # Remove multiple space
    removedString = " ".join(removedString.split())
    return removedString
