# File main.py

import KMP
import BM
import colorama
from colorama import Fore
import numpy as np
import time

def main():
    # Baca input file
    filename = input("Masukkan path relative file: ")
    file = open(filename, 'r')

    matrix = []
    lines = file.readlines()

    for i, line in enumerate(lines):
        if (line.strip() == ''):
            break
        matrix.append(line.strip().split(' '))
    matrix = np.array(matrix)

    words = []
    i += 1
    while (i < len(lines)):
        if (lines[i].strip() != ''):
            words.append(lines[i].strip())
        i += 1

    file.close()

    start_time = time.time()
    # Cari kata pada matriks 
    wordMatrix = []
    m = len(matrix)
    n = len(matrix[0])
    
    # Menyimpan text dengan arah diagonal ke dalam sebuah array
    digRowP = []
    digRowN = []
    digColP = []
    digColN = []
    # arah diagonal gradien positif bagian baris
    for i in range(m):
        text = []
        k = i
        while (n-(k-i)-1 >= 0 and k < m):
            text.append(matrix[k][n-(k-i)-1])
            k += 1
        digRowP.append(text)

    # arah diagonal gradien positif bagian kolom
    for j in range(n-1):
        text = []
        k = 0
        while (j-k >= 0 and k < m):
            text.append(matrix[k][j-k])
            k += 1
        digColP.append(text)
    
    # arah diagonal gradien negatif bagian baris
    for i in range(m):
        text = []
        k = i
        while (k-i < n and k < m):
            text.append(matrix[k][k-i])
            k += 1
        digRowN.append(text)
    
    # arah diagonal gradien negatif bagian kolom
    for j in range(1,n):
        text = []
        k = 0
        while (k+j < n and k < m):
            text.append(matrix[k][k+j])
            k += 1
        digColN.append(text)

    # Memeriksa setiap baris
    for word in words:
        l = len(word)   
        for i in range(m):
            # arah kanan
            idx = KMP.kmpMatch(matrix[i], word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(idx, idx+l):
                    arrayOfIdxWord.append([i, k])
                wordMatrix.append(arrayOfIdxWord)
                break
            # arah kiri
            idx = KMP.kmpMatch(reverse(matrix[i]), word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(n-idx-1, n-idx-1-l, -1):
                    arrayOfIdxWord.append([i, k])
                wordMatrix.append(arrayOfIdxWord)
                break
    
        # Memeriksa setiap kolom
        for j in range(n):
            # bawah
            idx = KMP.kmpMatch(matrix[:, j], word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(idx, idx+l):
                    arrayOfIdxWord.append([k, j])
                wordMatrix.append(arrayOfIdxWord)
                break
            
            # atas
            idx = KMP.kmpMatch(reverse(matrix[:, j]), word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(m-idx-1, m-idx-1-l, -1):
                    arrayOfIdxWord.append([k, j])
                wordMatrix.append(arrayOfIdxWord)
                break

        # Memeriksa teks dengan arah diagonal
        # arah diagonal gradien positif bagian baris
        for i, text in enumerate(digRowP):
            idx = KMP.kmpMatch(text, word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([i+idx+k, n-idx-k-1])
                wordMatrix.append(arrayOfIdxWord)
                break

            idx = KMP.kmpMatch(reverse(text), word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([i+(len(text)-idx-1)-k, (n-len(text))+idx+k])
                wordMatrix.append(arrayOfIdxWord)
                break
        
        # arah diagonal gradien positif bagian kolom
        for i, text in enumerate(digColP):
            idx = KMP.kmpMatch(text, word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([idx+k, i-idx-k])
                wordMatrix.append(arrayOfIdxWord)
                break

            idx = KMP.kmpMatch(reverse(text), word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([len(text)-idx-k-1, (i-len(text))+idx+k+1])
                wordMatrix.append(arrayOfIdxWord)
                break
     
        # arah diagonal gradien negatif bagian baris
        for i, text in enumerate(digRowN):
            idx = KMP.kmpMatch(text, word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([i+idx+k, idx+k])
                wordMatrix.append(arrayOfIdxWord)
                break

            idx = KMP.kmpMatch(reverse(text), word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([(i+len(text))-idx-k-1, len(text)-idx-k-1])
                wordMatrix.append(arrayOfIdxWord)
                break

        # arah diagonal gradien negatif bagian kolom
        for i, text in enumerate(digColN):
            idx = KMP.kmpMatch(text, word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([idx+k, i+idx+1+k])
                wordMatrix.append(arrayOfIdxWord)
                break

            idx = KMP.kmpMatch(reverse(text), word)
            if (idx != -1):
                arrayOfIdxWord = []
                for k in range(l):
                    arrayOfIdxWord.append([len(text)-idx-k-1, i+len(text)-idx-k])
                wordMatrix.append(arrayOfIdxWord)
                break
    end_time = time.time()
    # Menampilkan hasil search word di puzzle
    colorama.init(autoreset=True)
    result = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append([matrix[i][j], -1])
        result.append(row)
    
    for i in range(len(wordMatrix)):
        for row in wordMatrix[i]:
            result[row[0]][row[1]][1] = i % 7
    
    for row in result:
        for col in row:
            if (col[1] == -1):
                print(col[0], end=' ')
            elif (col[1] == 0):
                print(Fore.RED + str(col[0]), end=' ')
            elif (col[1] == 1):
                print(Fore.GREEN + str(col[0]), end=' ')
            elif (col[1] == 2):
                print(Fore.YELLOW + str(col[0]), end=' ')
            elif (col[1] == 3):
                print(Fore.BLUE + str(col[0]), end=' ')
            elif (col[1] == 4):
                print(Fore.MAGENTA + str(col[0]), end=' ')
            else:
                print(Fore.CYAN + str(col[0]), end=' ')
        print()
        
    print("\n--- %s seconds ---" % (end_time - start_time))

def reverse(array):
    li = []
    for i in range(len(array) - 1, -1, -1):
        li.append(array[i])
    return li

if __name__ == "__main__":
    main()