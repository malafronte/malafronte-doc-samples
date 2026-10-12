"""Confronto di strategie di ricerca sullo stesso carico — Unità 18.

Il modulo confronta la stessa operazione **codice → record** mediante
scansione lineare, ricerca dicotomica su copia ordinata, tabella hash
didattica e `dict` nativo di riferimento. Le misure contano confronti di
chiave, nodi visitati, accessi ai bucket o sonde secondo la strategia: le
metriche hanno unità diverse e la tabella dei risultati le dichiara. I tempi
hanno unità e protocollo separati: generazione, ordinamento di presentazione,
stampa e grafici restano fuori dalla regione misurata.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

import time

from tabella_hash_u18 import TabellaHashConcatenata


def ricerca_lineare(raccolta, chiave):
    """Cerca `chiave` nella sequenza e restituisce `(posizione, confronti)`.

    La posizione è l'indice della prima occorrenza oppure `None`; i confronti
    contano le uguaglianze fra chiavi esaminate.
    """
    confronti = 0
    for posizione, coppia in enumerate(raccolta):
        confronti += 1
        if coppia[0] == chiave:
            return posizione, confronti
    return None, confronti


def ricerca_dicotomica(ordinata, chiave):
    """Cerca `chiave` nella sequenza ordinata e restituisce `(posizione, confronti)`.

    La posizione è l'indice nell'ordinata oppure `None`; i confronti contano
    le uguaglianze e le scelte di metà intervallo seguono l'ordine delle
    chiavi. La preparazione dell'ordinata è un costo separato dalla ricerca.
    """
    confronti = 0
    basso, alto = 0, len(ordinata) - 1
    while basso <= alto:
        medio = (basso + alto) // 2
        confronti += 1
        if ordinata[medio][0] == chiave:
            return medio, confronti
        if ordinata[medio][0] < chiave:
            basso = medio + 1
        else:
            alto = medio - 1
    return None, confronti


def interroga_hash(tabella, chiave):
    """Interroga la tabella e restituisce `(trovato, confronti)`.

    Il risultato è `True` per la chiave presente e `False` per la chiave
    assente; i confronti sono quelli della catena selezionata.
    """
    confronti = tabella.confronti_per(chiave)
    return tabella.contiene(chiave), confronti


def costruisci_tabella(coppie, capacita=5):
    """Costruisce una tabella concatenata dalle `coppie` e la restituisce."""
    tabella = TabellaHashConcatenata(capacita)
    for chiave, valore in coppie:
        tabella.assegna(chiave, valore)
    return tabella


def confronta_strategie(coppie, queries, capacita=5):
    """Confronta le strategie sulle stesse query e restituisce le righe.

    Ogni riga riporta la strategia, la query, l'esito logico e i confronti
    con la propria unità: confronti di chiave per scansione e dicotomica,
    confronti nella catena per la tabella hash. La costruzione della tabella,
    l'ordinamento della copia e la costruzione del `dict` sono preparazione e
    non entrano nei conteggi delle query. Gli esiti logici delle strategie
    corrette coincidono sulle query ammesse.
    """
    ordinata = sorted(coppie, key=lambda coppia: coppia[0])
    tabella = costruisci_tabella(coppie, capacita)
    riferimento = dict(coppie)
    righe = []
    for chiave in queries:
        posizione, confronti = ricerca_lineare(coppie, chiave)
        righe.append(
            {
                "strategia": "scansione",
                "query": chiave,
                "trovato": posizione is not None,
                "confronti": confronti,
            }
        )
        posizione, confronti = ricerca_dicotomica(ordinata, chiave)
        righe.append(
            {
                "strategia": "dicotomica",
                "query": chiave,
                "trovato": posizione is not None,
                "confronti": confronti,
            }
        )
        trovato, confronti = interroga_hash(tabella, chiave)
        righe.append(
            {
                "strategia": "hash",
                "query": chiave,
                "trovato": trovato,
                "confronti": confronti,
            }
        )
        righe.append(
            {
                "strategia": "dict",
                "query": chiave,
                "trovato": chiave in riferimento,
                "confronti": None,
            }
        )
    return righe


def misura_secondi(funzione, ripetizioni=5):
    """Esegue `funzione` e restituisce `(ultimo_risultato, secondi_totali)`.

    La preparazione resta fuori dalla regione misurata: il chiamante costruisce
    i dati prima e passa una funzione senza argomenti. Ripetizioni e sintesi
    sono dichiarate dal chiamante; l'ambiente e le versioni appartengono al
    protocollo della relazione.
    """
    if isinstance(ripetizioni, bool) or not isinstance(ripetizioni, int) or ripetizioni < 1:
        raise ValueError("ripetizioni intere positive richieste")
    inizio = time.perf_counter()
    risultato = None
    for _contatore in range(ripetizioni):
        risultato = funzione()
    fine = time.perf_counter()
    return risultato, fine - inizio
