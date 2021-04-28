presuffix = []

#Exact String Matching
def KMP(word, pattern):
    lenword = len(word)
    lenpattern = len(pattern)
    idx1 = idx2 = 0
    presuffix = [0] * lenpattern
    presuffixx(pattern, presuffix)
    print(presuffix)
    while idx1 < lenword:
        if pattern[idx2] == word[idx1]:
            idx1 += 1
            idx2 += 1
        if idx2 == lenpattern:
            return True
        elif idx1 < lenword and pattern[idx2] != word[idx1]:
            if idx2 != 0:
                idx2 = presuffix[idx2 - 1]
            else:
                idx1 += 1
    return False

def presuffixx(pattern, presuffix):
    temp = 0
    idx = 1
    while idx < len(pattern):
        if pattern[idx] == pattern[temp]:
            temp += 1
            presuffix[idx] = temp
            idx += 1
        else:
            if temp != 0:
                temp = presuffix[temp - 1]
            else:
                presuffix[idx] = 0
                idx += 1

#TO DO:
#Approximation Matching
#Levenshtein
def Levenshtein(word, pattern):
    lenword = len(word)
    lenpattern = len(pattern)
    levdist = [[ 0 for j in range(lenword + 1) ] for i in range(lenpattern + 1)]
    #print(levdist)
    for i in range(lenpattern + 1):
        levdist[i][0] = i
    for i in range(lenword + 1):
        levdist[0][i] = i
    for i in range(1, lenpattern + 1):
        for j in range(1, lenword + 1):
            if (pattern[i - 1] == word[j - 1]):
                levdist[i][j] = levdist[i - 1][j - 1]
            else:
                temp1 = levdist[i][j - 1]
                temp2 = levdist[i - 1][j - 1]
                temp3 = levdist[i - 1][j]
                if (temp1 <= temp2 and temp1 <= temp2):
                    levdist[i][j] = temp1 + 1
                elif (temp2 <= temp1 and temp2 <= temp3):
                    levdist[i][j] = temp2 + 1
                else:
                    levdist[i][j] = temp3 + 1
    return levdist[lenpattern][lenword]

def matchingPercentage(word, pattern):
    lenword = len(word)
    lenpattern = len(pattern)
    #print(Levenshtein(word, pattern))
    return float("{:.2f}".format((lenword + lenpattern - Levenshtein(word, pattern)) / (lenword + lenpattern)))


#TEST
# x = input("Kata: " )
# y = input("Pola: ")
# testKMP = KMP(x, y)
# if(testKMP == True):
#     print("Kecocokan ditemukan\n")
# else:
#     print("Tingkat Kecocokan sebesar", matchingPercentage(x, y), "ditemukan.\n")
