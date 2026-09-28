"""Riferimento del LAB-PY-U11: il protocollo di misura completato.

Controparte completa dello starter `misure_u11.py`, da leggere **dopo** le fasi
L5 e L7. Le due regioni cronometrate sono state completate rispettando il
confine dichiarato: preparazione delle copie, verifica e stampe restano fuori
dal timer.

Ambiente: CPython sul computer, sola libreria standard (`time`, `sys`).
"""

import sys
import time

from dataset_u11 import SEME, copie_indipendenti


def misura_ordinamento(procedura, originale, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di una chiamata di `procedura`.

    Contratto unico: `procedura` riceve una lista **nuova** e o la ordina sul
    posto restituendo `None`, oppure restituisce la lista ordinata senza
    modificare l'argomento. Il valore registrato è la durata media di una
    chiamata: `(fine - inizio) / chiamate_per_lotto`.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    atteso = sorted(originale)
    campioni = []
    for _ in range(ripetizioni):
        copie = copie_indipendenti(originale, chiamate_per_lotto)
        inizio = time.perf_counter()
        risultati = [procedura(copia) for copia in copie]
        fine = time.perf_counter()
        for copia, risultato in zip(copie, risultati):
            effettivo = copia if risultato is None else risultato
            if effettivo != atteso:
                raise AssertionError("la procedura ha prodotto un risultato diverso da sorted")
        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def misura_ricerca(ricerca, valori, bersaglio, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di `ricerca(valori, bersaglio)`.

    La ricerca non modifica l'argomento e non serve alcuna copia. La preparazione
    dell'ordine resta fuori da questa misura.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    campioni = []
    for _ in range(ripetizioni):
        inizio = time.perf_counter()
        risultati = [ricerca(valori, bersaglio) for _ in range(chiamate_per_lotto)]
        fine = time.perf_counter()
        atteso = valori.index(bersaglio) if bersaglio in valori else None
        for risultato in risultati:
            if risultato != atteso:
                raise AssertionError("la ricerca ha prodotto un risultato inatteso")
        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def misura_sequenza_ricerche(ricerca, valori, bersagli, ripetizioni=5):
    """Restituisce i campioni di durata, in secondi, di una **serie** di ricerche.

    Un campione registra la durata complessiva di `len(bersagli)` interrogazioni
    successive sulla **stessa** lista `valori`, che non viene modificata. Il
    valore registrato è quindi la durata **dell'intera serie**, non di una
    singola ricerca: la differenza va dichiarata quando si confrontano le righe
    della tabella.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if not bersagli:
        raise ValueError("serve almeno una interrogazione")

    campioni = []
    for _ in range(ripetizioni):
        inizio = time.perf_counter()
        risultati = [ricerca(valori, bersaglio) for bersaglio in bersagli]
        fine = time.perf_counter()
        attesi = [valori.index(bersaglio) if bersaglio in valori else None for bersaglio in bersagli]
        if risultati != attesi:
            raise AssertionError("la sequenza ha prodotto esiti inattesi")
        campioni.append(fine - inizio)
    return campioni


def sintesi_campioni(campioni):
    """Restituisce la sintesi descrittiva: numero, minimo, mediana, massimo."""
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
        "seme": SEME,
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
    from ordinamenti_u11 import merge_sort, quick_sort

    originale = [5, 2, 4, 2] * 10
    for nome, procedura in (("quick_sort", quick_sort), ("merge_sort", merge_sort)):
        campioni = misura_ordinamento(procedura, originale, ripetizioni=5)
        print(riga_tabella(nome, "molti_duplicati", len(originale), sintesi_campioni(campioni)))
    print("Metadati:", metadati_misura())
