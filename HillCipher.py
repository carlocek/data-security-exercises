#ISTRUZIONI:
#chiamare la funzione HillEncrypt() passando il testo da cifrare, la lunghezza dei blocchi e la chiave K sotto forma di matrice 
#per ottenere la matrice relativa al ciphertext
#chiamare la funzione HillDecrypt() passando le matrici relative a ciphertext e chiave per ottenere la matrice del plaintext corrispondente
#chiamare la funzione HillAttack() passando una coppia (plaintext, ciphertext) e la lunghezza dei blocchi m
#per calcolare la matrice relativa alla chiave


import math
import numpy as np
from sympy import Matrix
import string

#FUNZIONE CHE FORMATTA E RESTITUISCE IL TESTO IN MAIUSCOLO E SENZA PUNTEGGIATURA
def TextFormatting(text):
    for i in string.punctuation:
        text = text.replace(i, "")
    text = text.replace(" ", "")
    text = text.upper()
    return text

#FUNZIONE PER CIFRARE TRAMITE IL CIFRARIO DI HILL
def HillEncrypt(text, m, K):
    text = TextFormatting(text)
    #creo una lista che avrà come elementi i blocchi di m lettere di text
    gramText = []
    #ciclo per fare padding su text nel caso in cui m non divida la len(text)
    while len(text) % m != 0:
        text += " "
    n = int(len(text) / m) #numero di m-grammi in text
    for i in range(n):
        gramText.append(text[i*m: (i+1)*m])
    #inizializzo una matrice m x n in cui le colonne saranno i singoli m-grammi (tradotti in numeri)
    PMat = np.zeros((m, n))
    for i in range(n):
        #salvo in P l'i-esimo blocco che sarà poi la i-esima colonna di PMat
        P = np.array(list(gramText[i]))
        for j in range(m):
            PMat[j, i] = ord(P[j]) - 65 #ord(x) rende il codice ASCII corrispondente al carattere x, che andrà shiftato indietro di 65 (che è il codice ASCII del carattere A)
    #risolvo il sistema lineare per la cifratura definito dal cifrario di Hill
    C = np.dot(K, PMat)
    C = C % 26
    print("la matrice PMat ottenuta dall formattazione del plaintext è ", PMat)
    print("la matrice relativa al testo cifrato è ", C)
    print("\n")
    return C

#FUNZIONE PER DECIFRARE TRAMITE IL CIFRARIO DI HILL
def HillDecrypt(C, K):
    symK = Matrix(K)
    #uso un metodo della classe Matrix di sympy per calcolare l'inversa di una matrice mod 26
    symInvK = symK.inv_mod(26)
    #ritorno al tipo di partenza (numpy.array)
    invK = np.array(symInvK)
    print("l'inversa di K usata per decifrare è ", invK)
    #risolvo il sistema lineare per la decifratura definito dal cifrario di Hill
    PMat = np.dot(invK, C) 
    PMat = PMat % 26
    print("la matrice relativa al testo decifrato è ", PMat)

#FUNZIONE PER ESEGUIRE UN ATTACCO KNOWN PLAINTEXT AL CIFRARIO DI HILL
def HillAttack(ptext, ctext, m):
    ptext = TextFormatting(ptext)
    ctext = TextFormatting(ctext)
    #creo le liste che avranno come elementi i blocchi di m lettere di ptext e ctext
    gramPText = []
    gramCText = []
    #ciclo per fare padding su ptext e ctext nel caso in cui m non divida la loro lunghezza
    while len(ptext) % m != 0:
        ptext += " "
        ctext += " "
    n = int(len(ptext) / m) #lunghezza di ptext e ctext in blocchi
    for i in range(n):
        gramPText.append(ptext[i*m: (i+1)*m])
        gramCText.append(ctext[i*m: (i+1)*m])
    #inizializzo le matrici m x n in cui le colonne saranno i singoli m-grammi (tradotti in numeri)
    PMat = np.zeros((m, n))
    CMat = np.zeros((m, n))
    for i in range(n):
        #salvo in P e C l'i-esimi blocchi che saranno poi le i-esime colonne di PMat e CMat
        P = np.array(list(gramPText[i]))
        C = np.array(list(gramCText[i]))
        for j in range(m):
            PMat[j, i] = ord(P[j]) - 65
            CMat[j, i] = ord(C[j]) - 65
    #costruisco la matrice PStar quadrata a partire da PMat fermandomi appena ne trovo una invertibile
    notInvertible = True
    for i in range(n + 1 - m):
        PStar = PMat[:, i: i + m]
        CStar = CMat[:, i: i + m]
        if math.gcd(int(np.linalg.det(PStar)) % 26, 26) == 1:
            notInvertible = False
            break
    if notInvertible:
        print("non ho trovato matrici quadrate invertibili")
        exit()
    PStar = PStar.astype(int)
    symPStar = Matrix(PStar)
    #uso un metodo della classe Matrix di sympy per calcolare l'inversa di una matrice mod 26
    symInvPStar = symPStar.inv_mod(26)
    invPStar = np.array(symInvPStar)
    print(invPStar)
    #risolvo il sistema lineare per ricavare la matrice della chiave K
    K = np.dot(CStar, invPStar)
    K = K % 26
    print("la matrice della chiave ottenta dall'attacco è ", K)


#DEFINIZIONE PARAMETRI DA PASSARE ALLE FUNZIONI
m = 2
text = "friday"
K = np.array([[7, 8], [19, 3]])
ptext = "friday"
ctext = "pqcfku"

C = HillEncrypt(text, m, K)
HillDecrypt(C, K)
HillAttack(ptext, ctext, m)