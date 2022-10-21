#PROGRAMMA CHE DATO IN INGRESSO UN TESTO E LA LUNGHEZZA M DEI BLOCCHI CALCOLA:
#ISTOGRAMMA DELLA FREQUENZA DELLE 26 LETERE,
#DISTRIBUZIONE EMPIRICA DEGLI M GRAMMI,
#INDICE DI COINCIDENZA ED ENTROPIA DELLA DISTIBUZIONE DEGLI M GRAMMI
#per calcolare le quantità descritte, chiamare la funzione TextAnalysis(text, m) 
#passando il testo da analizzare ed il parametro che definisce la dimensione dei blocchi

import matplotlib.pyplot as plt
import numpy as np
import math
import string

#FUNZIONE PRINCIPALE
def TextAnalysis(text, m):
    text = TextFormatting(text)
    LettersHistogram(text)
    TextGramAnalysis(text, m)

#FUNZIONE CHE FORMATTA E RESTITUISCE IL TESTO IN MAIUSCOLO E SENZA PUNTEGGIATURA
def TextFormatting(text):
    for i in string.punctuation:
        text = text.replace(i, "")
    text = text.replace("—", "")
    text = text.replace("’", "")
    text = text.replace(" ", "")
    text = text.upper()
    return text

#FUNZIONE CHE PLOTTA L'ISTOGRAMMA DELLE FREQUENZE DELLE LETTERE NEL TESTO
def LettersHistogram(text):
    n = len(text)
    # inizializzo un array che memorizza il numero di occorrenze di ogni lettera in text
    occ = np.zeros(26)
    for i in text:
        for j in range(65, 91): #range di codici ASCII per le lettere A-Z maiuscole
            if i == chr(j): #chr() restituisce il carattere relativo al codice ASCII j
                 occ[j-65] += 1
                 break
    freq = occ/n
    plt.bar(range(26), freq)
    plt.show()
    print("\n")

#FUNZIONE CHE DIVIDE IL TESTO IN BLOCCHI DI M LETTERE E CALCOLA 
#DISTRIBUZIONE EMPIRICA DEGLI M-GRAMMI CON RELATIVA ENTROPIA ED INDICE DI COINCIDENZA
def TextGramAnalysis(text, m):
    #creo una lista in cui ogni elemento sarà un blocco di m lettere del testo
    mGram = []
    #ciclo che introduce spazi di padding quando la lunghezza del testo non è divisibile per m
    while len(text) % m != 0:
        text += " "
    n = int(len(text) / m) #n rappresenta il numero di blocchi di m lettere
    print("il numero di blocchi di " + str(m) + " lettere è", n)
    for i in range(n):
        mGram.append(text[i*m: (i+1)*m])
    print("il testo diviso in blocchi è ", mGram)
    q = EmpyricalDist(mGram, m, n)
    Entropy(q)
    IndexCoincidence(q, n)

#FUNZIONE CHE CALCOLA E RESTITUISCE LA DISTRIBUZIONE EMPIRICA DEGLI M GRAMMI IN text
def EmpyricalDist(mGram, m, n):
    #creo una lista che memorizza le occorrenze di ogni blocco di m lettere in text
    occ = []
    #creo una lista che memorizza tutti i blocchi di m lettere diversi in text
    minorGram = []
    #count conta le volte in cui incontro un blocco già contato per indicizzare correttamente il vettore delle occorrenze
    count = 0
    for i, x in enumerate(mGram):
        # definisco una var booleana che dice se abbiamo già contato uno specifico blocco oppure no
        isNewGram = True
        for j in range(i):
            if mGram[j] == x and i != 0:
                isNewGram = False
                count += 1
                break
        if isNewGram:
            occ.append(0)
            minorGram.append(x)
            for y in mGram[i:]:
                if x == y:
                    occ[i-count] += 1
    print("la lunghezza del vettore che calcola le occorrenze degli m-grammi in text è ", len(occ))
    q = []
    for i in range(len(occ)):
        q.append(occ[i]/n)
    print("la distribuzione empirica degli m-grammi in text è ", q)
    print("\n")
    return q

#FUNZIONE CHE CALCOLA L'ENTROPIA DELLA DISTRIBUZIONE EMPIRICA RELATIVA AD UN BLOCCO
def Entropy(q):
    sum = 0
    for i in range(len(q)):
        #controllo necessario per applicare il logaritmo della formula
        if q[i] != 0:
            sum += q[i] * math.log10(q[i])
    sum = -sum
    print("l'entropia della distribuzione empirica degli m grammi è ", sum)
    print("\n")

#FUNZIONE CHE CALCOLA L'INDICE DI COINCIDENZA DI UN BLOCCO x
def IndexCoincidence(q, n):
    #creo una lista che conta il numero di occorrenze di ogni elemento di q (distr empirica)
    occ = []
    count = 0
    for i, x in enumerate(q):
        isNewElement = True
        for j in range(i):
            if q[j] == x and i != 0:
                isNewElement = False
                count += 1
                break
        if isNewElement:
            occ.append(0)
            for y in q[i:]:
                if x == y:
                    occ[i-count] += 1
    sum = 0
    for i in range(len(occ)):
        sum += (occ[i]*(occ[i]-1))/(n*(n-1))
    print("l' indice di coincidenza della distribuzione empirica degli m-grammi è ", sum)


f = open(r"MobyDickFirstChapter.txt")
text = f.read()
f.close()
TextAnalysis(text, 4)