"""Riferimento del LAB-PY-U10: gli ordinamenti completi e verificati.

Controparte completa dello starter `ordinamenti_u10.py`. Le quattro funzioni
hanno lo stesso contratto e lo stesso parametro `chiave` dello starter: si
leggono **dopo** le fasi L2-L3, come confronto formativo. Le durate e le
scelte di dettaglio non sono l'unica soluzione possibile: il confronto riguarda
invariante, condizioni di arresto e ordine degli aggiornamenti.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`.
"""


def _valutatore(chiave):
    """Restituisce la funzione che produce il valore confrontabile di un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def insertion_sort(valori, chiave=None):
    """Ordina `valori` sul posto con l'inserimento diretto; restituisce `None`.

    Versione stabile: si spostano soltanto gli elementi **strettamente maggiori**
    della chiave corrente, quindi l'uguaglianza non provoca spostamenti.
    Confronti fra chiavi: `n-1` su lista già ordinata, `n(n-1)/2` su lista
    inversa. Spazio ausiliario costante.
    """
    valore = _valutatore(chiave)
    for indice in range(1, len(valori)):
        record = valori[indice]
        chiave_corrente = valore(record)
        posizione = indice - 1
        while posizione >= 0 and valore(valori[posizione]) > chiave_corrente:
            valori[posizione + 1] = valori[posizione]
            posizione -= 1
        valori[posizione + 1] = record
    return None


def selection_sort(valori, chiave=None):
    """Ordina `valori` sul posto col minimo del suffisso; restituisce `None`.

    Versione standard **non stabile**: lo scambio fra la posizione corrente e
    quella del minimo può invertire due elementi con la stessa chiave.
    Confronti fra chiavi: `n(n-1)/2` per ogni disposizione. Scambi: al massimo
    `n-1`. Spazio ausiliario costante.
    """
    valore = _valutatore(chiave)
    n = len(valori)
    for indice in range(n - 1):
        minimo = indice
        for j in range(indice + 1, n):
            if valore(valori[j]) < valore(valori[minimo]):
                minimo = j
        if minimo != indice:
            valori[indice], valori[minimo] = valori[minimo], valori[indice]
    return None


def bubble_sort(valori, chiave=None):
    """Ordina `valori` sul posto con passaggi fissi; restituisce `None`.

    Versione stabile: si scambia solo con `>`. Confronti fra chiavi:
    `n(n-1)/2` per ogni disposizione, compresa la lista già ordinata, dove gli
    scambi sono zero. Spazio ausiliario costante.
    """
    valore = _valutatore(chiave)
    n = len(valori)
    for passata in range(n - 1):
        for j in range(0, n - 1 - passata):
            if valore(valori[j]) > valore(valori[j + 1]):
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
    return None


def bubble_sort_ottimizzato(valori, chiave=None):
    """Come `bubble_sort`, con la zona ridotta e l'arresto; restituisce `None`.

    Due effetti distinti: la zona esaminata si restringe a ogni passata e il
    ciclo si interrompe quando una passata non compie alcuno scambio. Sul già
    ordinato: una passata e `n-1` confronti per `n >= 1`. Versione stabile.
    """
    valore = _valutatore(chiave)
    n = len(valori)
    for passata in range(n - 1):
        scambi_avvenuti = False
        for j in range(0, n - 1 - passata):
            if valore(valori[j]) > valore(valori[j + 1]):
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi_avvenuti = True
        if not scambi_avvenuti:
            break
    return None


if __name__ == "__main__":
    prova = [5, 2, 4, 2]
    insertion_sort(prova)
    print("insertion_sort([5, 2, 4, 2]) ->", prova)
