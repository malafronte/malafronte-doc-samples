"""Dataset delle cinque famiglie dell'Unità 11 - **fornito completo**.

Questo modulo non contiene alcun corpo da completare: si usa nelle fasi L4 e L5
e riproduce **esattamente** la costruzione e il seme del `dataset_u10.py` del
LAB-PY-U10. La duplicazione è intenzionale: l'attività del LAB-PY-U11 resta
riproducibile anche senza aver svolto il laboratorio precedente e nessun file va
recuperato da altre cartelle per la parte essenziale.

Le **cinque famiglie** di input sono: `ordinato`, `inverso`, `quasi_ordinato`,
`molti_duplicati`, `pseudo_casuale`. La famiglia `quasi_ordinato` non è un nome
generico: viene costruita esattamente come dichiarato in `genera_famiglia`,
perché lo stesso nome può descrivere input diversi se non ne è specificata la
costruzione.

Ambiente: CPython sul computer, sola libreria standard (`random`). Il generatore
è deterministico: a parità di nome, dimensione e seme la lista è sempre la
stessa, quindi tutti gli algoritmi confrontati ricevono gli **stessi** dati.
"""

import random


FAMIGLIE = ("ordinato", "inverso", "quasi_ordinato", "molti_duplicati", "pseudo_casuale")

SEME = 20260927


def genera_famiglia(nome, n, seme=SEME):
    """Restituisce una lista di `n` interi della famiglia `nome`.

    Costruzione esatta delle cinque famiglie, con `n` numero di elementi:

    | `nome` | Costruzione |
    |---|---|
    | `ordinato` | `list(range(n))`, già in ordine crescente |
    | `inverso` | `list(range(n, 0, -1))`, ordine strettamente decrescente |
    | `quasi_ordinato` | `list(range(n))` con due scambi dichiarati: le posizioni `(0, 1)` e `(n // 2, n // 2 + 1)`; richiede `n >= 4`, altrimenti la lista resta ordinata e il caso è dichiarato |
    | `molti_duplicati` | `n` valori estratti con `random.Random(seme).randrange(3)`, quindi solo 0, 1 e 2 |
    | `pseudo_casuale` | `n` valori estratti con `random.Random(seme).randrange(n + 1)`, con il seme esplicito |

    Il seme è parte del protocollo: due esecuzioni con lo stesso seme producono
    gli stessi dati e le misure restano confrontabili.
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
    """Restituisce `quante` copie separate di `originale`, una per chiamata.

    Le copie si preparano **fuori** dalla regione cronometrata: ogni procedura
    riceve la propria lista e non modifica quella degli altri algoritmi.
    """
    return [list(originale) for _ in range(quante)]


if __name__ == "__main__":
    for nome in FAMIGLIE:
        print(f"{nome:<15} n=6 -> {genera_famiglia(nome, 6)}")
