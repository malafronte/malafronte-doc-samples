"""Dati del catalogo dei materiali — laboratorio LAB-PY-U19.

Il modulo espone le voci canoniche D6 del laboratorio: otto materiali con
codice testuale univoco, descrizione e quantità non negativa. I codici
`"007"` e `"7"` sono chiavi distinte; la quantità `0` è un valore legittimo.
La sequenza restituita è una nuova lista a ogni chiamata, così le costruzioni
degli indici non condividono la raccolta principale.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations


def voci_canoniche():
    """Restituisce gli otto record D6 come `(codice, descrizione, quantita)`."""
    return [
        ("007", "cavetto USB", 4),
        ("012", "tastiera", 2),
        ("003", "mouse", 6),
        ("017", "webcam", 1),
        ("021", "adattatore", 3),
        ("034", "microfono", 2),
        ("7", "supporto", 5),
        ("042", "cuffie", 4),
    ]


def coppie_indice():
    """Restituisce le coppie `(codice, record)` pronte per l'indice B-tree."""
    return [
        (codice, (codice, descrizione, quantita))
        for codice, descrizione, quantita in voci_canoniche()
    ]


def query_laboratorio():
    """Restituisce le query del laboratorio: esatte riuscite e fallite."""
    return {"riuscite": ["007", "021", "042"], "fallite": ["000", "999", "014"]}
