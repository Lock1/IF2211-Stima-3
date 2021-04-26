import csv
impword = []
tskword = []
presuffix = []
def start(imp, tsk):
    with open (imp, newline = '') as f:
        temp = f.read()
        s = ""
        for i in temp:
            if(i == ','):
                impword.append(s)
                s = ""
            else:
                s += i
    with open (tsk, newline = '') as f:
        temp = f.read()
        s = ""
        for i in temp:
            if(i == ','):
                tskword.append(s)
                s = ""
            else:
                s += i
#Exact String Matching
def KMP(word, pattern):
    #print(impword)
    #print(tskword)
    lenword = len(word)
    lenpattern = len(pattern)
    print(lenword)
    print(lenpattern)
    idx1 = idx2 = 0
    presuffix = [0] * lenpattern
    presuffixx(pattern, lenpattern, presuffix)
    while idx1 < lenword:
        if pattern[idx2] == word[idx1]:
            idx1 += 1
            idx2 += 1
        if idx2 == lenpattern:
            return True
            idx2 = presuffix[idx2 - 1]
        elif idx1 < lenword and pattern[idx2] != word[idx1]:
            if idx2 != 0:
                idx2 = presuffix[idx2 - 1]
            else:
                idx1 += 1
    return False
def presuffixx(pattern, lenpattern, presuffix):
    temp = 0
    presuffix[0]
    idx = 1
    while idx < lenpattern:
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

start("katapenting.csv", "katatugas.csv")
x = str(input("Kata: " ))
y = str(input("Pola: "))
testKMP = KMP(x, y)
print(testKMP)