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
        resultingDate.append(monthString.index(monthFound) + 1)
        regexResult = re.search("[0-9][0-9][0-9][0-9]", stringSource)
        matchedIndexTuple = regexResult.span()
        resultingDate.append(int(stringSource[matchedIndexTuple[0]:matchedIndexTuple[0]+4]))
    return resultingDate


def getDate(stringSource):
    # Date/Month/Year
    if re.search("/", stringSource) != None:
        return getSlashedDate(stringSource)

    # Date MonthString Year
    for month in monthString:
        if re.search(month.lower(), stringSource.lower()) != None:
            return getStringDate(stringSource, month)

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
