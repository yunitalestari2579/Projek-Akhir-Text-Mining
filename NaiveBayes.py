import csv
import codecs
import PreProcessing as pp
import TermWeighting as tw
from collections import defaultdict

def count(alldoc, sentimen:int):
    hasil = 0
    if(sentimen == 0):
        # 13-24 merupakan dokumen dengan sentimen negatif
        for i in range(13, 24):
            hasil += alldoc[i]
    else:
        # 0-12 merupakan dokumen dengan sentimen positif
        for i in range(0, 12):
            hasil += alldoc[i]
    return hasil

def cond_prob(matrix:defaultdict(dict)):
    P = defaultdict(dict)
    countPos = 0
    countNeg = 0
    for b in matrix:
        countTermPos = count(matrix[b], 1)
        countTermNeg = count(matrix[b], 0)
        countPos += countTermPos
        countNeg += countTermNeg
        P[b][0] = (countTermNeg+1)/(countNeg+len(matrix))
        P[b][1] = (countTermPos+1)/(countPos+len(matrix))
    return P

def read_dataset():
    D = list()
    positif = negatif = 0
    with codecs.open('Kelompok 9.csv', 'r', encoding='ascii', errors='ignore') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            #row[0] merujuk ke kalimatnya, row[8] merujuk ke sentimennya
            D.append([row[0], row[8]])
            if(row[8] == 'Positif'):
                positif+=1
            else:
                negatif+=1
    return D, positif, negatif

def Training(D:list, positif:int, negatif:int):
    #D[0] merujuk pada dokumen
    #D[1] merujuk pada sentimennya

    # Hitung probabilitas prior
    prior_negatif = negatif/len(D[0])
    prior_positif = positif/len(D[0])

    # Lakukan PreProcessing
    PP = pp.PreProcessing(D[0], "getStem")
    # Hitung Raw Term
    rt = tw.make_matrix(PP)

    # Hitung conditional probability
    cp = cond_prob(rt)
    #tw.cetak_matrix(cp, "Hasil Training")

    return prior_negatif, prior_positif, cp

def Testing(D_uji, PNeg, PPos, CP):
    testSentence = D_uji[0]
    print("\nKalimat Uji : ", testSentence)
    splitted = testSentence.split(' ')
    for word in splitted:
        for b in CP:
            if(b == word):
                PNeg *= CP[b][0]
                PPos *= CP[b][1]
    #print("Prob Negatif : ", PNeg)
    #print("Prob Positif : ", PPos)
    if(PNeg > PPos):
        print("Hasil Uji : Negatif", end =' vs ')
        hasil = "Negatif"
    else:
        print("Hasil Uji : Positif", end =' vs ')
        hasil = "Positif"
    print("Sentimen Asli :", D_uji[1])
    if hasil==D_uji[1] :
        return 1
    else:
        return 0

#fungsi untuk melakukan pengujian k-fold
def Testing_kfold(k:int):
    # D adl singkatan dari Dokumen
    D, pos, neg = read_dataset()
    #pd perulangan di bawah D akan diotak-atik,
    #maka sebaiknya buat list backup yang menyimpan kondisi asli dataset
    D_backup = D.copy()
    uji = list()
    jumlah_uji = len(D)/k
    akurasi_mean = j = 0
    for i in range(1, k+1):
        print("\nPENGUJIAN FOLD ke-", i)
        correct = 0
        #pemilihan data uji dan penghilangan data tsb dari dokumen
        uji.append(D.pop(j)); uji.append(D.pop(j)); uji.append(D.pop(j))
        uji.append(D.pop(j+12)); uji.append(D.pop(j+12)); uji.append(D.pop(j+12))
        j += 3
        #lakukan training
        PNeg, PPos, CP = Training(D[0], pos - jumlah_uji/2, neg - jumlah_uji/2)
        #lakukan testing
        for u in uji:
            correct  += Testing(u, PNeg, PPos, CP)
        print("Akurasi : ", correct/jumlah_uji)
        akurasi_mean += correct/jumlah_uji
        #Kembalikan dokumen seperti semula
        D = D_backup.copy()
        uji.clear()
    print("\nAKURASI RATA-RATA : ", akurasi_mean/k)

Testing_kfold(5)