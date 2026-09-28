"""Ricerche del cap. PY-14 - **modulo di servizio completo**.

Questo file non contiene alcun corpo da completare e non è oggetto del
LAB-PY-U11: conserva il contratto canonico della ricerca per il **primo indice**
usato dalla fase L7, dove si misura e si previene il costo di una serie di
interrogazioni su una lista già ordinata. Le due funzioni sono quelle verificate
nel LAB-PY-U10 e nel cap. PY-14: `None` indica l'assenza e `0` è un risultato
valido, da controllare con `is None`.

Il nome del file è diverso da `ricerche_u10.py` per evitare collisioni di import
nella cartella di lavoro dello studente; le funzioni conservano nomi e
contratti.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


def cerca_lineare(valori, bersaglio):
    """Restituisce il primo indice di `bersaglio` in `valori`, oppure `None`.

    Nessuna precondizione di ordinamento. L'uscita è al primo incontro e `0` è
    un risultato valido: l'assenza si riconosce con `is None`. Confronti `==`:
    fino a `n`, uno per ogni elemento esaminato.
    """
    for indice in range(len(valori)):
        if valori[indice] == bersaglio:
            return indice
    return None


def cerca_dicotomica(valori, bersaglio):
    """Restituisce il primo indice di `bersaglio` in `valori` ordinato, oppure `None`.

    Precondizione: `valori` è una lista **non decrescente**; il controllo non è
    compito della funzione. Estremi inclusivi, medio `(sinistra + destra) // 2`;
    a parità si aggiorna il candidato e si prosegue nella metà **sinistra**, per
    restituire il primo indice. Un sondaggio può produrre un confronto
    (uguaglianza vera) oppure due (uguaglianza falsa e confronto di ordine).
    """
    sinistra = 0
    destra = len(valori) - 1
    candidato = None
    while sinistra <= destra:
        medio = (sinistra + destra) // 2
        if valori[medio] == bersaglio:
            candidato = medio
            destra = medio - 1
        elif valori[medio] < bersaglio:
            sinistra = medio + 1
        else:
            destra = medio - 1
    return candidato


if __name__ == "__main__":
    ordinata = [1, 3, 3, 3, 8]
    print("cerca_lineare([1, 3, 3, 3, 8], 3) ->", cerca_lineare(ordinata, 3))
    print("cerca_dicotomica([1, 3, 3, 3, 8], 3) ->", cerca_dicotomica(ordinata, 3))
    print("cerca_dicotomica([1, 3, 3, 3, 8], 7) ->", cerca_dicotomica(ordinata, 7))
