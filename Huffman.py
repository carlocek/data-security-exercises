#FUNZIONE CHE GENERA UN CODICE DI Huffman RELATIVO AD alphabet
def Huffman(alphabet, prob):
    #creo la lista che conterrà, in posizione i, i due elementi uniti nel i-esimo passo della fase 1 dell'algoritmo
    mergeOrder = []
    #creo il dizionario in cui salverò le associazioni simboli-codice
    code = {}

    #inizio fase 1 dell'algoritmo
    while len(prob) != 1:
        #salvo l'indice relativo alla probabilità minore del vettore prob
        min1 = prob.index(min(prob))
        #salvo l'elemento di prob con valore minore e lo rimuovo da prob
        probmin1 = prob.pop(min1)
        #salvo l'elemento di alphabet con probabilità minore e lo rimuovo da alphabet    
        alphabetmin1 = alphabet.pop(min1)
        #salvo l'indice relativo alla seconda probabilità minore del vettore prob
        min2 = prob.index(min(prob))
        #aggiorno il vettore prob, sostituendo nella posizione relativa al secondo elemento minore
        #la somma delle due probabilità minori dell'iterazione corrente
        prob[min2] = probmin1 + prob[min2]
        #salvo in mergeOrder i due elementi di alphabet che ho appena unito
        mergeOrder.append([alphabet[min2], alphabetmin1])
        #aggiorno alphabet sostituendo nella posizione relativa al secondo elemento con probabilità minore
        #una lista contenente i due elementi che ho unito
        alphabet[min2] = [alphabet[min2], alphabetmin1]

    #inizio fase 2 dell'algoritmo
    #salvo e rimuovo l'ultimo elemento di mergeOrder, che conterrà i due elementi che
    #ho unito nell'ultima iterazione della fase 1
    lastMerged = mergeOrder.pop(len(mergeOrder)-1)
    #inizializzo il dizionario assegnando ai due elementi che ho unito nell'ultima
    #iterazione della fase 1 i codici 0 ed 1
    code.update({str(lastMerged[0]): "0", str(lastMerged[1]): "1"})
    while len(mergeOrder) > 0:
        lastMerged = mergeOrder.pop(len(mergeOrder)-1)
        #salvo in codeword il codice, all'interno del dizionario, relativo alla chiave
        #rappresentante l'elemento che devo "scoppiare" nella corrente iterazione
        codeword = code[str(lastMerged)]
        #rimuovo questo elemento dal dizionario per rimpiazzarlo con due elementi aventi
        #chiavi rappresentanti le componenti della chiave rimossa e valori rispettivamente pari al codice
        #relativo alla chiave rimossa, con l'aggiunta in coda di 0 e 1
        code.pop(str(lastMerged))
        code.update({str(lastMerged[0]): codeword + "0", str(lastMerged[1]): codeword + "1"})
    print("il codice rappresentato in forma di dizionario è: \n", code)
    return code

#FUNZIONE CHE CODIFICA TEXT USANDO IL CODICE HUFFMAN GENERATO DA Huffman()
def HuffmanCode(text, code):
    encodedtext = ""
    for l in text:
        encodedtext += code[l]
    print("il testo codificato con huffman è: ", encodedtext)
    return encodedtext


#FUNZIONE CHE PRENDE IN INGERSSO UN CODICE ED UNA STRINGA BINARIA E LA DECODIFICA
def Decode(code, binstr):
    #inizializzo l'indice che rappresenta l'inizio della porzione di binstr che analizzo
    #ad ogni iterazione
    m = 0
    #creo la lista in cui salverò i simboli decodificati
    text = []
    for i in range(1, len(binstr)+1):
        #salvo la porzione di binstr da analizzare
        tempstr = binstr[m:i]
        #scorro il dizionario relativo al codice finchè non trovo un valore uguale alla porzione
        #di binstr che sto analizzando, a quel punto appendo a text la chiave corrispondente e
        #aggiorno l'offset di partenza per analizzare le successive porzioni di binstr
        for e in code:
            if tempstr == code[e]:
                text.append(e)
                m = i
                break
    print("la codifica della stringa di bit è: ", text)



#FUNZIONE TEST
def test():
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    prob = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02228, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
    binstr = "011001000"
    code = Huffman(alphabet, prob)
    Decode(code, binstr)
    text = "CACCE"
    HuffmanCode(text, code)

test()