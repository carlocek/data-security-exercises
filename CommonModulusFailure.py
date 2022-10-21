#CODICE CHE MOSTRA L'ATTACCO COMMON MODULUS FAILURE AL PROTOCOLLO RSA:
#Un utente A possiede due coppie di chiavi pubbliche-private RSA, relative allo stesso modulo n
#Un secondo utente invia ad A, in tempi diversi, lo stesso messaggio m, cifrato prima con la chiave e1 e poi con la chiave 12.
#Un attaccante intercetta i relativi plaintext c1 e c2. Si ricava m a partire dalle informazioni disponibili


from modulo import modulo

#SETTAGGIO PARAMETRI
e1 = 3
e2 = 11
c1 = 41545998005971238876458051627852835754086854813200489396433
c2 = 88414116534670744329474491095339301121066308755769402836577
n = 825500608838866132701444300844117841826444264266030066831623

#FUNZIONE CHE IMPLEMENTA L'ATTACCO COMMON MODULUS FAILURE
def cmf(e1, e2, c1, c2, n):
    x = int(modulo(e1, e2)**(-1))
    y = int((1 - e1 * x) / e2)
    #modulo(a, b)**i calcola a**i mod b ammettendo anche esponenti negativi
    m = (modulo(c1, n)**x) * (modulo(c2, n)**y)
    return int(m)

#TEST
m = cmf(e1, e2, c1, c2, n)
print("il plaintext ricavato e': ", m)

c1_test = int(modulo(m, n)**3) 
print(c1_test == c1)