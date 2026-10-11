"""Indice di record con chiavi uniche costruito su un BST — Unità 17, cap. PY-33.

Il modulo definisce il record immutabile `Scheda` e le funzioni che
costruiscono e consultano un indice `AlberoBST` le cui chiavi coincidono
con `Scheda.codice`. La corrispondenza fra chiave dell'indice e campo
`codice` del record viene verificata alla costruzione.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from dataclasses import dataclass

from bst_u17 import AlberoBST


@dataclass(frozen=True)
class Scheda:
    """Record immutabile di una scheda tecnica sintetica.

    `codice` è un intero univoco e coincide con la chiave dell'indice;
    `titolo` è una stringa. L'immutabilità rende osservabile ogni
    sostituzione di un record: un record modificato è un record diverso.
    """

    codice: int
    titolo: str


def costruisci_indice(schede):
    """Restituisce un `AlberoBST` indicizzato per `Scheda.codice`.

    Un codice ripetuto nella sorgente solleva `ValueError` prima che
    l'indice completato venga restituito: la struttura non viene
    consegnata in stato parziale.
    """
    indice = AlberoBST()
    for scheda in schede:
        indice.inserisci(scheda.codice, scheda)
    return indice


def verifica_corrispondenza(indice):
    """Controlla che ogni chiave coincida con il `codice` del record.

    Restituisce `True` quando la corrispondenza vale per ogni voce;
    una discordanza solleva `AssertionError` con la chiave coinvolta.
    """
    for chiave, scheda in indice.voci_ordinate():
        assert chiave == scheda.codice, f"chiave {chiave} con record codice {scheda.codice}"
    return True


def schede_canoniche():
    """Restituisce le dieci schede sintetiche del capitolo.

    I titoli sono distinti e i codici coincidono con le chiavi del
    dataset D1, così le tracce del capitolo restano confrontabili.
    """
    titoli = {
        40: "indice generale",
        20: "sezione sinistra",
        60: "sezione destra",
        10: "voce minima",
        30: "voce intermedia",
        50: "successore della radice",
        70: "voce massima",
        25: "sottovoce di 30",
        35: "sottovoce di 30",
        55: "sottovoce di 50",
    }
    return [Scheda(codice, titolo) for codice, titolo in titoli.items()]
