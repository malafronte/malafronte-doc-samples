"""Soluzioni formative degli esercizi di base — Unità 18.

Il modulo raccoglie i controlli eseguibili delle schede di base: stati attesi
delle tracce, diagnosi dei difetti con sintomo, causa, modifica minima e nuova
prova, suite discriminante di esempio e riferimenti per fotografia e indice.
Ogni funzione è verificata dalla suite `tests/test_soluzioni_u18.py`; i
ragionamenti completi restano nelle soluzioni guidate della raccolta.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from hash_chiavi_u18 import famiglia_stesso_indice, indice_per
from indice_record_u18 import RecordMateriale, costruisci_indice, fotografia
from tabella_hash_u18 import TabellaHashConcatenata


def stato_base():
    """Costruisce la tabella con le quattro associazioni canoniche."""
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(12, "A")
    tabella.assegna(7, "B")
    tabella.assegna(22, "C")
    tabella.assegna(17, "D")
    return tabella


def verifica_sequenza_base():
    """Verifica stati e conteggi della traccia base e li restituisce.

    La funzione controlla indici, catena del bucket 2, dimensione, carico ed
    esiti delle cinque ricerche canoniche; il dizionario riporta i valori
    osservati.
    """
    tabella = stato_base()
    tabella.assegna(7, "B2")
    ricerche = {}
    for query in (17, 7, 12, 27, 4):
        try:
            esito = tabella.cerca(query)
        except KeyError:
            esito = "KeyError"
        ricerche[query] = (esito, tabella.confronti_per(query))
    return {
        "indici": {chiave: indice_per(chiave, 5) for chiave in (12, 7, 22, 17)},
        "catena_bucket_2": tabella.coppie(),
        "dimensione": len(tabella),
        "carico": tabella.fattore_carico,
        "ricerche": ricerche,
    }


def verifica_crescita():
    """Verifica la crescita da cinque a dieci bucket e la restituisce."""
    tabella = TabellaHashConcatenata(5)
    for chiave in (12, 7, 22, 17, 3, 8):
        tabella.assegna(chiave, f"V{chiave}")
    return {
        "dimensione": len(tabella),
        "capacita": tabella.capacita,
        "carico": tabella.fattore_carico,
        "indici": {chiave: tabella._indice(chiave) for chiave in (12, 7, 22, 17, 3, 8)},
        "associazioni": sorted(tabella.coppie(), key=lambda coppia: repr(coppia[0])),
    }


def diagnosi_sovrascrittura():
    """Diagnosi E01: una sola coppia per bucket perde la chiave precedente."""
    bucket = {}
    bucket[12 % 5] = (12, "A")
    bucket[7 % 5] = (7, "B")
    sintomo = "cerca(12) solleva KeyError dopo l'inserimento di 7"
    causa = "la posizione conserva una sola coppia e la seconda scrittura la sostituisce"
    correzione = "ogni posizione conserva la testa di una catena di associazioni"
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(12, "A")
    tabella.assegna(7, "B")
    verificato = tabella.cerca(12) == "A" and tabella.cerca(7) == "B"
    return {"sintomo": sintomo, "causa": causa, "correzione": correzione, "verificato": verificato}


def diagnosi_dimensione_su_aggiornamento():
    """Diagnosi E02: la dimensione cresce anche durante un aggiornamento."""
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(7, "B")
    tabella.assegna(7, "B2")
    return {
        "sintomo": "len pari a 2 dopo due assegnamenti alla stessa chiave",
        "causa": "il contatore viene incrementato senza distinguere inserimento e aggiornamento",
        "correzione": "incrementare la dimensione soltanto per una chiave nuova",
        "verificato": len(tabella) == 1 and tabella.cerca(7) == "B2",
    }


def diagnosi_scansione_interrotta():
    """Diagnosi E03: la scansione si arresta prima della coda della catena."""
    tabella = stato_base()
    return {
        "sintomo": "cerca(12) fallisce mentre cerca(17) riesce nella stessa catena",
        "causa": "il ciclo esce dopo il primo nodo diverso dalla chiave richiesta",
        "correzione": "proseguire fino al nodo richiesto oppure fino al termine None",
        "verificato": tabella.cerca(12) == "A" and tabella.confronti_per(12) == 4,
    }


def diagnosi_crescita_con_indici_vecchi():
    """Diagnosi E04: la crescita conserva gli indici calcolati con la vecchia capacità."""
    tabella = TabellaHashConcatenata(5)
    for chiave in (12, 7, 22, 17, 3, 8):
        tabella.assegna(chiave, f"V{chiave}")
    return {
        "sintomo": "cerca(7) fallisce dopo la crescita anche se la chiave è presente",
        "causa": "i nodi restano nelle vecchie posizioni mentre la ricerca usa la nuova capacità",
        "correzione": "ricalcolare l'indice di ogni chiave con la nuova capacità e ricollocarla",
        "verificato": tabella.cerca(7) == "V7" and tabella._indice(7) == 7,
    }


def diagnosi_marcatore_mancante():
    """Diagnosi E05: la cancellazione rende vuota la posizione invece di marcarla."""
    from tracce_sondaggio_u18 import SondaggioLineare

    tabella = SondaggioLineare(7)
    tabella.inserisci(5, "E5")
    tabella.inserisci(12, "E12")
    tabella.inserisci(19, "E19")
    tabella.rimuovi(12)
    return {
        "sintomo": "cerca(19) fallisce dopo la rimozione di 12",
        "causa": "la posizione resa vuota interrompe il sondaggio prima di raggiungere 19",
        "correzione": "marcare la posizione come cancellata e attraversarla nelle ricerche",
        "verificato": tabella.cerca(19) == "E19",
    }


def suite_discriminante():
    """Restituisce una suite di esempio che distingue tre difetti plausibili.

    Ogni caso riporta il nome, la sequenza di operazioni, l'esito atteso e i
    difetti che l'esito rivelerebbe. La suite è un esempio motivato, non
    l'unica selezione ammessa per l'esercizio T06.
    """
    return [
        {
            "nome": "collisioni conservate",
            "operazioni": ["assegna(12, 'A')", "assegna(7, 'B')"],
            "atteso": "cerca(12) = 'A' e cerca(7) = 'B'",
            "difetti_rivelati": ["sovrascrittura per collisione (E01)"],
        },
        {
            "nome": "dimensione con aggiornamento",
            "operazioni": ["assegna(7, 'B')", "assegna(7, 'B2')"],
            "atteso": "len = 1 e cerca(7) = 'B2'",
            "difetti_rivelati": ["dimensione incrementata in aggiornamento (E02)"],
        },
        {
            "nome": "ricerca in coda e crescita",
            "operazioni": ["sequenza base", "assegna(3, 'E')", "assegna(8, 'F')"],
            "atteso": "cerca(12) = 'A', capacita = 10 e n = 6",
            "difetti_rivelati": ["scansione interrotta (E03)", "indici vecchi dopo crescita (E04)"],
        },
    ]


def fotografia_riferimento():
    """Restituisce la fotografia ordinata dell'indice canonico di record."""
    indice = costruisci_indice(
        [
            RecordMateriale("007", "cavetto USB", 4),
            RecordMateriale("012", "tastiera", 2),
            RecordMateriale("003", "mouse", 6),
            RecordMateriale("017", "webcam", 1),
        ],
        5,
    )
    return fotografia(indice)


def chiavi_stesso_indice_riferimento():
    """Restituisce la famiglia di riferimento con indice 2 e capacità 5."""
    return famiglia_stesso_indice(5, 2, 4)
