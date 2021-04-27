kataPenting = ["kelompok", "deadline", "meet", "mata kuliah", "tambah", "hapus", "ada"]
kataTugas = ["kuis", "ujian", "tucil", "tubes", "praktikum", "laporan"]
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

# start("katapenting.csv", "katatugas.csv")
x = input("Kata: " )
y = input("Pola: ")
testKMP = KMP(x, y)
print(testKMP)
