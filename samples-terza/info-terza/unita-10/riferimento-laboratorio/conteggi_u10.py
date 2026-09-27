"""Riferimento del LAB-PY-U10: la strumentazione dei conteggi completa.

Controparte completa dello starter `conteggi_u10.py`. Le quattro funzioni
ordinano esattamente come le controparti di `ordinamenti_u10.py` e restituiscono
in più il registro `{"confronti", "scambi", "spostamenti"}`. La prova di
equivalenza è nei casi L09 della suite: prima si verifica che il risultato
coincide, poi si leggono i numeri.

Eventi contati:

- **confronto fra chiavi**: valutazione effettiva di `>` o `<` fra due chiavi;
- **scambio**: interversione di due posizioni della lista;
- **spostamento**: assegnamento che trasla di una posizione un elemento.
"""


def _valutatore(chiave):
    """Restituisce la funzione che produce il valore confrontabile di un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def insertion_sort_con_conteggi(valori, chiave=None):
    """Come `insertion_sort`, più `{"confronti", "scambi", "spostamenti"}`.

    Insertion sort non interviene mai per scambio: `scambi` è zero per
    costruzione. I `spostamenti` contano le traslazioni di una posizione.
    """
    valore = _valutatore(chiave)
    confronti = 0
    spostamenti = 0
    for indice in range(1, len(valori)):
        record = valori[indice]
        chiave_corrente = valore(record)
        posizione = indice - 1
        while posizione >= 0:
            confronti += 1
            if valore(valori[posizione]) > chiave_corrente:
                valori[posizione + 1] = valori[posizione]
                spostamenti += 1
                posizione -= 1
            else:
                break
        valori[posizione + 1] = record
    return {"confronti": confronti, "scambi": 0, "spostamenti": spostamenti}


def selection_sort_con_conteggi(valori, chiave=None):
    """Come `selection_sort`, più `{"confronti", "scambi", "spostamenti"}`.

    Il numero di confronti è fisso per ogni disposizione di `n` elementi:
    `n(n-1)/2`. Gli `spostamenti` sono zero: selection interviene per scambio.
    """
    valore = _valutatore(chiave)
    confronti = 0
    scambi = 0
    n = len(valori)
    for indice in range(n - 1):
        minimo = indice
        for j in range(indice + 1, n):
            confronti += 1
            if valore(valori[j]) < valore(valori[minimo]):
                minimo = j
        if minimo != indice:
            valori[indice], valori[minimo] = valori[minimo], valori[indice]
            scambi += 1
    return {"confronti": confronti, "scambi": scambi, "spostamenti": 0}


def bubble_sort_con_conteggi(valori, chiave=None):
    """Come `bubble_sort`, più `{"confronti", "scambi", "spostamenti"}`.

    Le passate sono fisse: `n(n-1)/2` confronti per ogni disposizione, compresa
    la lista già ordinata. Gli `spostamenti` sono zero.
    """
    valore = _valutatore(chiave)
    confronti = 0
    scambi = 0
    n = len(valori)
    for passata in range(n - 1):
        for j in range(0, n - 1 - passata):
            confronti += 1
            if valore(valori[j]) > valore(valori[j + 1]):
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi += 1
    return {"confronti": confronti, "scambi": scambi, "spostamenti": 0}


def bubble_sort_ottimizzato_con_conteggi(valori, chiave=None):
    """Come `bubble_sort_ottimizzato`, più `{"confronti", "scambi", "spostamenti"}`.

    Sul già ordinato: `n-1` confronti per `n >= 1` e zero scambi. Sul caso
    peggiore: `n(n-1)/2` confronti.
    """
    valore = _valutatore(chiave)
    confronti = 0
    scambi = 0
    n = len(valori)
    for passata in range(n - 1):
        scambi_avvenuti = False
        for j in range(0, n - 1 - passata):
            confronti += 1
            if valore(valori[j]) > valore(valori[j + 1]):
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi += 1
                scambi_avvenuti = True
        if not scambi_avvenuti:
            break
    return {"confronti": confronti, "scambi": scambi, "spostamenti": 0}


def formule_attese(n):
    """Restituisce i conteggi attesi per una lista di `n` elementi (fornita)."""
    return {
        "triangolare": n * (n - 1) // 2,
        "lineare_ordinato": max(0, n - 1),
    }


if __name__ == "__main__":
    registro = bubble_sort_ottimizzato_con_conteggi([1, 2, 3, 4])
    print("bubble_sort_ottimizzato_con_conteggi([1, 2, 3, 4]) ->", registro)
