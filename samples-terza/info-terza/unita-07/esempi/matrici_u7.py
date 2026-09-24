"""Matrici rettangolari come liste di liste dell'Unità 7.

Collocare il file in `programmi/matrici_u7.py` della raccolta dello
studente. Una matrice è rappresentata da una lista i cui elementi sono a
loro volta liste: la lista esterna contiene le RIGHE, ogni riga contiene le
proprie colonne. La matrice si dice rettangolare quando tutte le righe
hanno la stessa lunghezza: è la precondizione di questo modulo.

Il punto delicato è l'alias delle righe. L'espressione
`[[valore] * colonne] * righe` produce una lista di righe che sono lo
STESSO oggetto ripetuto: una scrittura su una cella appare in ogni riga.
Le funzioni qui sotto costruiscono invece righe indipendenti.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/matrici_u7.py
"""


def costruisci_matrice(righe: int, colonne: int, valore: int = 0) -> list[list[int]]:
    """Restituisce una matrice `righe` x `colonne` di righe INDIPENDENTI, riempite con `valore`.

    Riceve il numero di `righe`, il numero di `colonne` e il `valore` da
    scrivere in ogni cella, 0 se omesso. Restituisce una matrice nuova in
    cui ogni riga è una lista propria: una scrittura su una cella non si
    ripercuote sulle altre righe. Nessun argomento viene modificato.
    Con `righe` uguale a 0 il risultato è `[]`; con `colonne` uguale a 0 e
    `righe` positivo il risultato è una matrice di righe vuote.

    ERRATO: `[[valore] * colonne] * righe`. La ripetizione esterna copia il
    RIFERIMENTO alla stessa riga: la matrice risultante ha righe aliase e
    `matrice[0][0] = 99` modifica tutte le righe contemporaneamente. La
    ripetizione interna `[valore] * colonne` è invece sicura, perché gli
    interi sono immutabili e ogni riga viene creata dalla comprensione.
    """
    return [[valore for _ in range(colonne)] for _ in range(righe)]


def dimensioni(matrice: list[list[int]]) -> tuple[int, int]:
    """Restituisce `(righe, colonne)` della matrice rettangolare ricevuta.

    Riceve la `matrice` e restituisce la tupla con il numero di righe e il
    numero di colonne, dedotto dalla lunghezza della prima riga. L'argomento
    non viene modificato. Per matrice vuota il risultato è `(0, 0)`, perché
    non esiste alcuna riga da cui dedurre le colonne.

    PRECONDIZIONE: tutte le righe hanno la stessa lunghezza. Se le righe
    differiscono la matrice non è rettangolare, il risultato descrive solo
    la prima riga e il comportamento delle altre funzioni del modulo è
    fuori contratto: il controllo della rettangolarità appartiene al
    problema che usa la matrice.
    """
    if not matrice:
        return (0, 0)
    return (len(matrice), len(matrice[0]))


def valore(matrice: list[list[int]], i: int, j: int) -> int:
    """Restituisce il contenuto della cella (`i`, `j`) della `matrice`.

    Riceve la `matrice` e gli indici di riga `i` e di colonna `j`. Non
    modifica l'argomento: si limita a leggere. Per matrice vuota, oppure
    con indici fuori intervallo, la chiamata non è applicabile e produce
    `IndexError`: la validazione degli indici è parte della consegna quando
    il problema la richiede.
    """
    return matrice[i][j]


def assegna(matrice: list[list[int]], i: int, j: int, valore: int) -> None:
    """Scrive `valore` nella cella (`i`, `j`) della `matrice` e non restituisce nulla.

    Riceve la `matrice`, gli indici `i` e `j` e il `valore` da scrivere.
    MODIFICA in loco la riga `i`, quindi la matrice intera: chi chiama
    osserva il cambiamento. Il risultato è `None`. Per matrice vuota o
    indici fuori intervallo la chiamata produce `IndexError`, come per la
    lettura.
    """
    matrice[i][j] = valore


def somma_riga(matrice: list[list[int]], i: int) -> int:
    """Restituisce la somma degli elementi della riga `i` della `matrice`.

    Riceve la `matrice` e l'indice di riga `i`. Scorre la riga con un ciclo
    esplicito e ne somma gli elementi. Non modifica l'argomento. Per riga
    vuota il risultato è 0, il neutro dell'addizione; per indice fuori
    intervallo la chiamata produce `IndexError`.
    """
    somma = 0
    for elemento in matrice[i]:
        somma += elemento
    return somma


def somma_colonna(matrice: list[list[int]], j: int) -> int:
    """Restituisce la somma degli elementi della colonna `j` della `matrice`.

    Riceve la `matrice` e l'indice di colonna `j`. Scorre le righe con un
    ciclo esplicito e somma l'elemento in posizione `j` di ciascuna.
    Non modifica l'argomento. Per matrice vuota il risultato è 0; per
    colonna inesistente la chiamata produce `IndexError`.
    """
    somma = 0
    for riga in matrice:
        somma += riga[j]
    return somma


def somme_per_riga(matrice: list[list[int]]) -> list[int]:
    """Restituisce l'elenco delle somme, una per ogni riga della `matrice`.

    Riceve la `matrice` e costruisce una lista NUOVA con la somma di ogni
    riga, nello stesso ordine delle righe. Non modifica l'argomento.
    Per matrice vuota il risultato è `[]`; per matrice con righe vuote
    (`colonne` uguale a 0) la lista contiene uno 0 per ogni riga.

    Il risultato è una lista semplice di interi e non una matrice: una
    somma per riga è un vettore di lunghezza pari al numero di righe.
    """
    somme = []
    for indice in range(len(matrice)):
        somme.append(somma_riga(matrice, indice))
    return somme


def somme_per_colonna(matrice: list[list[int]]) -> list[int]:
    """Restituisce l'elenco delle somme, una per ogni colonna della `matrice`.

    Riceve la `matrice` rettangolare e costruisce una lista NUOVA con la
    somma di ogni colonna, nell'ordine delle colonne. Non modifica
    l'argomento. Per matrice vuota il risultato è `[]`; per matrice con
    righe vuote il risultato è `[]`, perché non ci sono colonne.

    La lunghezza del risultato è pari al numero di colonne, non a quello
    delle righe: è la distinzione da controllare quando si confrontano le
    due funzioni.
    """
    _, colonne = dimensioni(matrice)
    somme = []
    for j in range(colonne):
        somme.append(somma_colonna(matrice, j))
    return somme


def trasponi(matrice: list[list[int]]) -> list[list[int]]:
    """Restituisce la trasposta della `matrice`, in una struttura nuova e indipendente.

    Riceve la `matrice` e ne costruisce la trasposta: la colonna `j`
    dell'originale diventa la riga `j` del risultato, quindi una matrice
    `righe` x `colonne` dà una matrice `colonne` x `righe`. Le righe del
    risultato sono liste nuove e indipendenti: una scrittura sul risultato
    non si ripercuote sull'argomento, che non viene modificato.
    Per matrice vuota il risultato è `[]`; per matrice di una sola riga il
    risultato è una matrice di una sola colonna.
    """
    righe, colonne = dimensioni(matrice)
    return [[matrice[i][j] for i in range(righe)] for j in range(colonne)]


def trasponi_esplicita(matrice: list[list[int]]) -> list[list[int]]:
    """Stesso risultato di `trasponi`, con due cicli annidati pienamente visibili.

    Riceve la `matrice` e costruisce la trasposta percorrendo le colonne
    dell'originale in senso esterno e le righe in senso interno: per ogni
    colonna si prepara una lista nuova e vi si scrivono gli elementi presi
    dalle righe. L'argomento non viene modificato e ogni riga del risultato
    è un oggetto proprio. Per matrice vuota il risultato è `[]`.

    La versione esplicita precede la forma compatta: mostra che la
    trasposizione è uno scambio del ruolo degli indici e non un'operazione
    già pronta del linguaggio.
    """
    righe, colonne = dimensioni(matrice)
    trasposta = []
    for j in range(colonne):
        nuova_riga = []
        for i in range(righe):
            nuova_riga.append(matrice[i][j])
        trasposta.append(nuova_riga)
    return trasposta


def matrice_da_righe(righe: list[list[int]]) -> list[list[int]]:
    """Restituisce una matrice nuova le cui righe sono copie INDIPENDENTI di quelle ricevute.

    Riceve l'elenco delle `righe` e costruisce una lista esterna nuova con
    una lista nuova per ogni riga: nessuna riga del risultato è condivisa
    con l'argomento. Non modifica l'argomento. Per elenco vuoto il
    risultato è `[]`; le righe di lunghezze diverse sono rispettate, senza
    imporre la rettangolarità.

    È la difesa da usare quando una matrice arriva da un'altra funzione e
    non si sa se le sue righe siano già indipendenti.
    """
    copia = []
    for riga in righe:
        nuova_riga = []
        for elemento in riga:
            nuova_riga.append(elemento)
        copia.append(nuova_riga)
    return copia


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: le funzioni sopra restituiscono
    # e non scrivono nulla.
    print("1) La trappola delle righe condivise")
    trappola = [[0] * 3] * 2
    print("trappola [[0] * 3] * 2 :", trappola, "-> righe aliase:", trappola[0] is trappola[1])
    trappola[0][0] = 99
    print("dopo trappola[0][0] = 99:", trappola, "-> cambiano TUTTE le righe")

    print()
    print("2) Righe indipendenti")
    corretta = costruisci_matrice(2, 3, 0)
    print("costruisci_matrice(2, 3):", corretta, "-> righe aliase:", corretta[0] is corretta[1])
    corretta[0][0] = 99
    print("dopo corretta[0][0] = 99:", corretta, "-> cambia SOLO la prima riga")

    print()
    print("3) Dimensioni, lettura e scrittura")
    matrice = [[2, 4], [6, 8], [10, 12]]
    print("matrice        :", matrice)
    print("dimensioni     :", dimensioni(matrice), "-> (righe, colonne)")
    print("valore(1, 0)   :", valore(matrice, 1, 0))
    assegna(matrice, 1, 0, 60)
    print("assegna(1,0,60):", matrice, "-> restituisce None")

    print()
    print("4) Somme per riga e per colonna")
    matrice = [[2, 4], [6, 8], [10, 12]]
    print("matrice           :", matrice)
    print("somma_riga(0)     :", somma_riga(matrice, 0))
    print("somma_colonna(0)  :", somma_colonna(matrice, 0))
    print("somme_per_riga    :", somme_per_riga(matrice))
    print("somme_per_colonna :", somme_per_colonna(matrice))
    print("matrice vuota     :", somme_per_riga([]), somme_per_colonna([]))

    print()
    print("5) Trasposizione 3x2 -> 2x3")
    matrice = [[2, 4], [6, 8], [10, 12]]
    trasposta = trasponi(matrice)
    print("matrice   :", matrice)
    print("trasposta :", trasposta, "-> dimensioni", dimensioni(trasposta))
    print("trasposta esplicita:", trasponi_esplicita(matrice))
    print("matrice invariata  :", matrice)
    trasposta[0][0] = 777
    print("dopo trasposta[0][0] = 777:", trasposta)
    print("la matrice di partenza resta invariata:", matrice)

    print()
    print("6) Copia difensiva delle righe")
    esterna = [[1, 2], [3, 4]]
    difesa = matrice_da_righe(esterna)
    difesa[0][0] = 555
    print("difesa    :", difesa)
    print("esterna   :", esterna, "-> righe non condivise:", difesa[0] is not esterna[0])
