import PreProcessing as pp
from collections import defaultdict
import math

def make_matrix(stem:list):
    stem_1D = list()
    for i in range(len(stem)):
        for j in range(len(stem[i])):
            stem_1D.append(stem[i][j])
    baris = list(dict.fromkeys(stem_1D))
    matrix = defaultdict(dict)
    for b in baris:
        for d in range(len(stem)):
            jumlah = 0
            for w in range(len(stem[d])):
                if(b == stem[d][w]):
                    jumlah+=1
            matrix[b][d] = jumlah
    return matrix


def Tf(matrix:defaultdict(dict)):
    tf_matrix = defaultdict(dict)
    for b in matrix:
        for d in matrix[b]:
            if(matrix[b][d]  > 0):
                tf_matrix[b][d] = 1 + math.log10(matrix[b][d])
            else :
                tf_matrix[b][d] = 0
    return tf_matrix

def IDf(matrix:defaultdict(dict)):
    idf_matrix = defaultdict(dict)
    for b in matrix:
        Df = 0
        for d in matrix[b]:
            if(matrix[b][d] != 0):
                Df += 1
        idf_matrix[b] = math.log10(len(matrix[b])/Df)
    return idf_matrix

def Tf_IDf(matrix:defaultdict(dict)):
    tfidf = defaultdict(dict)
    tf = Tf(matrix)
    idf = IDf(matrix)
    for b in matrix:
        for d in matrix[b]:
            tfidf[b][d] = tf[b][d] * idf[b]
    return tfidf

def cetak_matrix(matrix:defaultdict(dict), s:str):
    print("\n", s)
    for b in matrix:
        print("%8s |" %(b), end='')
        for d in matrix[b]:
            print(" {n:3.3f}".format(n=matrix[b][d]), end=' ')
        print()

def main():
    D = list(None for i in range(4))
    D[0] = "Kupu kupu terbang di atas pohon"
    D[1] = "Dia terbang sambil mencari pohon untuk bertelur"
    D[2] = "Pohon tempat kupu kupu bertelur adalah pohon mangga"
    D[3] = "Kupu kupu bertelur untuk berkembang biak"
    stem = pp.PreProcessing(D, "getStem")
    matrix = make_matrix(stem)
    tfidf = Tf_IDf(matrix)
    cetak_matrix(matrix, '-------------Bobot Raw TF-------------')
    cetak_matrix(tfidf, '-------------Bobot Tf-IDf-------------')

#main()