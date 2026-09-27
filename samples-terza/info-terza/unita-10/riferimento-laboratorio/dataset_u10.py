"""Starter del LAB-PY-U10: le cinque famiglie di input (fornito completo).

Questo file **non** è da completare: prepara gli input del confronto e
garantisce che tutti gli algoritmi ricevano gli **stessi** dati. La fase L5 -
Dataset consiste nel usarlo, controllarne il determinismo e dichiarare seme e
costruzione nella scheda del protocollo.

Le cinque famiglie sono `ordinato`, `inverso`, `quasi_ordinato`,
`molti_duplicati`, `pseudo_casuale`. La famiglia `quasi_ordinato` non è un
nome generico: viene costruita esattamente come dichiarato in
`genera_famiglia`, perché lo stesso nome può descrivere input diversi se non
ne è specificata la costruzione.

Ambiente: CPython sul computer, sola libreria standard (`random`).
"""

import random

FAMIGLIE = ("ordinato", "inverso", "quasi_ordinato", "molti_duplicati", "pseudo_casuale")

SEME = 20260927


def genera_famiglia(nome, n, seme=SEME):
    """Restituisce una lista di `n` interi della famiglia `nome`.

    | `nome` | Costruzione |
    |---|---|
    | `ordinato` | `list(range(n))`, già crescente |
    | `inverso` | `list(range(n, 0, -1))`, strettamente decrescente |
    | `quasi_ordinato` | `list(range(n))` con due scambi dichiarati: le posizioni `(0, 1)` e `(n // 2, n // 2 + 1)`; richiede `n >= 4`, altrimenti la lista resta ordinata |
    | `molti_duplicati` | `n` valori da `random.Random(seme).randrange(3)`, quindi solo 0, 1 e 2 |
    | `pseudo_casuale` | `n` valori da `random.Random(seme).randrange(n + 1)`, con il seme esplicito |

    Il seme è parte del protocollo: a parità di nome, `n` e seme la lista è
    sempre la stessa. La lista è **nuova** a ogni chiamata, così nessun
    algoritmo può modificarla a danno del successivo.
    """
    if nome not in FAMIGLIE:
        raise ValueError(f"famiglia sconosciuta: {nome!r}; ammesse: {FAMIGLIE}")
    if n < 0:
        raise ValueError("il numero di elementi non può essere negativo")

    if nome == "ordinato":
        return list(range(n))
    if nome == "inverso":
        return list(range(n, 0, -1))
    if nome == "quasi_ordinato":
        valori = list(range(n))
        if n >= 4:
            valori[0], valori[1] = valori[1], valori[0]
            meta = n // 2
            valori[meta], valori[meta + 1] = valori[meta + 1], valori[meta]
        return valori
    if nome == "molti_duplicati":
        casuale = random.Random(seme)
        return [casuale.randrange(3) for _ in range(n)]
    casuale = random.Random(seme)
    return [casuale.randrange(n + 1) for _ in range(n)]


def copie_indipendenti(originale, quante):
    """Restituisce `quante` copie **separate** della stessa lista originale.

    Ogni algoritmo riceve una copia propria: se due procedure lavorassero sulla
    stessa lista, la seconda la troverebbe già ordinata e il confronto non
    sarebbe valido. La copia si prepara **fuori** dalla regione cronometrata.
    """
    return [list(originale) for _ in range(quante)]


if __name__ == "__main__":
    for nome in FAMIGLIE:
        print(nome, genera_famiglia(nome, 8))
