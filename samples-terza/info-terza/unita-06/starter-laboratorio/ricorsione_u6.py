"""Raccolta delle funzioni del laboratorio LAB-PY-U6 — versione di partenza.

Stato iniziale dichiarato: è fornito soltanto `fattoriale_iterativo`,
già noto dalle unità precedenti. Tutte le altre funzioni richieste
dalle istruzioni (fattoriale_ric, fibonacci_ric, fibonacci_iter,
hanoi e la funzione scelta per il trasferimento) vanno aggiunte qui
seguendo le fasi L2-L5: il file cresce insieme al laboratorio.
Non scrivere corpi finti: finché una funzione non è implementata, resta
assente, e i test che la importano falliscono in modo visibile.
L'import del modulo non deve chiedere input né stampare; le eventuali
presentazioni stanno in un main protetto dalla guardia di avvio.
"""


def fattoriale_iterativo(n: int) -> int:
    """Restituisce il fattoriale di n, intero non negativo (versione iterativa già nota).

    Prodotto accumulato sugli interi da 2 a n; per n minore di 2 il
    prodotto resta 1, il valore del prodotto vuoto.
    """
    prodotto = 1
    for fattore in range(2, n + 1):
        prodotto *= fattore
    return prodotto


# Fase L2 — Ricorsione lineare: aggiungere qui `fattoriale_ric` secondo il
# contratto del cap. PY-10 (base zero, riduzione n - 1, ricomposizione).

# Fase L3 — Fibonacci: aggiungere qui `fibonacci_ric` e `fibonacci_iter`
# con i due casi base e la coppia di valori consecutivi.

# Fase L4 — Hanoi: aggiungere qui `hanoi` con la firma del cap. PY-12
# (n, origine, destinazione, appoggio, mosse) e l'effetto dichiarato.

# Fase L5 — Trasferimento: aggiungere qui `somma_ric` oppure `mcd_ric`.

# Eventuale main protetto dalla guardia, per le presentazioni a stampa:
# if __name__ == "__main__":
#     ...
