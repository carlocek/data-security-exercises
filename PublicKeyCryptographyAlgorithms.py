#IMPLEMENTAZIONE DI ALCUNI ALGORITMI RELATIVI A CRITTOGRAFIA A CHIAVE PUBBLICA


import time
import matplotlib.pyplot as plt
from random import *


#FUNZIONE CHE IMPLEMENTA L'ALGORITMO DI EUCLIDE E RITORNA MCD(a, b)
def euclide(a, b):
    r_tmp0 = a
    r_tmp1 = b
    while True:
        r = r_tmp0 % r_tmp1
        r_tmp0 = r_tmp1
        r_tmp1 = r
        if r == 0:
            break
    return r_tmp0


#FUNZIONE CHE IMPLEMENTA L'ALGORITMO DI EUCLIDE ESTESO E RITORNA MCD(a, b)
#E NEL CASO MCD(a, b)=1 RITORNA ANCHE a**(-1) mod b
def extEuclide(a, b):
    mcd = euclide(a, b)
    if mcd == 1:
        #setto i parametri r0, r1, q1 e le due variabili utili al calcolo dei
        #coefficienti di r1
        r_tmp0 = b
        r_tmp1 = a
        q = r_tmp0 // r_tmp1
        coeff_tmp0 = 1
        coeff_tmp1 = r_tmp0 - q
        #calcolo il resto r2
        r = r_tmp0 % r_tmp1
        while r != 1:
            #aggiorno le variabili relative a quoziente e resti e
            #calcolo ad ogni passo il coefficiente di r1 quando esprimo l'i-esimo resto
            #in funzione di r1
            q = r_tmp1 // r
            coeff_tmp = (coeff_tmp0 - q * coeff_tmp1) % b
            coeff_tmp0 = coeff_tmp1
            coeff_tmp1 = coeff_tmp
            r_tmp0 = r_tmp1
            r_tmp1 = r
            r = r_tmp0 % r_tmp1
        #appena incontro un r == 1 ritorno il coefficiente di r1 del passo precedente
        #cge sarà anche l'inverso moltiplicativo
        return coeff_tmp1
    else:
        return mcd

#TEST
a = 17
b = 60
mcd = extEuclide(a, b)
print("l'output di extEuclide(17, 60) è: ", mcd)


#FUNZIONE CHE IMPLEMENTA L'ALGORITMO DI ESPONENZIAZIONE VELOCE RESITUENDO a**n mod m
def fastExp(a, n, m):
    #inizializzo la variabile relativa ai prodotti parziali
    d = 1 
    #converto l'esponente n in stringa di bit
    n = bin(n)
    n = n[2:]
    for i in range(len(n)):
        #elevo d al quadrato e se l'i-esimo bit di n è pari a 1 aggiorno
        #il prodotto parziale moltiplicandolo per a
        d = (d**2) % m
        if n[i] == "1":
            d = (d*a) % m
    return d

#TEST
print("l'output di fastExp(3, 11, 10) è: ", fastExp(3, 11, 10))


#FUNZIONE CHE IMPLEMENTA IL TEST DI MILLER-RABIN RESTITUENDO UN VALORE BOOLEANO
def testMillerRabin(n):
    #controllo la parità di n
    if n % 2 == 0:
        return True
    m = n-1
    r = 0
    #determino i parametri m e r
    while n-1 == (2**r)*m and m % 2 == 0:
        m = m // 2
        r += 1
    #esguo 20 test partendo da un x<n generato casualmente ogni volta
    for j in range(20):
        x = randint(1, n-1)
        x_i = fastExp(x, m, n)
        #controllo la condizione su x0
        if x_i != 1 and x_i % n != n-1:
            #genero la successione degli xi, fermandomi se trovo un elemento
            #che non rispetta le ipotesi del test
            for i in range(1, r+1):
                x_i = fastExp(x_i, 2, n)
                if i != r and x_i % n == n-1:
                    break
                #se sono arrivato alla fine della successione senza interrompere,
                #posso concludere che n è composto
                if i == r:
                    return True
    #se il test non ritorna True per 20 volte consecutive,
    #posso concludere che n è primo
    return False

#TEST
print("l'output di testMillerRabin(18251533719285077110439929943761997761965932631283) è : ", testMillerRabin(18251533719285077110439929943761997761965932631283))


#FUNZIONE CHE GENERA UN NUMERO PRIMO LUNGO k CIFRE
def primeGenerator(k):
    b = True
    while b:
        #genero un intero casuale lungo k cifre
        x = randint(10**(k-1), 10**k)
        #applico a x un test di primalità che restituisce False
        #se x è primo, uscendo dal ciclo e ritornando x
        b = testMillerRabin(x)
    return x

#TEST
print("l'output di primeGenerator(100) è: ", primeGenerator(100))


#FUNZIONE CHE IMPLEMENTA L'ENCRYPTION DI RSA
def encryptRSA(m, e, n):
    c = fastExp(m, e, n)
    return int(c)

#FUNZIONE CHE IMPLEMENTA LA DECRYPTION DI RSA
def decryptRSA(c, d, phi_n, n):
    m = fastExp(c, d % phi_n, n)
    return int(m)

#FUNZIONE CHE IMPLEMENTA L'ENCRYPTION DI RSA USANDO IL CRT
def CRTdecryptRSA(c, d, p, q, phi_p, phi_q, pInv, qInv, n):
    m1 = fastExp(c, d % phi_p, p)
    m2 = fastExp(c, d % phi_q, q)
    x = (((m1) * ((q)*(qInv))) + ((m2) * ((p)*(pInv)))) % n
    return x

#FUNZIONE CHE IMPLEMENTA LA DECRYPTION DI RSA USANDO IL CRT
def CRTencryptRSA(m, e, p, q, pInv, qInv, n):
    c1 = fastExp(m, e, p)
    c2 = fastExp(m, e, q)
    x = (((c1) *((q)*(qInv))) + ((c2) * (p)*(pInv))) % n
    return x


#FUNZIONE CHE CONFRONTA LA DECRYPTION DI RSA CON QUELLA DI RSA_CRT SU 100 CIPHERTEXT
#CASUALI E PLOTTA I TEMPI DI ESECUZIONE DEI DUE APPROCCI
def testRSA():
    #genero due primi lunghi k cifre
    p = primeGenerator(100)
    q = primeGenerator(100)
    #calcolo il modulo RSA n
    n = p*q
    #calcolo il numero di coprimi < n
    phi_n = (p-1)*(q-1)
    phi_p = p-1
    phi_q = q-1
    #precomputo i valori utili alla decryption che sfrutta il CRT
    qInv = extEuclide(q, p)
    pInv = extEuclide(p, q)
    #calcolo gli esponenti pubblico e privato
    while True:
        e = randint(2, 20)
        d = extEuclide(e, phi_n)
        if euclide(d, phi_n) == 1:
            break
    #inizializzo le liste dove salverò i tempi di esecuzione dei due approcci
    timeRSA_CRT = []
    timeRSA = []
    x_axis = []
    #per ogni i costruisco l'asse x per il plot, genero un ciphertext casuale e 
    #calcolo i tempi di inizio e fine delle funzioni di decryption RSA e RSA con CRT
    for i in range(100):
        x_axis.append(i)
        c = randint(10**100, 10**101)
        ti_RSA = time.time()
        decryptRSA(c, d, phi_n, n)
        tf_RSA = time.time()
        timeRSA.append(tf_RSA - ti_RSA)
        ti_RSA_CRT = time.time()
        CRTdecryptRSA(c, d, p, q, phi_p, phi_q, pInv, qInv, n)
        tf_RSA_CRT = time.time()
        timeRSA_CRT.append(tf_RSA_CRT - ti_RSA_CRT)
    #plotto i risultati
    plt.plot(x_axis, timeRSA, color="green", label="RSA standard")
    plt.plot(x_axis, timeRSA_CRT, color="blue", label="RSA con CRT")
    plt.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
    plt.xlabel("numero di iterazione")
    plt.ylabel("tempo di esecuzione")
    plt.show()

#TEST
testRSA()
