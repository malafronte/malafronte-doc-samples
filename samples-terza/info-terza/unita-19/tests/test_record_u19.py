"""Prove dell'indice di record — Unità 19."""

import pytest

from dati_btree_u19 import CHIAVI_D6_ORDINATE, RECORD_D6
from indice_record_u19 import costruisci_indice_record, intervallo_chiuso, valida_record


def test_record_interi_e_ordine():
    """L'indice conserva record interi in ordine lessicografico."""
    indice = costruisci_indice_record()
    assert [chiave for chiave, _dato in indice.voci_ordinate()] == CHIAVI_D6_ORDINATE
    assert indice.cerca("007") == ("007", "cavetto USB", 4)


def test_zeri_significativi():
    """`"007"` e `"7"` sono chiavi distinte dell'indice."""
    indice = costruisci_indice_record()
    assert indice.cerca("007") != indice.cerca("7")
    assert indice.cerca("7") == ("7", "supporto", 5)


def test_quantita_zero():
    """La quantità `0` è un valore legittimo del record."""
    indice = costruisci_indice_record()
    assert indice.cerca("012")[2] == 2
    valida_record(("000", "prova", 0))


def test_intervallo_valido_e_vuoto():
    """L'intervallo `007..021` produce quattro codici; il vuoto una lista vuota."""
    indice = costruisci_indice_record()
    assert [c for c, _d in intervallo_chiuso(indice, "007", "021")] == ["007", "012", "017", "021"]
    assert intervallo_chiuso(indice, "030", "031") == []


def test_intervallo_invertito():
    """Un intervallo con limite inferiore maggiore solleva `ValueError`."""
    with pytest.raises(ValueError):
        intervallo_chiuso(costruisci_indice_record(), "021", "007")


def test_duplicati_e_sorgente():
    """I duplicati sono rifiutati prima della consegna; la sorgente è invariata."""
    record = list(RECORD_D6)
    duplicati = record + [("007", "duplicato", 1)]
    with pytest.raises(ValueError):
        costruisci_indice_record(duplicati)
    assert list(RECORD_D6) == record
