"""Regressioni del confronto, della cache e del prestito speculare U19."""

import pytest

import confronto_starter
from dati_catalogo import coppie_indice
from problemi_btree_u19 import conta_accessi_blocchi, traccia_speculare_d5
from ricerca_btree_starter import BTreeDidattico


@pytest.fixture
def ricerca_simulata(monkeypatch):
    """Simula esiti corretti con un oracolo, senza risolvere la ricerca L2."""
    oracolo = dict(coppie_indice())

    def cerca(self, chiave):
        return oracolo[chiave]

    monkeypatch.setattr(BTreeDidattico, "cerca", cerca)
    return cerca


def test_confronto_verifica_cerca_e_record_interi(ricerca_simulata, monkeypatch):
    def cerca_corrotto(self, chiave):
        codice, _descrizione, _quantita = ricerca_simulata(self, chiave)
        return codice, "descrizione errata", -999

    monkeypatch.setattr(BTreeDidattico, "cerca", cerca_corrotto)
    assert confronto_starter.esegui_confronto()["coerente"] is False


def test_confronto_rileva_assenza_errata(ricerca_simulata, monkeypatch):
    def sempre_assente(self, chiave):
        raise KeyError(chiave)

    monkeypatch.setattr(BTreeDidattico, "cerca", sempre_assente)
    assert confronto_starter.esegui_confronto()["coerente"] is False


def test_confronto_registra_tre_strutture(ricerca_simulata):
    rapporto = confronto_starter.esegui_confronto()
    assert rapporto["coerente"] is True
    assert {riga["struttura"] for riga in rapporto["righe"]} == {"lista", "b-tree", "dict"}


def test_confronto_rileva_strumentazione_incoerente(ricerca_simulata, monkeypatch):
    originale = BTreeDidattico.ricerca_con_conteggi

    def strumento_corrotto(self, chiave):
        esito = originale(self, chiave)
        if esito["trovato"]:
            esito["dato"] = (chiave, "dato alterato", -999)
        return esito

    monkeypatch.setattr(BTreeDidattico, "ricerca_con_conteggi", strumento_corrotto)
    assert confronto_starter.esegui_confronto()["coerente"] is False


def test_cache_conserva_query_ripetute():
    assert conta_accessi_blocchi([10, 10]) == [
        {"query": 10, "nodi": 3, "trasferimenti": 3},
        {"query": 10, "nodi": 3, "trasferimenti": 0},
    ]


def test_cache_fredda_e_radice_residente():
    assert conta_accessi_blocchi([], radice_residente=True) == []
    assert [riga["trasferimenti"] for riga in conta_accessi_blocchi([10, 4])] == [3, 0]
    assert [
        riga["trasferimenti"] for riga in conta_accessi_blocchi([10, 4], conserva_cache=False)
    ] == [3, 1]
    assert [
        riga["trasferimenti"] for riga in conta_accessi_blocchi([10, 4], radice_residente=True)
    ] == [2, 0]


def test_prestito_speculare_dal_destro_e_fixture_errata():
    esito = traccia_speculare_d5()
    albero = esito["albero"]
    assert esito["coerente"] is True
    assert albero.radice.chiavi() == [50]
    assert albero.radice.figli[0].figli[1].chiavi() == [45]
    assert albero.radice.figli[1].chiavi() == [60]
    assert albero.contiene(10) is False
    assert "figli" in esito["diagnosi"]
