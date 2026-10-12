"""Dati del laboratorio LAB-PY-U18 — catalogo sintetico di materiali.

Il record `VoceCatalogo` ha codice testuale univoco, descrizione e quantità
non negativa. Le funzioni `voci_canoniche` e `voci_con_duplicato` restituiscono
i dataset del laboratorio; `carica_catalogo` rilegge gli stessi dati dal CSV,
così il caricamento resta fuori dai tempi di costruzione dell'indice secondo
la procedura dell'Unità 12.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VoceCatalogo:
    """Valore immutabile di una voce: codice, descrizione e quantità."""

    codice: str
    descrizione: str
    quantita: int

    def __post_init__(self):
        if type(self.codice) is not str or self.codice == "":
            raise ValueError("codice testuale non vuoto richiesto")
        if type(self.descrizione) is not str:
            raise TypeError("descrizione attesa di tipo str")
        if isinstance(self.quantita, bool) or not isinstance(self.quantita, int):
            raise TypeError("quantità attesa di tipo int")
        if self.quantita < 0:
            raise ValueError("quantità minima 0")


def voci_canoniche():
    """Restituisce le otto voci canoniche del catalogo di laboratorio."""
    return [
        VoceCatalogo("007", "cavetto USB", 4),
        VoceCatalogo("012", "tastiera", 2),
        VoceCatalogo("003", "mouse", 6),
        VoceCatalogo("017", "webcam", 1),
        VoceCatalogo("021", "cuffie", 3),
        VoceCatalogo("034", "hub USB", 2),
        VoceCatalogo("7", "etichetta singola", 9),
        VoceCatalogo("042", "webcam 4K", 0),
    ]


def voci_con_duplicato():
    """Restituisce il catalogo con un codice ripetuto per il caso LAB18-11."""
    return voci_canoniche() + [VoceCatalogo("007", "cavetto duplicato", 5)]


def _percorso_dati(nome):
    """Restituisce il percorso del CSV nella cartella `dati` del laboratorio."""
    return Path(__file__).parent / "dati" / nome


def carica_catalogo(nome="catalogo.csv"):
    """Carica le voci dal CSV e le restituisce come lista di `VoceCatalogo`."""
    voci = []
    with _percorso_dati(nome).open(encoding="utf-8", newline="") as archivio:
        for riga in csv.DictReader(archivio):
            voci.append(VoceCatalogo(riga["codice"], riga["descrizione"], int(riga["quantita"])))
    return voci
