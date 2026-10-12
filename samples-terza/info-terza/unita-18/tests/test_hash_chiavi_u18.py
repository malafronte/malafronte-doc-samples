"""Prove su hash didattico, indici e distribuzione — Unità 18.

Casi del piano §§5.1, 5.3 e 5.4: interi positivi e negativi, codici testuali
canonici, traccia dell'accumulatore, famiglie con lo stesso indice e riepilogo
della distribuzione.
"""

import pytest

from hash_chiavi_u18 import (
    famiglia_stesso_indice,
    indice_per,
    riepilogo_distribuzione,
    traccia_accumulatore,
)
from tabella_hash_u18 import hash_didattico


def test_hash_interi_restituisce_intero():
    assert hash_didattico(12) == 12
    assert hash_didattico(0) == 0
    assert hash_didattico(-3) == -3


def test_hash_rifiuta_tipi_fuori_dominio():
    for chiave in (True, 1.5, None, (1, 2), ["a"]):
        with pytest.raises(TypeError):
            hash_didattico(chiave)


def test_indici_interi_positivi_e_negativi():
    assert indice_per(12, 5) == 2
    assert indice_per(7, 5) == 2
    assert indice_per(-3, 5) == 2
    for chiave in (12, 7, 22, 17, 3, 8, -3, -8):
        assert 0 <= indice_per(chiave, 5) < 5
        assert 0 <= indice_per(chiave, 10) < 10


def test_hash_e_indici_dei_codici_canonici():
    attesi = {"007": (47671, 1), "012": (47697, 2), "003": (47667, 2), "017": (47702, 2)}
    for codice, (hash_atteso, indice_atteso) in attesi.items():
        assert hash_didattico(codice) == hash_atteso
        assert indice_per(codice, 5) == indice_atteso
    assert (hash_didattico("7"), indice_per("7", 5)) == (55, 0)
    assert (hash_didattico(""), indice_per("", 5)) == (0, 0)


def test_traccia_accumulatore_007():
    passi = traccia_accumulatore("007")
    assert [carattere for carattere, _punto, _h in passi] == ["0", "0", "7"]
    assert passi[0][1] == ord("0") == 48
    assert passi[-1][2] == 47671
    assert traccia_accumulatore("") == []


def test_collisione_di_indice_con_hash_diversi():
    assert hash_didattico(12) != hash_didattico(7)
    assert indice_per(12, 5) == indice_per(7, 5) == 2


def test_capacita_non_valida():
    with pytest.raises(ValueError):
        indice_per(3, 0)
    with pytest.raises(TypeError):
        indice_per(3, "5")


def test_famiglia_stesso_indice():
    famiglia = famiglia_stesso_indice(5, 2, 4)
    assert famiglia == [2, 7, 12, 17]
    for chiave in famiglia:
        assert indice_per(chiave, 5) == 2
    assert famiglia_stesso_indice(5, 2, 0) == []
    with pytest.raises(ValueError):
        famiglia_stesso_indice(5, 5, 2)
    with pytest.raises(ValueError):
        famiglia_stesso_indice(5, 2, -1)


def test_riepilogo_distribuzione_concentrata():
    riepilogo = riepilogo_distribuzione([0, 0, 4, 0, 0])
    assert riepilogo["n"] == 4
    assert riepilogo["m"] == 5
    assert riepilogo["carico"] == pytest.approx(0.8)
    assert riepilogo["bucket_vuoti"] == 4
    assert riepilogo["lunghezza_massima"] == 4
    assert riepilogo["indici_massimo"] == [2]


def test_riepilogo_distribuzione_vuota():
    riepilogo = riepilogo_distribuzione([0, 0, 0])
    assert riepilogo["n"] == 0
    assert riepilogo["carico"] == 0
    assert riepilogo["lunghezza_massima"] == 0
    assert riepilogo["indici_massimo"] == [0, 1, 2]
