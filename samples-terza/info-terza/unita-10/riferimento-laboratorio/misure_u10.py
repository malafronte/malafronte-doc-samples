"""Riferimento del LAB-PY-U10: il protocollo di misura completo.

Controparte completa dello starter `misure_u10.py`. La regione cronometrata
contiene **soltanto** le chiamate all'algoritmo studiato: preparazione delle
copie, verifica del risultato e restituzione dei valori restano fuori.

Le durate riportate da un'esecuzione sono un **esempio** registrato in un
ambiente: una classe può ottenere numeri diversi conservando la correttezza del
metodo. Il confronto con il riferimento riguarda protocollo, confini del timer,
forma dei dati e proporzioni della conclusione, non l'uguaglianza dei numeri.
"""

import sys
import time

from dataset_u10 import copie_indipendenti


def misura_ordinamento(ordinamento, originale, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di una chiamata di `ordinamento`.

    `ordinamento` ordina una lista sul posto e restituisce `None`. `originale`
    non viene modificata. Il valore registrato è la durata media di una
    chiamata: `(fine - inizio) / chiamate_per_lotto`.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    campioni = []
    for _ in range(ripetizioni):
        # Preparazione FUORI dalla regione cronometrata.
        copie = copie_indipendenti(originale, chiamate_per_lotto)

        inizio = time.perf_counter()
        for copia in copie:
            ordinamento(copia)
        fine = time.perf_counter()

        # Verifica del risultato FUORI dalla regione cronometrata.
        atteso = sorted(originale)
        for copia in copie:
            if copia != atteso:
                raise AssertionError("l'ordinamento ha prodotto un risultato diverso da sorted")

        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def sintesi_campioni(campioni):
    """Restituisce la sintesi descrittiva: numero, minimo, mediana, massimo.

    Per `m` dispari la mediana è il valore centrale; per `m` pari è la media dei
    due centrali. È una scelta descrittiva, non una stima del «vero tempo».
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
    import dataset_u10 as dati
    import ordinamenti_u10 as ordi

    originale = dati.genera_famiglia("inverso", 200)
    campioni = misura_ordinamento(ordi.bubble_sort_ottimizzato, originale, ripetizioni=5)
    print(riga_tabella("bubble_sort_ottimizzato", "inverso", 200, sintesi_campioni(campioni)))
    print(metadati_misura())
