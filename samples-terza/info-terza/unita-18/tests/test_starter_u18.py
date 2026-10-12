"""Prove sulle operazioni già complete dello starter LAB-PY-U18.

Gli stati si costruiscono con nodi di prova, senza completare i metodi
assegnati allo studente. Il controllo distingue chiavi ripetute, collisioni
fra chiavi diverse e chiavi di tipo diverso con la stessa forma testuale.
"""

import pytest

from indice_hash_starter import TabellaHashConcatenata, _NodoHash


@pytest.mark.parametrize("chiave", [7, "007", ""])
def test_starter_rifiuta_chiavi_ripetute(chiave):
    tabella = TabellaHashConcatenata(5)
    posizione = tabella._indice(chiave)
    coda = _NodoHash(chiave, "primo valore")
    testa = _NodoHash(chiave, "secondo valore", coda)
    tabella._bucket[posizione] = testa
    tabella._dimensione = 2

    with pytest.raises(AssertionError, match="chiave ripetuta"):
        tabella.controlla_invarianti()


def test_starter_ammette_collisioni_fra_chiavi_distinte():
    tabella = TabellaHashConcatenata(5)
    tabella._bucket[2] = _NodoHash(7, "B", _NodoHash(12, "A"))
    tabella._dimensione = 2

    tabella.controlla_invarianti()


def test_starter_distingue_chiavi_intere_e_testuali():
    tabella = TabellaHashConcatenata(5)
    tabella._bucket[tabella._indice(7)] = _NodoHash(7, "intero")
    tabella._bucket[tabella._indice("7")] = _NodoHash("7", "stringa")
    tabella._dimensione = 2

    tabella.controlla_invarianti()
