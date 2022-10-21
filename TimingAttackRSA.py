#ESECUZIONE DI UN TIMING ATTACK AL PROTOCOLLO RSA

#TEMPO DI ESECUZIONE STIMATO: 1:30 MIN

from TimingAttackModule import *
from random import *

#SETTAGGIO PARAMETRI
N = 2000 #numero di iterazioni per calcolare le varianze dei due casi da confrontare
ta = TimingAttack()

#FUNZIONE CHE ESEGUE UN TIMING ATTACK DETERMINANDO L'ESPONENTE SEGRETO d
def timingAtt(ta, N):
    #inizializzo la lista in cui salverò i bit dell'esponente segreto scoperti ad ogni iterazione del ciclo esterno
    d_prime = [1]
    for i in range(1, 64):
        #inizializzo le variabili utili al calcolo delle varianze nei due casi a confronto
        sum0 = 0
        sum0_square = 0
        sum1 = 0
        sum1_square = 0
        d_prime.append(0)
        for j in range (N):
            c = randint(10**100, 10**101)
            #misuro il tempo di esecuzione dell'algoritmo fastExp sulla macchina sotto attacco
            t_vic = ta.victimdevice(c)
            #setto l'i-esimo bit della mia lista a 0 e misuro il tempo di esecuzione dell'algoritmo fastExp
            #sulla macchina dell'attaccante fino all'i-esima iterazione
            d_prime[i] = 0
            t_att0 = ta.attackerdevice(c, d_prime)
            #setto l'i-esimo bit della mia lista a 1 e misuro il tempo di esecuzione dell'algoritmo fastExp
            #sulla macchina dell'attaccante fino all'i-esima iterazione
            d_prime[i] = 1
            t_att1 = ta.attackerdevice(c, d_prime)
            #calcolo le sommatorie presenti nella formula della varianza per la differenza tra i tempi T e T'
            sum0_square = sum0_square + (t_vic-t_att0)**2
            sum0 = sum0 + (t_vic - t_att0)
            sum1_square = sum1_square + (t_vic-t_att1)**2
            sum1 = sum1 + (t_vic - t_att1)
        #calcolo le varianze relative ai casi i-esimo bit di d_prime pari a 0 o ad 1 e setto il bit a seconda di 
        #quale varianza è minore rispetto all'altra
        var0 = sum0_square/(N) - ((sum0/(N))**2)
        var1 = sum1_square/(N) - ((sum1/(N))**2)
        if var0 < var1:
            d_prime[i] = 0
        else:
            d_prime[i] = 1
    ta.test(d_prime)
    print(d_prime)
    
timingAtt(ta, N)