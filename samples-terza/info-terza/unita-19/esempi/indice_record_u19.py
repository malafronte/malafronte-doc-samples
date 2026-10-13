"""Indice ordinato di record con B-tree — Unità 19 (cap. PY-35, sez. J).

Il modulo costruisce l'indice dei materiali D6 con il costruttore di
riferimento: il codice è una stringa univoca, la quantità un intero non
negativo, l'ordine delle chiavi è lessicografico. La ricerca esatta del codice
restituisce il record intero; la vista ordinata comprende le voci dei nodi
interni del B-tree; l'intervallo chiuso filtra la visita ordinata completa,
con costo `O(n)` dichiarato. Un intervallo con limite inferiore maggiore del
superiore solleva `ValueError`; un intervallo valido privo di chiavi
restituisce una lista vuota.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from btree_costruzione_u19 import costruisci_btree_riferimento
from dati_btree_u19 import RECORD_D6


def valida_record(record):
    """Convalida il record `(codice, descrizione, quantita)` del catalogo.

    Il codice è una stringa non vuota, la descrizione una stringa, la quantità
    un intero esatto non negativo. Un record fuori dominio solleva
    `ValueError`; il dato `0` è una quantità legittima.
    """
    codice, descrizione, quantita = record
    if type(codice) is not str or not codice:
        raise ValueError(f"codice testuale non vuoto atteso, ricevuto {codice!r}")
    if type(descrizione) is not str:
        raise ValueError(f"descrizione testuale attesa, ricevuto {descrizione!r}")
    if type(quantita) is not int or isinstance(quantita, bool) or quantita < 0:
        raise ValueError(f"quantità intera non negativa attesa, ricevuto {quantita!r}")


def costruisci_indice_record(record=RECORD_D6):
    """Costruisce l'indice B-tree dei record con chiavi i codici testuali.

    La funzione convalida ogni record, rifiuta i codici duplicati con
    `ValueError` prima di esporre l'indice e conserva la sequenza sorgente. Il
    B-tree restituito ha grado minimo 2 e chiavi di tipo `str`.
    """
    for elemento in record:
        valida_record(elemento)
    voci = [(codice, (codice, descrizione, quantita)) for codice, descrizione, quantita in record]
    return costruisci_btree_riferimento(voci, grado_minimo=2, tipo_chiave=str)


def intervallo_chiuso(indice, primo, ultimo):
    """Restituisce i record con codice fra `primo` e `ultimo` estremi inclusi.

    La funzione filtra la visita ordinata completa dell'indice B-tree e
    restituisce le coppie in ordine crescente di codice. Un intervallo con il
    limite inferiore maggiore del superiore solleva `ValueError`, secondo il
    contratto dichiarato nel capitolo e condiviso con soluzioni e adattatori.
    """
    if primo > ultimo:
        raise ValueError(f"intervallo invertito: {primo!r} maggiore di {ultimo!r}")
    return [(chiave, dato) for chiave, dato in indice.voci_ordinate() if primo <= chiave <= ultimo]
