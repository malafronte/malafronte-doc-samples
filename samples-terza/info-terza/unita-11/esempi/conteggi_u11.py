"""Varianti strumentate di fusione, partizione, MergeSort e QuickSort.

Queste funzioni sono **varianti nominate** delle quattro funzioni canoniche di
`merge_quick_u11.py`: aggiungono un registro dei conteggi e non cambiano né il
risultato né gli effetti. La prova di equivalenza è nei test: prima si verifica
che il risultato coincide con quello della controparte senza contatori, poi si
leggono i numeri. Le versioni con contatori **non vanno cronometrate** per
attribuirne il tempo alle versioni ordinarie.

Eventi contati, con lo stesso vocabolario del cap. PY-14 esteso a `<=`:

- **confronto fra chiavi**: valutazione effettiva di un operatore di confronto
  (`<`, `>`, `<=`, `>=`, `==`) fra due chiavi, compresa quella falsa che
  interrompe un ciclo. Se l'operatore non viene valutato, il confronto non si
  conta.
- **scambio**: interversione di due posizioni **diverse** della lista. Gli
  scambi con le due posizioni coincidenti non si eseguono e non si contano.
- **copia**: assegnamento che scrive un elemento di una sequenza in un'altra
  sequenza o in una nuova posizione della stessa. Comprende le copie delle metà
  prodotte dallo slicing, le copie del caso base e le scritture nella lista
  risultato della fusione.
- **profondità massima**: numero massimo di frame ricorsivi contemporaneamente
  attivi durante l'esecuzione, con la chiamata esterna che vale 1.

Registri restituiti:

| Funzione | Registro |
|---|---|
| `fondi_ordinate_con_conteggi` | `{"risultato", "confronti", "copie"}` |
| `merge_sort_con_conteggi` | `{"risultato", "confronti", "copie", "profondita_massima"}` |
| `partiziona_lomuto_con_conteggi` | `{"pivot_finale", "confronti", "scambi"}` |
| `quick_sort_con_conteggi` | `{"confronti", "scambi", "copie", "profondita_massima"}` |

`merge_sort_con_conteggi` restituisce la lista ordinata **nuova** e non modifica
l'ingresso; `partiziona_lomuto_con_conteggi` e `quick_sort_con_conteggi`
modificano la lista come le loro controparti. Il campo `copie` di QuickSort è
sempre zero: la partizione canonica scambia posizioni della stessa lista e non
copia elementi in sequenze nuove.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


def _valutatore(chiave):
    """Restituisce la funzione che estrae la chiave di confronto da un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def _fondi_contata(sinistra, destra, chiave, stato):
    """Fonde due liste ordinate aggiornando `stato` con confronti e copie."""
    valore = _valutatore(chiave)
    risultato = []
    j = 0
    k = 0
    while j < len(sinistra) and k < len(destra):
        stato["confronti"] += 1
        if valore(sinistra[j]) <= valore(destra[k]):
            risultato.append(sinistra[j])
            stato["copie"] += 1
            j += 1
        else:
            risultato.append(destra[k])
            stato["copie"] += 1
            k += 1
    while j < len(sinistra):
        risultato.append(sinistra[j])
        stato["copie"] += 1
        j += 1
    while k < len(destra):
        risultato.append(destra[k])
        stato["copie"] += 1
        k += 1
    return risultato


def _merge_sort_contato(valori, chiave, stato, profondita):
    """Versione ricorsiva di `merge_sort` che aggiorna `stato` a ogni passo."""
    if profondita > stato["profondita_massima"]:
        stato["profondita_massima"] = profondita
    if len(valori) <= 1:
        stato["copie"] += len(valori)
        return list(valori)
    meta = len(valori) // 2
    stato["copie"] += len(valori)  # le due metà prodotte dallo slicing
    sinistra = _merge_sort_contato(valori[:meta], chiave, stato, profondita + 1)
    destra = _merge_sort_contato(valori[meta:], chiave, stato, profondita + 1)
    return _fondi_contata(sinistra, destra, chiave, stato)


def _partiziona_contata(valori, sinistra, destra, chiave, stato):
    """Versione di `partiziona_lomuto` che aggiorna `stato` con confronti e scambi."""
    valore = _valutatore(chiave)
    pivot = valori[destra]
    chiave_pivot = valore(pivot)
    confine = sinistra - 1
    for j in range(sinistra, destra):
        stato["confronti"] += 1
        if valore(valori[j]) <= chiave_pivot:
            confine += 1
            if confine != j:
                valori[confine], valori[j] = valori[j], valori[confine]
                stato["scambi"] += 1
    posizione = confine + 1
    if posizione != destra:
        valori[posizione], valori[destra] = valori[destra], valori[posizione]
        stato["scambi"] += 1
    return posizione


def _quick_sort_contato(valori, sinistra, destra, chiave, stato, profondita):
    """Versione ricorsiva di `quick_sort` che aggiorna `stato` a ogni passo.

    La profondità viene registrata all'ingresso di ogni chiamata, comprese
    quelle sugli intervalli di 0 o 1 elemento: la chiamata che ordina l'intera
    lista vale 1 e ogni sottoproblema aggiunge un livello.
    """
    if profondita > stato["profondita_massima"]:
        stato["profondita_massima"] = profondita
    if sinistra >= destra:
        return
    p = _partiziona_contata(valori, sinistra, destra, chiave, stato)
    _quick_sort_contato(valori, sinistra, p - 1, chiave, stato, profondita + 1)
    _quick_sort_contato(valori, p + 1, destra, chiave, stato, profondita + 1)


def fondi_ordinate_con_conteggi(sinistra, destra, chiave=None):
    """Come `fondi_ordinate`, più il registro dei conteggi.

    Restituisce `{"risultato", "confronti", "copie"}`: `risultato` è la lista
    nuova fusa, `confronti` conta i `<=` fra chiavi, `copie` conta le scritture
    degli elementi nella lista risultato. Gli ingressi non vengono modificati.
    """
    stato = {"confronti": 0, "copie": 0}
    risultato = _fondi_contata(sinistra, destra, chiave, stato)
    return {
        "risultato": risultato,
        "confronti": stato["confronti"],
        "copie": stato["copie"],
    }


def merge_sort_con_conteggi(valori, chiave=None):
    """Come `merge_sort`, più il registro dei conteggi.

    Restituisce `{"risultato", "confronti", "copie", "profondita_massima"}`:
    `risultato` è la lista ordinata **nuova**, `copie` conta anche le metà
    prodotte dallo slicing e le copie del caso base, `profondita_massima` è la
    profondità raggiunta dallo stack ricorsivo. `valori` non viene modificato.

    Per `n` potenza di due le copie sono esattamente `2n·log2(n) + n`, come
    restituito da `copie_attese_merge_sort`.
    """
    stato = {"confronti": 0, "copie": 0, "profondita_massima": 0}
    risultato = _merge_sort_contato(valori, chiave, stato, 1)
    return {
        "risultato": risultato,
        "confronti": stato["confronti"],
        "copie": stato["copie"],
        "profondita_massima": stato["profondita_massima"],
    }


def partiziona_lomuto_con_conteggi(valori, sinistra, destra, chiave=None):
    """Come `partiziona_lomuto`, più il registro dei conteggi.

    Restituisce `{"pivot_finale", "confronti", "scambi"}` e modifica in posto
    l'intervallo `[sinistra, destra]`, come la controparte senza contatori.
    I confronti sono `destra - sinistra`, uno per ogni elemento non pivot.
    """
    stato = {"confronti": 0, "scambi": 0}
    pivot_finale = _partiziona_contata(valori, sinistra, destra, chiave, stato)
    return {
        "pivot_finale": pivot_finale,
        "confronti": stato["confronti"],
        "scambi": stato["scambi"],
    }


def quick_sort_con_conteggi(valori, chiave=None):
    """Come `quick_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "copie", "profondita_massima"}` e ordina
    `valori` sul posto, come la controparte senza contatori. `copie` è sempre 0:
    la partizione canonica scambia posizioni della stessa lista e non costruisce
    sequenze nuove.
    """
    stato = {"confronti": 0, "scambi": 0, "copie": 0, "profondita_massima": 0}
    _quick_sort_contato(valori, 0, len(valori) - 1, chiave, stato, 1)
    return {
        "confronti": stato["confronti"],
        "scambi": stato["scambi"],
        "copie": stato["copie"],
        "profondita_massima": stato["profondita_massima"],
    }


def confronti_massimi_fusione(a, b):
    """Restituisce il limite superiore dei confronti per fondere liste di `a` e `b` elementi.

    Con entrambe le liste non vuote i confronti sono al più `a + b - 1`; con un
    lato vuoto sono zero. Il valore è un **limite**, non un risultato atteso:
    `[1, 2]` e `[3, 4]` si fondono con `a + b - 2` confronti, perché l'ultimo
    elemento si inserisce senza confronto.
    """
    if a < 0 or b < 0:
        raise ValueError("le lunghezze non possono essere negative")
    return 0 if a == 0 or b == 0 else a + b - 1


def copie_attese_merge_sort(n):
    """Restituisce il numero esatto di copie elementari compiute da `merge_sort` su `n` elementi.

    La funzione segue la stessa struttura ricorsiva del codice: ogni chiamata su
    `n >= 2` elementi copia `n` elementi nelle due metà e `n` elementi nel
    risultato della fusione, più le copie delle chiamate ricorsive. Il caso base
    copia i suoi 0 o 1 elementi.

    Per `n` potenza di due il valore coincide con `2n·log2(n) + n`:
    `n = 1` dà 1, `n = 2` dà 6, `n = 4` dà 20. Le copie totali crescono come
    Θ(n log n), mentre la memoria occupata **contemporaneamente** resta Θ(n).
    """
    if n < 0:
        raise ValueError("il numero di elementi non può essere negativo")
    if n <= 1:
        return n
    meta = n // 2
    return 2 * n + copie_attese_merge_sort(meta) + copie_attese_merge_sort(n - meta)


if __name__ == "__main__":
    print("Fusione contata di [1, 3, 5] e [2, 3, 6]:")
    print(fondi_ordinate_con_conteggi([1, 3, 5], [2, 3, 6]))
    # {'risultato': [1, 2, 3, 3, 5, 6], 'confronti': 5, 'copie': 6}

    print("MergeSort contato su [5, 2, 4, 2]:")
    print(merge_sort_con_conteggi([5, 2, 4, 2]))
    # {'risultato': [2, 2, 4, 5], 'confronti': 5, 'copie': 20, 'profondita_massima': 3}

    print("Partizione contata su [2a, 2b, 1c]:")
    marcati = [(2, "a"), (2, "b"), (1, "c")]
    print(partiziona_lomuto_con_conteggi(marcati, 0, 2, chiave=lambda r: r[0]))
    # {'pivot_finale': 0, 'confronti': 2, 'scambi': 1}

    print("QuickSort contato su [5, 2, 4, 2]:")
    valori = [5, 2, 4, 2]
    print(quick_sort_con_conteggi(valori), valori)
    # {'confronti': 4, 'scambi': 2, 'copie': 0, 'profondita_massima': 3} [2, 2, 4, 5]

    print("Copie attese di MergeSort su n = 1, 2, 4, 8:")
    print([copie_attese_merge_sort(n) for n in (1, 2, 4, 8)])  # [1, 6, 20, 56]
