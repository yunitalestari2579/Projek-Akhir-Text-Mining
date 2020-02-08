from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import csv
import codecs

def tokenisasi(doc:str):
    doc.replace('-', ' ')
    token = doc.split(' ')
    for i in range(len(token)):
        token[i] = token[i].lower()
    return token

def isInList(w:str, l:list, awal, akhir):
    #fungsi ini menggunakan binary search
    if(akhir >= awal):
        tengah = int((akhir+awal)/2)
        if(w == l[tengah]):
            return True
        elif(w < l[tengah]):
            return isInList(w, l, awal, tengah-1)
        elif(w > l[tengah]):
            return isInList(w, l, tengah+1, akhir)
    else:
        return False

def filtering(tokens:list):
    file = open('stopword_list_tala.txt', 'r')
    stoplist, filters = list(), list()
    stoplist = file.read().split("\n")
    for i in range(len(tokens)):
        if(not isInList(tokens[i], stoplist, 0, (len(stoplist)-1))):
            filters.append(tokens[i])
    return filters

def cetakList(l:list):
    for i in range(len(l)):
        print('Dok', i, ' : ', l[i])

def PreProcessing(D:list, S:str):
    ### TOKENISASI
    Token_AllDocs = []
    for i in range(len(D)):
        t = tokenisasi(D[i])
        #print(t)
        Token_AllDocs.append(t)
    #print("\nHASIL TOKENISASI :")
    #cetakList(Token_AllDocs)

    ### FILTERING
    Filtering_AllDocs = []
    for i in range(len(Token_AllDocs)):
        f = filtering(Token_AllDocs[i])
        Filtering_AllDocs.append(f)
    #print("\nHASIL FILTERING :")
    #cetakList(Filtering_AllDocs)

    ### STEMMING
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    Stemming_AllDocs = []
    for i in range(len(Filtering_AllDocs)):
        s =list()
        for j in range(len(Filtering_AllDocs[i])):
            ss = stemmer.stem(Filtering_AllDocs[i][j])
            s.append(ss)
        Stemming_AllDocs.append(s)
    #print("\nHASIL STEMMING :")
    #cetakList(Stemming_AllDocs)

    ### TYPE
    Type_AllDocs = []
    for i in range(len(Stemming_AllDocs)):
        ty = list(dict.fromkeys(Stemming_AllDocs[i]))
        Type_AllDocs.append(ty)
    #print("\nHASIL TYPING :")
    #cetakList(Type_AllDocs)

    ### TERM
    Term_AllDocs = Type_AllDocs
    #print("\nHASIL TERM :")
    #cetakList(Term_AllDocs)
    
    if(S == "getStem"):
        return Stemming_AllDocs
    elif(S == "getTerm"):
        return Term_AllDocs

def main():
    with codecs.open('../Kelompok 9.csv', 'r', encoding='ascii', errors='ignore') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        D = list()
        for row in readCSV:
            D.append(row[0])
        PP = PreProcessing(D, "getTerm")
        print(PP)

#main()