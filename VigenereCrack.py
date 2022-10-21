#PROGRAMMA CHE DECIFRA UN TESTO CIFRATO TRAMITE CIFRARIO DI VIGENERE A PARTIRE
#DA UN PLAINTEXT IN INGLESE

import numpy as np

#FUNZIONE PRINCIPALE
def VigenereCrack(x, m, p):
    #formattazione cyphertext in matrice
    n = int(len(x)/m)
    A = np.zeros((m, n), dtype = str)
    key = [] #lista in cui metto i valori relativi alle lettere della chiave
    for j in range(n):
        for i in range(m):
            A[i][j] = x[j*m + i]
    #creazione stringa da passare alla funzione che calcola gli indici di coincidenza di ogni riga
    for i in range(m):
        y = ""
        for j in range(n):
            y += A[i][j]
        IndexCoincidence(y, i) #prende in ingresso ogni volta una riga della matrice
        key.append(keyCrack(y, m, p)) #prende in ingresso ogni volta una riga della matrice
        print("\n")
    print("la chiave è ", key)


#funzione che calcola l'indice di coincidenza di una stringa y
def IndexCoincidence(y, k):
    arr = np.zeros(26)
    for i in y:
        for j in range(65, 91):#range di codici ASCII per le lettere A-Z
            if i == chr(j):
                 arr[j-65] += 1
                 break
    sum = 0
    for i in range(26):
        sum += (arr[i]*(arr[i]-1))/(len(y)*(len(y)-1))
    print("l' indice di coincidenza della " + str(k) + " riga è ", sum)


#funzione che calcola per ogni g i possibili valori del prodotto scalare,
#prendendone il massimo e stampando l'indice g relativo a questo massimo
def keyCrack(y, m, p):
    arr = np.zeros(26)
    for i in y:
        for j in range(65, 91):#range di codici ASCII per le lettere A-Z
            if i == chr(j):
                 arr[j-65] += 1
                 break
    max_arr = []
    for g in range(26):
        sum = 0
        for i in range(26):
            sum += (p[i]*arr[(g+i) % 26])/len(y)
        max_arr.append(sum)
    maximum = max(max_arr)
    print("il massimo prodotto scalare relativo a questa riga è ", maximum)
    print("l' indice g relativo a questo valore massimo è ", max_arr.index(maximum))
    return max_arr.index(maximum)


p = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02228, 0.06094, 0.06966,
     0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
     0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
f = open(r"VigenereCiphertext.txt")
x = f.read()
f.close()
VigenereCrack(x, 10, p)