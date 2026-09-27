"""Ordinamenti elementari dell'Unità 10: insertion, selection e due bubble.

Tutte le funzioni seguono lo **stesso contratto didattico** del capitolo PY-14:
ricevono una `list` di valori confrontabili, la ordinano **sul posto** in ordine
non decrescente e restituiscono `None`. Non producono una lista nuova: per
ottenerla serve una copia esplicita dell'argomento prima della chiamata.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.

Vocabolario dei conteggi usato dal capitolo e dal laboratorio:

- **confronto fra chiavi**: valutazione di `>`, `<` o `==` fra due chiavi;
- **scambio**: interversione di due posizioni della lista;
- **spostamento**: assegnamento che trasla di una posizione un elemento
  durante l'inserimento (insertion sort).

Il numero di confronti e il numero di scambi sono grandezze diverse, e nessuna
delle due è una durata.
"""


def insertion_sort(valori):
    """Ordina `valori` sul posto con l'inserimento diretto; restituisce `None`.

    Invariante: dopo l'iterazione `i`, il prefisso `valori[0:i+1]` è ordinato e
    contiene gli stessi elementi che erano in `valori[0:i+1]` all'inizio. Ad
    ogni passo si salva la **chiave** `valori[i]`, si spostano a destra soltanto
    gli elementi **strettamente maggiori** della chiave e si scrive la chiave
    nella posizione liberata.

    Perché è stabile: l'uguaglianza non soddisfa `>` e quindi non provoca
    alcuno spostamento; un elemento uguale alla chiave resta dove si trova.

    Confronti fra chiavi: n-1 per n ≥ 1 se la lista è già ordinata,
    n(n-1)/2 se la lista è ordinata al contrario. Spazio ausiliario
    1: servono solo `chiave` e `posizione`.
    """
    for indice in range(1, len(valori)):
        chiave = valori[indice]
        posizione = indice - 1
        while posizione >= 0 and valori[posizione] > chiave:
            valori[posizione + 1] = valori[posizione]
            posizione -= 1
        valori[posizione + 1] = chiave
    return None


def selection_sort(valori):
    """Ordina `valori` sul posto col minimo del suffisso; restituisce `None`.

    Invariante: dopo l'iterazione `i`, il prefisso `valori[0:i+1]` contiene i
    i+1 valori più piccoli dell'intera lista, nell'ordine con cui sono stati
    selezionati. Ad ogni passo si cerca il minimo del suffisso
    `valori[i:n]` e lo si scambia con la posizione `i` **solo se diverso**.

    Non è stabile nella versione standard: lo scambio sposta lontano anche gli
    elementi uguali che si trovavano fra la posizione corrente e il minimo. Il
    controesempio del capitolo è `[(2, "a"), (2, "b"), (1, "c")]`, confrontato
    sulla prima componente: dopo il primo scambio l'ordine relativo di `2a` e
    `2b` è invertito.

    Confronti fra chiavi: n(n-1)/2 per **ogni** disposizione di n elementi,
    perché il minimo del suffisso si cerca sempre fino in fondo. Scambi: al
    massimo n-1. Spazio ausiliario 1.
    """
    n = len(valori)
    for indice in range(n - 1):
        minimo = indice
        for j in range(indice + 1, n):
            if valori[j] < valori[minimo]:
                minimo = j
        if minimo != indice:
            valori[indice], valori[minimo] = valori[minimo], valori[indice]
    return None


def bubble_sort(valori):
    """Ordina `valori` sul posto con passaggi fissi; restituisce `None`.

    Invariante: dopo la passata p il suffisso `valori[n-1-p:n]` contiene i
    p+1 valori più grandi, nella loro posizione finale. Ad ogni coppia
    adiacente si scambia solo se la chiave di sinistra è **strettamente
    maggiore** di quella di destra: l'uguaglianza non scambia, quindi la
    versione è stabile.

    Il numero delle passate è fissato a n-1 indipendentemente dai dati: anche
    su una lista già ordinata si eseguono n(n-1)/2 confronti fra chiavi, con
    zero scambi. Una sola passata **non** completa l'ordinamento: su
    `[3, 2, 1]` porta `3` in fondo ma lascia `1` prima di `2`.

    Spazio ausiliario 1.
    """
    n = len(valori)
    for passata in range(n - 1):
        for j in range(0, n - 1 - passata):
            if valori[j] > valori[j + 1]:
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
    return None


def bubble_sort_ottimizzato(valori):
    """Come `bubble_sort`, con la zona ridotta e l'arresto; restituisce `None`.

    Due effetti distinti, da non confondere:

    1. la zona esaminata si restringe a ogni passata (`n - 1 - passata`), come
       nella versione semplice, perché il massimo del suffisso è già collocato;
    2. se una passata **non compie alcuno scambio** la lista è già ordinata e
       il ciclo si interrompe: i passaggi residui vengono evitati.

    Sul già ordinato: una sola passata e n-1 confronti fra chiavi per
    n ≥ 1. Sul caso peggiore n(n-1)/2 confronti. La condizione di
    arresto è «nessuno scambio nell'intera passata», non «ultimo scambio in
    posizione zero»: quest'ultima regola, senza altri controlli, può interrompere
    la scansione prima di aver coperto l'intervallo necessario.

    Versione stabile, come la precedente, perché si scambia solo con `>`.
    Spazio ausiliario 1.
    """
    n = len(valori)
    for passata in range(n - 1):
        scambi_avvenuti = False
        for j in range(0, n - 1 - passata):
            if valori[j] > valori[j + 1]:
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi_avvenuti = True
        if not scambi_avvenuti:
            break
    return None


def bubble_sort_ultimo_scambio(valori):
    """Approfondimento: bubble con la zona ridotta all'ultimo scambio.

    Non fa parte del percorso essenziale e si introduce **dopo** che la versione
    base è corretta e testata. Oltre alla zona che si restringe, la fine della
    passata successiva viene portata all'ultima posizione scambiata: gli
    elementi oltre quel punto sono già ordinati e non vengono più esaminati.

    La variante è stabile per lo stesso motivo della versione base. Non è una
    scorciatoia generale: migliora il comportamento su liste quasi ordinate, non
    cambia il caso peggiore n².
    """
    n = len(valori)
    limite = n - 1
    while limite > 0:
        ultimo_scambio = 0
        for j in range(0, limite):
            if valori[j] > valori[j + 1]:
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                ultimo_scambio = j
        limite = ultimo_scambio
    return None


if __name__ == "__main__":
    # Ogni funzione ordina una copia propria: le cinque partono dallo stesso
    # originale e producono tutte [2, 2, 4, 5]. Uscita attesa:
    #   insertion_sort             [5, 2, 4, 2] -> [2, 2, 4, 5]
    #   selection_sort             [5, 2, 4, 2] -> [2, 2, 4, 5]
    #   bubble_sort                [5, 2, 4, 2] -> [2, 2, 4, 5]
    #   bubble_sort_ottimizzato    [5, 2, 4, 2] -> [2, 2, 4, 5]
    #   bubble_sort_ultimo_scambio [5, 2, 4, 2] -> [2, 2, 4, 5]
    originale = [5, 2, 4, 2]
    per_ordinamento = (insertion_sort, selection_sort, bubble_sort,
                       bubble_sort_ottimizzato, bubble_sort_ultimo_scambio)
    for ordina in per_ordinamento:
        copia = list(originale)
        ordina(copia)
        print(f"{ordina.__name__:26} {originale} -> {copia}")
