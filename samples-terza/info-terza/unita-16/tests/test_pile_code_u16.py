"""Prove di contratto di pile e code - Unità 16 (PY-31).

Le stesse prove di contratto si applicano alle due pile e alle due code:
risultati, ordine, dimensione e stato dopo un errore. I casi specifici della
rappresentazione sono separati dalle prove comuni.
"""

from __future__ import annotations

import pytest

from pile_code_u16 import (
    CodaConcatenata,
    CodaDeque,
    PilaConcatenata,
    PilaLista,
    client_comune,
)

PILE = [PilaLista, PilaConcatenata]
CODE = [CodaDeque, CodaConcatenata]


@pytest.mark.parametrize("classe", PILE)
def test_pila_lifo_sulla_sequenza_a_b_c(classe):
    pila = classe()
    assert pila.vuota() is True
    for valore in ("A", "B", "C"):
        pila.inserisci(valore)
    assert len(pila) == 3
    assert pila.cima() == "C"  # osservare non modifica la pila
    assert len(pila) == 3
    assert [pila.estrai(), pila.estrai(), pila.estrai()] == ["C", "B", "A"]
    assert pila.vuota() is True
    assert len(pila) == 0


@pytest.mark.parametrize("classe", PILE)
def test_pila_vuota_solleva_e_conserva_lo_stato(classe):
    pila = classe()
    with pytest.raises(IndexError):
        pila.estrai()
    with pytest.raises(IndexError):
        pila.cima()
    assert pila.vuota() is True
    pila.inserisci("A")  # la struttura resta utilizzabile
    assert pila.estrai() == "A"


@pytest.mark.parametrize("classe", CODE)
def test_coda_fifo_sulla_sequenza_a_b_c(classe):
    coda = classe()
    assert coda.vuota() is True
    for valore in ("A", "B", "C"):
        coda.accoda(valore)
    assert len(coda) == 3
    assert coda.fronte() == "A"  # osservare non modifica la coda
    assert len(coda) == 3
    assert [coda.estrai(), coda.estrai(), coda.estrai()] == ["A", "B", "C"]
    assert coda.vuota() is True


@pytest.mark.parametrize("classe", CODE)
def test_coda_fifo_intercalata(classe):
    coda = classe()
    coda.accoda("A")
    coda.accoda("B")
    assert coda.estrai() == "A"
    coda.accoda("C")
    assert [coda.estrai(), coda.estrai()] == ["B", "C"]
    assert coda.vuota() is True


@pytest.mark.parametrize("classe", CODE)
def test_coda_vuota_solleva_e_conserva_lo_stato(classe):
    coda = classe()
    with pytest.raises(IndexError):
        coda.estrai()
    with pytest.raises(IndexError):
        coda.fronte()
    assert coda.vuota() is True
    coda.accoda("A")
    assert coda.fronte() == "A"
    assert len(coda) == 1


@pytest.mark.parametrize("classe", PILE)
def test_pila_con_valori_falsi_e_none(classe):
    pila = classe()
    for valore in (0, False, None):
        pila.inserisci(valore)
    assert pila.vuota() is False  # il vuoto si decide con vuota/len, non con il valore
    assert len(pila) == 3
    assert [pila.estrai(), pila.estrai(), pila.estrai()] == [None, False, 0]
    assert pila.vuota() is True


@pytest.mark.parametrize("classe", CODE)
def test_coda_con_valori_falsi_e_none(classe):
    coda = classe()
    for valore in (0, False, None):
        coda.accoda(valore)
    assert coda.vuota() is False
    assert len(coda) == 3
    assert [coda.estrai(), coda.estrai(), coda.estrai()] == [0, False, None]
    assert coda.vuota() is True


@pytest.mark.parametrize("classe", PILE)
def test_client_comune_con_due_pile_compatibili(classe):
    assert client_comune(classe(), ["A", "B", "C"]) == ["C", "B", "A"]


@pytest.mark.parametrize("classe", CODE)
def test_client_comune_con_due_code_compatibili(classe):
    assert client_comune(classe(), ["A", "B", "C"]) == ["A", "B", "C"]


def test_un_wrapper_fifo_che_estrae_dall_estremo_errato_non_e_fifo():
    """Un test con due elementi distingue LIFO e FIFO (difetto E04 della raccolta)."""

    class CodaErrata(PilaLista):
        """Wrapper difettoso: accoda con `append` ma estrae con `pop` da destra."""

        accoda = PilaLista.inserisci

    difettosa = CodaErrata()
    difettosa.accoda("A")
    difettosa.accoda("B")
    assert difettosa.estrai() == "B"  # ordine LIFO: il contratto FIFO è violato
