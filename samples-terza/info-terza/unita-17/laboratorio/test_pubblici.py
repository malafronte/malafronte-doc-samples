"""Casi pubblici LAB17-01…LAB17-12 del laboratorio LAB-PY-U17.

La suite è separata da quella degli esempi completi. All'inizio del
lavoro i test che coinvolgono i metodi `TODO` falliscono con
`NotImplementedError`: gli errori attesi sono descritti nella pagina del
laboratorio e scompaiono con il completamento delle fasi.
"""

from __future__ import annotations

import pytest
from dati_schede import Scheda, schede_canoniche, schede_con_duplicato

from indice_bst_starter import IndiceSchede


def indice_canonico():
    indice = IndiceSchede()
    indice.costruisci(schede_canoniche())
    return indice


# --- L1/L2: modello, previsioni e operazioni iniziali -------------------
def test_lab17_01_vuoto_e_nodo_unico():
    indice = IndiceSchede()
    assert indice.vuoto() is True
    assert len(indice) == 0
    assert indice.codici_ordinati() == []
    indice.costruisci([Scheda(40, "unico", "archivio")])
    assert len(indice) == 1
    assert indice.codici_ordinati() == [40]
    assert indice.record(40).titolo == "unico"
    assert indice.rimuovi(40) is True
    assert indice.vuoto() is True


def test_lab17_02_ricerca_e_valori_falsi():
    indice = IndiceSchede()
    indice.costruisci(schede_canoniche())
    assert indice.record(35).titolo == "sottovoce di 30"
    with pytest.raises(KeyError):
        indice.record(52)
    # Anche un record con campi vuoti resta un dato valido.
    indice.costruisci([Scheda(1, "", "vuoto")])
    assert indice.record(1) == Scheda(1, "", "vuoto")


def test_lab17_03_inserimento_e_duplicato():
    indice = IndiceSchede()
    indice.costruisci(schede_canoniche())
    assert len(indice) == 10
    stato_prima = indice.voci_ordinate()
    with pytest.raises(ValueError):
        indice.costruisci(schede_con_duplicato())
    assert indice.voci_ordinate() == stato_prima


def test_lab17_04_aggiornamento_e_dominio():
    indice = indice_canonico()
    # La sostituzione del record di una chiave esistente non fa crescere.
    indice.costruisci([Scheda(c, t, "aggiornato") for c, t, s in schede_canoniche()])
    assert len(indice) == 10
    with pytest.raises(TypeError):
        indice.contiene("30")
    with pytest.raises(KeyError):
        indice.record(999)


# --- L3: cancellazione guidata -----------------------------------------
def test_lab17_05_cancellazione_foglia():
    indice = indice_canonico()
    assert indice.rimuovi(10) is True
    assert len(indice) == 9
    assert indice.codici_ordinati() == [20, 25, 30, 35, 40, 50, 55, 60, 70]


def test_lab17_06_un_figlio_e_radice():
    indice = indice_canonico()
    assert indice.rimuovi(50) is True
    assert [codice for codice, _ in indice.intervallo(50, 60)] == [55, 60]
    piccolo = IndiceSchede()
    piccolo.costruisci([Scheda(40, "radice", "a"), Scheda(20, "sinistro", "a")])
    assert piccolo.rimuovi(40) is True
    assert piccolo.codici_ordinati() == [20]


def test_lab17_07_cancellazione_con_due_figli():
    indice = indice_canonico()
    assert indice.rimuovi(40) is True
    assert len(indice) == 9
    assert indice.codici_ordinati() == [10, 20, 25, 30, 35, 50, 55, 60, 70]
    assert indice.record(50).codice == 50
    assert indice.record(55).titolo == "sottovoce di 50"


def test_lab17_08_successore_immediato_e_ritorno_al_vuoto():
    indice = IndiceSchede()
    indice.costruisci(
        [Scheda(40, "a", "x"), Scheda(20, "b", "x"), Scheda(60, "c", "x"), Scheda(70, "d", "x")]
    )
    assert indice.rimuovi(40) is True
    assert indice.codici_ordinati() == [20, 60, 70]
    for codice in [20, 60, 70]:
        assert indice.rimuovi(codice) is True
    assert indice.vuoto() is True
    indice.costruisci([Scheda(30, "nuova", "x")])
    assert indice.codici_ordinati() == [30]


# --- L4: query e invarianti --------------------------------------------
def test_lab17_09_invarianti():
    indice = indice_canonico()
    indice.controlla_invarianti()
    indice.rimuovi(40)
    indice.controlla_invarianti()


def test_lab17_10_intervalli():
    indice = indice_canonico()
    assert [codice for codice, _ in indice.intervallo(25, 55)] == [25, 30, 35, 40, 50, 55]
    assert indice.intervallo(35, 35) == [(35, indice.record(35))]
    assert indice.intervallo(36, 39) == []
    assert IndiceSchede().intervallo(0, 100) == []
    with pytest.raises(ValueError):
        indice.intervallo(55, 25)


# --- L5: costi e scelta -------------------------------------------------
def test_lab17_11_degenerazione():
    from confronto_altezze_u17 import misura_costruzione, misura_ricerca

    bilineare, costruzione_b, altezza_b = misura_costruzione([4, 2, 6, 1, 3, 5, 7])
    catena, costruzione_c, altezza_c = misura_costruzione([1, 2, 3, 4, 5, 6, 7])
    assert (altezza_b, costruzione_b) == (2, 10)
    assert (altezza_c, costruzione_c) == (6, 21)
    assert misura_ricerca(bilineare, 7) == 3
    assert misura_ricerca(catena, 7) == 7


def test_lab17_12_associazione_e_conservazione():
    indice = indice_canonico()
    attesi = {codice: record for codice, record in indice.voci_ordinate()}
    indice.rimuovi(40)
    for codice, record in indice.voci_ordinate():
        assert record == attesi[codice]
    assert indice.codici_ordinati() == [c for c, _ in indice.voci_ordinate()]
