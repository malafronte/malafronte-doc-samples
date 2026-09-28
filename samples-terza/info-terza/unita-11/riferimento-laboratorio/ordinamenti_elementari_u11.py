"""Quattro ordinamenti elementari del cap. PY-14 - **modulo di servizio completo**.

Questo file non contiene alcun corpo da completare e non è oggetto del
LAB-PY-U11: conserva le quattro implementazioni elementari del cap. PY-14 -
`insertion_sort`, `selection_sort`, `bubble_sort` e `bubble_sort_ottimizzato` -
perché nella fase L8 il confronto comprenda **tutti** gli ordinamenti del corso,
U10 e U11 insieme a `sorted`. Senza questo modulo la parte essenziale del
laboratorio resterebbe comunque completa: MergeSort, QuickSort e `sorted` si
confrontano con i soli file di questa cartella.

Il nome del file è diverso da `ordinamenti_u10.py` per evitare la collisione di
import che si produrrebbe copiando nella stessa cartella i file del LAB-PY-U10:
le funzioni conservano invece i nomi e i contratti del capitolo. Sono gli stessi
contratti già verificati nel LAB-PY-U10: ordinamento sul posto, restituisce
`None`, parametro opzionale `chiave`.

Le proprietà da ricordare quando si legge la tabella finale: insertion e bubble
sono **stabili** perché l'uguaglianza non sposta né scambia; selection standard
**non lo è**; bubble ottimizzato arresta le passate quando una non compie
scambi. Confronti fra chiavi: `n(n-1)/2` per selection e bubble semplice in ogni
disposizione; `n-1` sul già ordinato per insertion e bubble ottimizzato.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
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
    for ordinamento in (insertion_sort, selection_sort, bubble_sort, bubble_sort_ottimizzato):
        prova = [5, 2, 4, 2]
        ordinamento(prova)
        print(f"{ordinamento.__name__}([5, 2, 4, 2]) -> {prova}")
