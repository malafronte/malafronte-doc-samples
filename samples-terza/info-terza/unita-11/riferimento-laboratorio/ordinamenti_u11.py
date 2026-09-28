"""Riferimento del LAB-PY-U11: fusione, partizione e ordinamenti completi.

Controparte completa dello starter `ordinamenti_u11.py`. Le quattro funzioni
hanno lo stesso contratto e lo stesso parametro `chiave` dello starter: si
leggono **dopo** le fasi L2-L3, come confronto formativo. Le scelte di dettaglio
non sono l'unica soluzione possibile: il confronto riguarda invariante della
fusione, condizioni di scambio della partizione e ordine delle chiamate
ricorsive.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`.
"""


def _valutatore(chiave):
    """Restituisce la funzione che produce il valore confrontabile di un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def fondi_ordinate(sinistra, destra, chiave=None):
    """Restituisce la lista nuova che fonde `sinistra` e `destra`, entrambe già ordinate.

    Due indici, scelta di sinistra a parità di chiave, resto dell'altro lato
    copiato senza confronti. Al più `a + b - 1` confronti con entrambi i lati non
    vuoti.
    """
    valore = _valutatore(chiave)
    risultato = []
    j = 0
    k = 0
    while j < len(sinistra) and k < len(destra):
        if valore(sinistra[j]) <= valore(destra[k]):
            risultato.append(sinistra[j])
            j += 1
        else:
            risultato.append(destra[k])
            k += 1
    risultato.extend(sinistra[j:])
    risultato.extend(destra[k:])
    return risultato


def merge_sort(valori, chiave=None):
    """Restituisce la lista nuova che contiene `valori` in ordine non decrescente.

    Caso base `len(valori) <= 1` con restituzione della copia, divisione a metà
    con lo slicing e fusione stabile dei due risultati. `valori` non viene
    modificato.
    """
    if len(valori) <= 1:
        return list(valori)
    meta = len(valori) // 2
    sinistra = merge_sort(valori[:meta], chiave)
    destra = merge_sort(valori[meta:], chiave)
    return fondi_ordinate(sinistra, destra, chiave)


def partiziona_lomuto(valori, sinistra, destra, chiave=None):
    """Riordina `valori[sinistra:destra+1]` attorno al pivot e ne restituisce l'indice.

    Pivot finale `valori[destra]`, confronto `<=`, prefisso `sinistra..confine`
    con chiave minore o uguale al pivot, scambio finale del pivot nella posizione
    `confine + 1` solo se diversa da `destra`.
    """
    valore = _valutatore(chiave)
    pivot = valori[destra]
    chiave_pivot = valore(pivot)
    confine = sinistra - 1
    for j in range(sinistra, destra):
        if valore(valori[j]) <= chiave_pivot:
            confine += 1
            if confine != j:
                valori[confine], valori[j] = valori[j], valori[confine]
    posizione = confine + 1
    if posizione != destra:
        valori[posizione], valori[destra] = valori[destra], valori[posizione]
    return posizione


def quick_sort(valori, chiave=None):
    """Ordina `valori` sul posto in ordine non decrescente; restituisce `None`.

    Uscita per intervalli di 0 o 1 elemento senza chiamare la partizione; i due
    sottointervalli ricorsivi escludono il pivot.
    """
    _quick_sort_intervallo(valori, 0, len(valori) - 1, chiave)
    return None


def _quick_sort_intervallo(valori, sinistra, destra, chiave):
    """Ordina sul posto `valori[sinistra:destra+1]`; nessuna azione per 0 o 1 elemento."""
    if sinistra >= destra:
        return
    p = partiziona_lomuto(valori, sinistra, destra, chiave)
    _quick_sort_intervallo(valori, sinistra, p - 1, chiave)
    _quick_sort_intervallo(valori, p + 1, destra, chiave)


if __name__ == "__main__":
    prova = [5, 2, 4, 2]
    print("merge_sort([5, 2, 4, 2]) ->", merge_sort(prova), "| ingresso:", prova)
    quick_sort(prova)
    print("quick_sort([5, 2, 4, 2]) ->", prova)
