"""Prove sui problemi classici risolti con visite di alberi — Unità 17, cap. PY-32.

Valutazione di espressioni con visita postordine, notazioni infissa,
prefissa e postfissa, ricerca di un file con visita preordine e uscita
anticipata, spazio occupato con accumulo postordine, su gerarchie
sintetiche con al massimo due voci per directory.
"""

import pytest

from alberi_binari_u17 import (
    Nodo,
    ampiezza,
    dimensione_totale,
    infissa,
    postordine,
    preordine,
    trova,
    valuta,
)


def albero_espressione():
    """L'espressione (3 + 4) * 5 come albero di operatori e operandi."""
    return Nodo("*", Nodo("+", Nodo(3), Nodo(4)), Nodo(5))


def gerarchia_doc():
    """Gerarchia sintetica: doc/ con foto/ [a.jpg, b.jpg] e leggi.txt."""
    foto = Nodo(("foto", None), Nodo(("a.jpg", 1200)), Nodo(("b.jpg", 800)))
    return Nodo(("doc", None), foto, Nodo(("leggi.txt", 300)))


def test_valuta_operazioni_e_operando_singolo():
    assert valuta(albero_espressione()) == 35
    assert valuta(Nodo(7)) == 7
    assert valuta(Nodo("-", Nodo(10), Nodo(4))) == 6


def test_valuta_casi_errati():
    with pytest.raises(ValueError):
        valuta(None)
    with pytest.raises(ValueError):
        valuta(Nodo(True))
    with pytest.raises(ValueError):
        valuta(Nodo("%", Nodo(3), Nodo(4)))
    with pytest.raises(ValueError):
        valuta(Nodo("+", Nodo(3)))


def test_notazioni_della_stessa_espressione():
    albero = albero_espressione()
    assert infissa(albero) == "((3 + 4) * 5)"
    assert infissa(Nodo(7)) == "7"
    with pytest.raises(ValueError):
        infissa(None)
    prefissa = " ".join(str(valore) for valore in preordine(albero))
    assert prefissa == "* + 3 4 5"
    postfissa = " ".join(str(valore) for valore in postordine(albero))
    assert postfissa == "3 4 + 5 *"


def test_trova_percorso_e_assenza():
    doc = gerarchia_doc()
    assert trova(doc, "b.jpg") == ["doc", "foto", "b.jpg"]
    assert trova(doc, "doc") == ["doc"]
    assert trova(doc, "assente.txt") is None
    assert trova(None, "b.jpg") is None


def test_dimensione_totale_somma_postordine():
    assert dimensione_totale(gerarchia_doc()) == 2300
    assert dimensione_totale(Nodo(("solo.txt", 45))) == 45
    assert dimensione_totale(None) == 0


def test_ampiezza_sulla_gerarchia():
    nomi = [nome for nome, _byte in ampiezza(gerarchia_doc())]
    assert nomi == ["doc", "foto", "leggi.txt", "a.jpg", "b.jpg"]
