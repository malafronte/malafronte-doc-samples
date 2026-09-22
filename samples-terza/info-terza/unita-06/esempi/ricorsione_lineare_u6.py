"""Funzioni ricorsive lineari dell'Unità 6: fattoriale, somma, MCD.

Collocare il file in `programmi/ricorsione_lineare_u6.py` della raccolta
dello studente. L'import non chiede input e non stampa: le dimostrazioni
stanno nel main protetto dalla guardia.
Esecuzione: uv run python programmi/ricorsione_lineare_u6.py
"""


def fattoriale_ric(n: int) -> int:
    """Restituisce il fattoriale di n (prodotto degli interi da 1 a n).

    Dominio: n intero non negativo (0! = 1 per definizione).
    Nessun input, nessuna stampa, nessun effetto: funzione pura.
    Base: n == 0. Riduzione: n - 1. Ricomposizione: n * parziale.
    """
    if n == 0:
        return 1
    parziale = fattoriale_ric(n - 1)
    return n * parziale


def fattoriale_iter(n: int) -> int:
    """Restituisce il fattoriale di n con l'accumulo iterativo già noto.

    Stesso dominio e stesso contratto di fattoriale_ric: cambia soltanto
    l'organizzazione del lavoro, non il risultato promesso.
    """
    prodotto = 1
    for fattore in range(2, n + 1):
        prodotto *= fattore
    return prodotto


def somma_ric(n: int) -> int:
    """Restituisce la somma degli interi da 1 a n (0 per n = 0).

    Dominio: n intero non negativo.
    Base: n == 0 con il neutro dell'addizione. Ricomposizione: n + parziale.
    """
    if n == 0:
        return 0
    parziale = somma_ric(n - 1)
    return n + parziale


def mcd_ric(a: int, b: int) -> int:
    """Restituisce il massimo comune divisore di a e b con Euclide.

    Dominio: a e b interi non negativi, non entrambi zero.
    Base: b == 0 (il risultato è a). Riduzione: la coppia (b, a % b),
    con secondo argomento strettamente decrescente nei passi ricorsivi.
    """
    if b == 0:
        return a
    return mcd_ric(b, a % b)


if __name__ == "__main__":
    print("fattoriale:", [fattoriale_ric(n) for n in (0, 1, 3, 5)])
    print("somma:     ", [somma_ric(n) for n in (0, 1, 4, 10)])
    print("mcd:       ", [mcd_ric(a, b) for a, b in ((48, 18), (7, 0), (0, 7), (7, 7), (12, 18))])
    print("confronto iterativo:", fattoriale_iter(5) == fattoriale_ric(5))
