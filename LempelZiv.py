import string

#FUNZIONE CHE, DATO UN TESTO IN INGRESSO, CREA IL DIZIONARIO DELLE ENTRATE RELATIVO ALLA CODIFICA LEMPEL-ZIV                          
def LZ(text):
    #inizializzo l'offset per lo scorrimento di text
    m = 1
    #inizializzo il numero di riferimento per i blocchi
    ref = 1
    #inizializzo il dizionario contenente i blocchi con i relativi puntatori (ref)
    refblockDiz = {"": 0, text[0]: ref}
    #inizializzo il dizionario contenente le entrate 
    entranceDiz = {"0": text[0]}
    for i in range(2, len(text)+1):
        padding = ""
        #estraggo il primo blocco da text controllando di non averlo gia analizzato
        textTemp = text[m:i]
        if textTemp in refblockDiz:
            continue
        #aggiorno il dizionario dei riferimenti ai blocchi
        ref += 1
        refblockDiz.update({textTemp: ref})
        #gestisco il padding di bit per evitare ambiguità in entranceDiz
        if len(bin(ref-1)[2:]) > len(bin(refblockDiz[textTemp[:-1]])[2:]):
            diff = len(bin(ref-1)[2:]) - len(bin(refblockDiz[textTemp[:-1]])[2:])
            while diff > 0:
                padding += "0"
                diff -= 1
        #aggiorno il dizionario delle entrate e l'offset per scorrere text
        entranceDiz.update({padding + bin(refblockDiz[textTemp[:-1]])[2:]: textTemp[-1]})
        m = i
        
    #gestisco l'ultimo blocco della stringa da codificare nel caso questo sia un blocco già analizzato in precedenza
    if textTemp in refblockDiz:
        padding = ""
        ref += 1
        refblockDiz.update({textTemp: ref})
        if len(bin(ref-1)[2:]) > len(bin(refblockDiz[textTemp[:-1]])[2:]):
            diff = len(bin(ref-1)[2:]) - len(bin(refblockDiz[textTemp[:-1]])[2:])
            while diff > 0:
                padding += "0"
                diff -= 1
        entranceDiz.update({padding + bin(refblockDiz[textTemp[:-1]])[2:]: textTemp[-1]})
    print("il dizionario relativo ai riferimenti è: ", refblockDiz)
    print("il dizionario relativo alle entrate è: ", entranceDiz)
    return entranceDiz

#FUNZIONE CHE CODIFICA text CON LZ USANDO IL DIZ DELLE ENTRATE GENERATO DA LZ() ED UN DIZIOANRIO
#CHE ASSOCIA AD OGNI LETTERA UN SIMBOLO DI DEFAULT
def LZCode(text, entranceDiz, defaultDiz):
    #inizializzo la stringa che conterrà il testo codificato
    encodedtext = ""
    #scorro il dizionario delle entrate aggiungendo a encodedtext ad ogni passo, oltre al codice dell'entrata,
    #il simbolo associato all'ultima lettera del blocco che sto codificando
    for i in entranceDiz.keys():
        encodedtext += (i + defaultDiz[entranceDiz[i]])
    print("il testo codifiicato con lempel-ziv è: ", encodedtext)
    return encodedtext

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

#FUNZIONE CHE FORMATTA IL TESTO IN MAIUSCOLO ELIMINANDO SPAZI E PUNTEGGIATURA
def textFormatting(text):
    for i in string.punctuation:
        text = text.replace(i, "")
    text = text.replace("—", "")
    text = text.replace("’", "")
    text = text.replace(" ", "")
    text = text.upper()
    #print(text)
    return text

#FUNZIONE CHE ESEGUE IL CONFRONTO TRA LE PERCENTUALI DI COMPRESSIONE DI HUFFMAN E LEMPEL-ZIV
def comparison(text, defaultDiz, alphabet, prob):
    #formatto il testo in maiuscolo eliminando spazi e punteggiatura
    text = textFormatting(text)
    textBlocks = []
    compressionPercH = []
    compressionPercLZ = []
    n = 10
    m = len(text)//n
    code = Huffman(alphabet, prob)
    #divido text in n blocchi e li salvo in textBlocks
    for i in range(n):
        textBlocks.append(text[i*m: (i+1)*m])
    #per ogni blocco genero il codice corrispondente con i due metodi e salvo la percentuale di compressione
    #per Huffman e Lempel-Ziv rispettivamente in compressionPercH e compressionPercLZ
    for b in textBlocks:
        #calcolo compressione per Huffman
        encodedH = HuffmanCode(b, code)
        percH = ((5*len(b) - len(encodedH)) / (5*len(b))) * 100
        compressionPercH.append(percH)
        #calcolo compressione per Lempel-Ziv
        entranceDiz = LZ(b)
        encodedLZ = LZCode(b, entranceDiz, defaultDiz)
        percLZ = ((5*len(b) - len(encodedLZ)) / (5*len(b))) * 100
        compressionPercLZ.append(percLZ)
    #calcolo la media delle due liste contenenti le percentuali di compressione per singoli blocchi
    meancompressionH = (sum(compressionPercH)) / n
    meancompressionLZ = (sum(compressionPercLZ)) / n
    print("la percentuale di compressione media usando Huffman è: ", meancompressionH)
    print("la percentuale di compressione media usando LZ è: ", meancompressionLZ)

#FUNZIONE DI TEST
def test():
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    prob = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02228, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
    defaultDiz = {"A": "0", "B": "1", "C": "11", "D": "100", "E": "101", "F": "110", "G": "111", "H": "1000", "I": "1001", "J": "1010", "K": "1011", "L": "1100", "M": "1101", "N": "1110", "O": "1111", "P": "10000", "Q": "10001", "R": "10010", "S": "10011", "T": "10100", "U": "10101", "V": "10110", "W": "10111", "X": "11000", "Y": "11001", "Z": "11010"}
    text1 = "AABABBBABAABABBBABBABB"
    #testo la funzione di codifica su text1
    entranceDiz = LZ(text1)
    LZCode(text1, entranceDiz, defaultDiz)
    f = open(r"dummytext.txt")
    text2 = f.read()
    f.close()
    #metto a confronto la codifica LZ con quella di Huffman su 10 blocchi estratti da text2
    print("\nINIZIO FASE DI COMPARAZIONE\n")
    comparison(text2, defaultDiz, alphabet, prob)
    
test()