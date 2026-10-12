"""Indice hash di record con codici testuali — Unità 18.

Il modulo costruisce un indice di consultazione per codice sopra la tabella
concatenata del capitolo: il costruttore riceve una raccolta di record,
valida i codici secondo il dominio applicativo, verifica l'unicità e produce
un indice completo. I duplicati sono un errore del dataset: la costruzione
pubblica consegna la struttura soltanto dopo il successo e la raccolta
sorgente resta conservata.

Il record sintetico ha codice testuale, descrizione e quantità; i codici
conservano gli zeri significativi perché restano stringhe. Le query
preservano la raccolta principale e la fotografia ordinata serve alla
presentazione, non alla ricerca.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from dataclasses import dataclass

from tabella_hash_u18 import TabellaHashConcatenata


@dataclass(frozen=True)
class RecordMateriale:
    """Valore immutabile di un materiale: codice, descrizione e quantità.

    Il codice è una stringa non vuota: gli zeri iniziali sono significativi e
    la conversione in intero appartiene alle scelte di dominio, non alla
    rappresentazione. La quantità è un intero non negativo; i booleani non
    sono interi del dominio.
    """

    codice: str
    descrizione: str
    quantita: int

    def __post_init__(self):
        valida_codice(self.codice)
        if type(self.descrizione) is not str:
            raise TypeError("descrizione attesa di tipo str")
        if isinstance(self.quantita, bool) or not isinstance(self.quantita, int):
            raise TypeError("quantità attesa di tipo int")
        if self.quantita < 0:
            raise ValueError("quantità minima 0")


def valida_codice(codice):
    """Convalida il codice del dominio applicativo e non restituisce nulla.

    La tabella generale ammette anche la stringa vuota; il costruttore
    dell'indice richiede invece un codice testuale non vuoto. Un tipo diverso
    da `str` solleva `TypeError`, la stringa vuota solleva `ValueError`.
    """
    if type(codice) is not str:
        raise TypeError(f"codice atteso di tipo str, ricevuto {type(codice).__name__}")
    if codice == "":
        raise ValueError("codice non vuoto richiesto dal dominio applicativo")


def record_canonici():
    """Restituisce i quattro record canonici del capitolo.

    I codici `"012"`, `"003"` e `"017"` collidono nel bucket 2 con capacità 5;
    `"007"` seleziona il bucket 1. Valori e quantità sono distinguibili.
    """
    return [
        RecordMateriale("007", "cavetto USB", 4),
        RecordMateriale("012", "tastiera", 2),
        RecordMateriale("003", "mouse", 6),
        RecordMateriale("017", "webcam", 1),
    ]


def costruisci_indice(record, capacita=5):
    """Costruisce l'indice completo dai `record` e lo restituisce.

    Ogni record è un `RecordMateriale`; un tipo diverso solleva `TypeError`.
    Un codice ripetuto solleva `ValueError` senza consegnare una struttura
    parziale: la verifica precede la consegna e la raccolta sorgente resta
    conservata. La costruzione è un'operazione del contratto applicativo,
    distinta dalla semantica di aggiornamento di `assegna` della tabella.
    """
    elenco = list(record)
    for voce in elenco:
        if not isinstance(voce, RecordMateriale):
            raise TypeError("indice costruito su RecordMateriale")
    visti = set()
    for voce in elenco:
        if voce.codice in visti:
            raise ValueError(f"codice duplicato nel dataset: {voce.codice!r}")
        visti.add(voce.codice)
    indice = TabellaHashConcatenata(capacita)
    for voce in elenco:
        indice.assegna(voce.codice, voce)
    return indice


def consulta(indice, codice):
    """Restituisce il record associato a `codice` nell'indice.

    Il codice segue la validazione del dominio; il codice assente solleva
    `KeyError` senza confondersi con un valore valido.
    """
    valida_codice(codice)
    return indice.cerca(codice)


def fotografia(indice):
    """Restituisce le coppie `(codice, record)` ordinate per codice.

    La fotografia serve alla presentazione e al confronto con un `dict`
    nativo; la ricerca usa la tabella e non questa lista.
    """
    return sorted(indice.coppie(), key=lambda coppia: coppia[0])


def sostituisci_record(indice, codice, nuovo_record):
    """Sostituisce il record di `codice` e restituisce la nuova fotografia.

    Il nuovo record deve portare lo stesso codice; un codice diverso solleva
    `ValueError`. La raccolta principale resta una fotografia coerente dopo
    la sostituzione.
    """
    valida_codice(codice)
    if not isinstance(nuovo_record, RecordMateriale):
        raise TypeError("nuovo record atteso di tipo RecordMateriale")
    if nuovo_record.codice != codice:
        raise ValueError("il nuovo record deve conservare il codice consultato")
    indice.assegna(codice, nuovo_record)
    return fotografia(indice)
