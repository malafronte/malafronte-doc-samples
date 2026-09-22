"""Fattoriale ricorsivo e tracciatore didattico (Unità 6).

Collocare il file in `programmi/traccia_fattoriale_u6.py` della raccolta.
È il listato canonico con numerazione stabile citato dal cap. PY-10,
dalla figura sui frame e dalla guida al debugger.
Esecuzione: uv run python programmi/traccia_fattoriale_u6.py
"""


def fattoriale_ric(n: int) -> int:
    """Restituisce il fattoriale di n, intero non negativo.

    Base: n == 0. Il valore locale parziale esiste solo dopo il ritorno
    della chiamata: prima, nel chiamante sospeso, il nome non è associato.
    """
    if n == 0:
        return 1
    parziale = fattoriale_ric(n - 1)
    return n * parziale


def traccia_fattoriale(n: int) -> int:
    """Versione con stampe di osservazione: entra/esce a ogni chiamata.

    Le stampe sono strumenti di diagnosi e non fanno parte della funzione
    pura: il risultato resta il valore restituito, non l'output stampato.
    """
    print("entra", n)
    if n == 0:
        return 1
    parziale = traccia_fattoriale(n - 1)
    print("esce", n)
    return n * parziale


if __name__ == "__main__":
    print("fattoriale_ric(3) =", fattoriale_ric(3))
    print("traccia per n = 2:")
    print("risultato:", traccia_fattoriale(2))
