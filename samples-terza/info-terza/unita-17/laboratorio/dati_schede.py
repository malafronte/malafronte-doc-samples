"""Schede tecniche sintetiche del laboratorio LAB-PY-U17 — Unità 17.

Il modulo definisce il record immutabile `Scheda` e i dataset sintetici
usati dal laboratorio. È già completo: il lavoro dello studente riguarda
i metodi dello starter `indice_bst_starter.py`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scheda:
    """Record immutabile di una scheda tecnica sintetica.

    `codice` è un intero univoco e coincide con la chiave dell'indice;
    `titolo` è una stringa non vuota; `settore` identifica l'ambito.
    """

    codice: int
    titolo: str
    settore: str


#: Codici di riferimento usati nei casi pubblici LAB17.
CODICI_CANONICI = (10, 20, 25, 30, 35, 40, 50, 55, 60, 70)


def schede_canoniche():
    """Restituisce le dieci schede sintetiche del laboratorio.

    L'ordine di restituzione è quello della raccolta, distinto
    dall'ordine crescente dei codici prodotto dall'indice.
    """
    voci = [
        (40, "indice generale", "archivio"),
        (20, "sezione sinistra", "archivio"),
        (60, "sezione destra", "archivio"),
        (10, "voce minima", "consultazione"),
        (30, "voce intermedia", "consultazione"),
        (50, "successore della radice", "consultazione"),
        (70, "voce massima", "consultazione"),
        (25, "sottovoce di 30", "dettaglio"),
        (35, "sottovoce di 30", "dettaglio"),
        (55, "sottovoce di 50", "dettaglio"),
    ]
    return [Scheda(codice, titolo, settore) for codice, titolo, settore in voci]


def schede_con_duplicato():
    """Restituisce una sorgente sintetica con un codice ripetuto.

    La sorgente serve al caso LAB17-03: la costruzione dell'indice deve
    rifiutare il duplicato senza consegnare una struttura parziale.
    """
    base = schede_canoniche()
    return base + [Scheda(30, "voce ripetuta", "dettaglio")]
