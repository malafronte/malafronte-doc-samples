"""Casi pubblici LAB18-01…LAB18-14 del laboratorio LAB-PY-U18.

La suite è separata da quella degli esempi completi. All'inizio del lavoro i
test che coinvolgono i metodi `TODO` falliscono con `NotImplementedError`: gli
errori attesi sono descritti nella pagina del laboratorio e scompaiono con il
completamento delle fasi.
"""

from __future__ import annotations

import pytest

from dati_catalogo import carica_catalogo, voci_canoniche, voci_con_duplicato
from indice_hash_starter import IndiceMateriali, TabellaHashConcatenata
from simulazione_sondaggio import simulazione_lab13


def tabella_base():
    tabella = TabellaHashConcatenata(5)
    for chiave, valore in [(12, "A"), (7, "B"), (22, "C"), (17, "D")]:
        tabella.assegna(chiave, valore)
    return tabella


def indice_canonico():
    indice = IndiceMateriali()
    indice.costruisci(voci_canoniche())
    return indice


def test_lab18_01_tabella_vuota():
    tabella = TabellaHashConcatenata(5)
    assert len(tabella) == 0
    assert tabella.contiene(12) is False
    with pytest.raises(KeyError):
        tabella.cerca(12)
    with pytest.raises(KeyError):
        tabella.rimuovi(12)


def test_lab18_02_valore_none():
    tabella = TabellaHashConcatenata(5)
    tabella.assegna("042", None)
    assert tabella.contiene("042") is True
    assert tabella.cerca("042") is None


def test_lab18_03_catena_condivisa():
    tabella = tabella_base()
    assert len(tabella) == 4
    for chiave, valore in [(12, "A"), (7, "B"), (22, "C"), (17, "D")]:
        assert tabella.cerca(chiave) == valore


def test_lab18_04_aggiornamento():
    tabella = tabella_base()
    tabella.assegna(7, "B2")
    assert tabella.cerca(7) == "B2"
    assert len(tabella) == 4


def test_lab18_05_rimozione_testa():
    tabella = tabella_base()
    assert tabella.rimuovi(17) == "D"
    assert len(tabella) == 3
    assert tabella.cerca(22) == "C"


def test_lab18_06_rimozione_interna():
    tabella = tabella_base()
    assert tabella.rimuovi(22) == "C"
    assert tabella.cerca(17) == "D"
    assert tabella.cerca(7) == "B"


def test_lab18_07_rimozione_coda_e_unico():
    tabella = tabella_base()
    assert tabella.rimuovi(12) == "A"
    assert tabella.cerca(7) == "B"
    singola = TabellaHashConcatenata(5)
    singola.assegna(3, "solo")
    assert singola.rimuovi(3) == "solo"
    assert len(singola) == 0


def test_lab18_08_rimozione_assente():
    tabella = tabella_base()
    with pytest.raises(KeyError):
        tabella.rimuovi(27)
    assert len(tabella) == 4


def test_lab18_09_crescita():
    tabella = TabellaHashConcatenata(5)
    for chiave in (12, 7, 22, 17, 3, 8):
        tabella.assegna(chiave, f"V{chiave}")
    assert tabella.capacita == 10
    assert len(tabella) == 6
    assert tabella.fattore_carico == pytest.approx(0.6)
    for chiave in (12, 7, 22, 17, 3, 8):
        assert tabella.cerca(chiave) == f"V{chiave}"


def test_lab18_10_codici_con_zeri():
    indice = indice_canonico()
    assert indice.consulta("007").descrizione == "cavetto USB"
    assert indice.consulta("7").descrizione == "etichetta singola"
    assert indice.consulta("012").quantita == 2


def test_lab18_11_duplicato_rifiutato():
    indice = IndiceMateriali()
    with pytest.raises(ValueError):
        indice.costruisci(voci_con_duplicato())
    assert len(indice) == 0


def test_lab18_12_validazione():
    tabella = TabellaHashConcatenata(5)
    with pytest.raises(TypeError):
        tabella.assegna(True, "x")
    with pytest.raises(TypeError):
        tabella.cerca(1.5)
    with pytest.raises(ValueError):
        TabellaHashConcatenata(0)
    indice = IndiceMateriali()
    with pytest.raises(ValueError):
        indice.consulta("")
    with pytest.raises(TypeError):
        indice.consulta(7)


def test_lab18_13_simulazione_marcatore():
    esiti = simulazione_lab13()
    assert esiti["posizioni_iniziali"] == [0, 5, 6]
    assert esiti["valore_19_oltre_marcatore"] == "E19"
    assert esiti["valore_19_aggiornato"] == "E19b"
    assert esiti["posizione_riusata_26"][0] == "occupata"
    assert esiti["posizione_riusata_26"][1] == 26


def test_lab18_14_confronto_query():
    indice = indice_canonico()
    riferimento = {voce.codice: voce for voce in voci_canoniche()}
    for codice in ("007", "012", "042", "999"):
        trovata = True
        try:
            esito = indice.consulta(codice)
        except KeyError:
            trovata = False
            esito = None
        assert trovata == (codice in riferimento)
        if trovata:
            assert esito == riferimento[codice]
    assert len(carica_catalogo()) == 8
