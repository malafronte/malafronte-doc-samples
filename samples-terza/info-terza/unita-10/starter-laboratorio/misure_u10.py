"""Starter del LAB-PY-U10: il protocollo di misura (fase L6).

Il file è **incompleto, e lo dichiara**: la regione cronometrata di
`misura_ordinamento` è da completare nella fase L6 - Misure, dopo che la suite
è verde. Le funzioni di sintesi e di metadati sono fornite complete e si
verificano subito con campioni artificiali, **prima** di applicarle a durate
reali.

Regole del protocollo, già spiegate dal cap. PY-13, parte IV:

1. la correttezza si verifica **prima** di misurare;
2. la lista di lavoro è una copia separata dell'originale, preparata **fuori**
   dalla regione cronometrata;
3. la verifica del risultato e le stampe restano fuori dal timer;
4. si raccolgono più campioni e si conservano i valori grezzi;
5. la sintesi dichiarata è la mediana, con minimo e massimo accanto.

Il confine della regione cronometrata contiene **soltanto** le chiamate
all'algoritmo studiato. Se una forma di lotto include inevitabilmente un
overhead, il confine esatto va documentato e mantenuto identico per tutti gli
algoritmi confrontati.

Ambiente: CPython sul computer, sola libreria standard (`time`, `sys`).
"""

import sys
import time

from dataset_u10 import copie_indipendenti


def misura_ordinamento(ordinamento, originale, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di una chiamata di `ordinamento`.

    `ordinamento` è una funzione con il contratto degli ordinamenti didattici:
    ordina una lista sul posto e restituisce `None`. `originale` è la lista di
    riferimento e **non** viene modificata. `ripetizioni` è il numero di
    campioni raccolti; `chiamate_per_lotto` è quante copie indipendenti
    ordinare dentro un singolo campione, per le prove troppo brevi.

    Il valore registrato è la durata media di una chiamata:
    `(fine - inizio) / chiamate_per_lotto`.

    Da completare nella fase L6 - Misure: preparazione delle copie fuori dal
    timer, due letture di `time.perf_counter`, chiamate del lotto, verifica del
    risultato fuori dal timer, raccolta del campione.
    """
    raise NotImplementedError("fase L6: completare la regione cronometrata")


def sintesi_campioni(campioni):
    """Restituisce la sintesi descrittiva: numero, minimo, mediana, massimo.

    Per `m` dispari la mediana è il valore centrale; per `m` pari è la media dei
    due centrali, e la convenzione va dichiarata. È una **scelta descrittiva**,
    non una stima del «vero tempo»: il valore grezzo resta la prova principale.
    """
    if not campioni:
        raise ValueError("nessun campione da riassumere")
    ordinati = sorted(campioni)
    m = len(ordinati)
    meta = m // 2
    if m % 2 == 1:
        mediana = ordinati[meta]
    else:
        mediana = (ordinati[meta - 1] + ordinati[meta]) / 2
    return {
        "numero": m,
        "minimo": ordinati[0],
        "mediana": mediana,
        "massimo": ordinati[-1],
        "campioni": ordinati,
    }


def metadati_misura():
    """Restituisce i metadati da conservare accanto a ogni serie di campioni."""
    return {
        "timer": "time.perf_counter",
        "unita": "secondi per chiamata",
        "python": sys.version.split()[0],
        "piattaforma": sys.platform,
        "seme": 20260927,
    }


def riga_tabella(algoritmo, famiglia, n, sintesi):
    """Restituisce una riga di testo della tabella dei risultati."""
    return (
        f"{algoritmo:<28} {famiglia:<15} n={n:<7} "
        f"mediana={sintesi['mediana'] * 1000:10.4f} ms  "
        f"min={sintesi['minimo'] * 1000:10.4f} ms  "
        f"max={sintesi['massimo'] * 1000:10.4f} ms  "
        f"campioni={sintesi['numero']}"
    )


if __name__ == "__main__":
    print("Starter del LAB-PY-U10: la regione cronometrata è da completare in L6.")
