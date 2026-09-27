"""Strumentazione separata dei confronti, degli scambi e dei sondaggi.

Questo modulo contiene **varianti nominate** delle ricerche e degli ordinamenti
del capitolo PY-14: sono versioni che contano gli eventi e li restituiscono
insieme al risultato, mentre le funzioni di riferimento di `ricerche_u10.py` e
`ordinamenti_u10.py` restituiscono soltanto il risultato del loro contratto.

La strumentazione **non modifica** il contratto delle funzioni di riferimento:
gli argomenti vengono ordinati o consultati esattamente allo stesso modo e le
varianti restituiscono in più il registro dei conteggi. La prova di questa
equivalenza è in `test_esempi_u10.py`: prima si verifica che il risultato
coincide, poi si leggono i numeri.

Vocabolario degli eventi, identico a quello del capitolo e del laboratorio:

- **confronto fra chiavi**: valutazione effettiva di un operatore di confronto
  fra due chiavi (`>`, `<`, `==`). Se l'operatore non viene valutato - per
  esempio perché un cortocircuito lo salta - il confronto non si conta.
- **scambio**: interversione di due posizioni della lista.
- **spostamento**: assegnamento che trasla di una posizione un elemento.
- **sondaggio**: accesso al medio della ricerca dicotomica. Un sondaggio non è
  un confronto: l'accesso può produrre un solo confronto Python, se l'uguaglianza
  è vera, oppure due - uguaglianza e poi minore - se non lo è.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


# ---------------------------------------------------------------------------
# Ricerche: sondaggi e confronti
# ---------------------------------------------------------------------------


def cerca_lineare_con_conteggi(valori, bersaglio):
    """Come `cerca_lineare`, più il registro dei conteggi.

    Restituisce un dizionario con `risultato`, `sondaggi` e `confronti`. Qui
    **sondaggi** indica gli elementi esaminati dalla scansione e **confronti** i
    `==` effettivamente valutati: i due numeri coincidono, perché ogni elemento
    esaminato produce un solo confronto. Il confronto serve a rendere visibile
    la differenza con la ricerca dicotomica, dove i due numeri divergono.
    """
    sondaggi = 0
    confronti = 0
    for indice in range(len(valori)):
        sondaggi += 1
        confronti += 1
        if valori[indice] == bersaglio:
            return {"risultato": indice, "sondaggi": sondaggi, "confronti": confronti}
    return {"risultato": None, "sondaggi": sondaggi, "confronti": confronti}


def cerca_dicotomica_con_conteggi(valori, bersaglio):
    """Come `cerca_dicotomica`, più il registro dei conteggi.

    Restituisce `risultato`, `sondaggi` e `confronti`. I **sondaggi** sono gli
    accessi a `valori[medio]`; i **confronti** sono gli operatori Python
    valutati su quel valore: `==` sempre, `<` soltanto se l'uguaglianza è falsa.
    Un sondaggio può dunque costare uno oppure due confronti.
    """
    sinistra = 0
    destra = len(valori) - 1
    candidato = None
    sondaggi = 0
    confronti = 0
    while sinistra <= destra:
        medio = (sinistra + destra) // 2
        valore_medio = valori[medio]
        sondaggi += 1
        confronti += 1
        if valore_medio == bersaglio:
            candidato = medio
            destra = medio - 1
        else:
            confronti += 1
            if valore_medio < bersaglio:
                sinistra = medio + 1
            else:
                destra = medio - 1
    return {"risultato": candidato, "sondaggi": sondaggi, "confronti": confronti}


# ---------------------------------------------------------------------------
# Ordinamenti: confronti, scambi e spostamenti
# ---------------------------------------------------------------------------


def insertion_sort_con_conteggi(valori):
    """Come `insertion_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto.
    Insertion sort **sposta** gli elementi e poi scrive la chiave nella
    posizione liberata: qui gli scambi sono zero per costruzione e i
    `spostamenti` contano gli assegnamenti di traslazione.
    """
    confronti = 0
    spostamenti = 0
    for indice in range(1, len(valori)):
        chiave = valori[indice]
        posizione = indice - 1
        while posizione >= 0:
            confronti += 1
            if valori[posizione] > chiave:
                valori[posizione + 1] = valori[posizione]
                spostamenti += 1
                posizione -= 1
            else:
                break
        valori[posizione + 1] = chiave
    return {"confronti": confronti, "scambi": 0, "spostamenti": spostamenti}


def selection_sort_con_conteggi(valori):
    """Come `selection_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto. Il
    numero di confronti è fisso per ogni disposizione di n elementi:
    n(n-1)/2, perché il minimo del suffisso si cerca sempre fino in fondo. Le
    righe di assegnamento `minimo = j` e `minimo = indice` non sono né confronti
    né scambi e non compaiono nel registro.
    """
    confronti = 0
    scambi = 0
    n = len(valori)
    for indice in range(n - 1):
        minimo = indice
        for j in range(indice + 1, n):
            confronti += 1
            if valori[j] < valori[minimo]:
                minimo = j
        if minimo != indice:
            valori[indice], valori[minimo] = valori[minimo], valori[indice]
            scambi += 1
    return {"confronti": confronti, "scambi": scambi, "spostamenti": 0}


def bubble_sort_con_conteggi(valori):
    """Come `bubble_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto. Le
    passate sono fisse: n(n-1)/2 confronti fra chiavi per ogni disposizione,
    compresa la lista già ordinata. Gli `spostamenti` sono zero: bubble
    interviene soltanto per scambi.
    """
    confronti = 0
    scambi = 0
    n = len(valori)
    for passata in range(n - 1):
        for j in range(0, n - 1 - passata):
            confronti += 1
            if valori[j] > valori[j + 1]:
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi += 1
    return {"confronti": confronti, "scambi": scambi, "spostamenti": 0}


def bubble_sort_ottimizzato_con_conteggi(valori):
    """Come `bubble_sort_ottimizzato`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto. Sul
    già ordinato il conteggio è n-1 confronti per n ≥ 1 - una sola
    passata, poi l'arresto - e zero scambi; sul caso peggiore è
    n(n-1)/2. La variante con l'ultimo scambio si conta separatamente, con la
    funzione omonima di `ordinamenti_u10.py` e un registro dedicato.
    """
    confronti = 0
    scambi = 0
    n = len(valori)
    for passata in range(n - 1):
        scambi_avvenuti = False
        for j in range(0, n - 1 - passata):
            confronti += 1
            if valori[j] > valori[j + 1]:
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi += 1
                scambi_avvenuti = True
        if not scambi_avvenuti:
            break
    return {"confronti": confronti, "scambi": scambi, "spostamenti": 0}


# ---------------------------------------------------------------------------
# Formule attese - base di verifica dei conteggi
# ---------------------------------------------------------------------------


def confronti_attesi_semplici(n):
    """Restituisce i confronti attesi di selection e bubble semplice su n elementi.

    La formula è n(n-1)/2 e vale per **ogni** disposizione degli elementi.
    I valori per n piccoli sono 0, 0, 1, 3, 6, 10, … e si controllano
    a mano prima di usare la formula in una tabella.
    """
    return n * (n - 1) // 2


def confronti_attesi_inserimento_ordinato(n):
    """Restituisce i confronti attesi di insertion sort su lista già ordinata.

    La formula è n-1 per n ≥ 1: una sola valutazione negativa della
    condizione per ogni chiave inserita. Per n = 0 il valore è 0.
    """
    return max(0, n - 1)


if __name__ == "__main__":
    # Contatori su n = 4 per i due casi che separano le formule. Uscita attesa:
    #   insertion  ordinato -> confronti 3, scambi 0, spostamenti 0
    #   insertion  inverso  -> confronti 6, scambi 0, spostamenti 6
    #   selection  ordinato -> confronti 6, scambi 0, spostamenti 0
    #   selection  inverso  -> confronti 6, scambi 2, spostamenti 0
    #   bubble     ordinato -> confronti 6, scambi 0, spostamenti 0
    #   bubble     inverso  -> confronti 6, scambi 6, spostamenti 0
    #   bubble_ott ordinato -> confronti 3, scambi 0, spostamenti 0
    #   bubble_ott inverso  -> confronti 6, scambi 6, spostamenti 0
    scelte = (
        ("insertion", insertion_sort_con_conteggi),
        ("selection", selection_sort_con_conteggi),
        ("bubble", bubble_sort_con_conteggi),
        ("bubble_ott", bubble_sort_ottimizzato_con_conteggi),
    )
    for nome, conta in scelte:
        for caso, originale in (("ordinato", [0, 1, 2, 3]), ("inverso", [4, 3, 2, 1])):
            registro = conta(list(originale))
            print(f"{nome:12} {caso:9} -> confronti {registro['confronti']}, "
                  f"scambi {registro['scambi']}, spostamenti {registro['spostamenti']}")
