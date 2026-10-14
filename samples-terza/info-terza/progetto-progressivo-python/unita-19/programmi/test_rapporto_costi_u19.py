"""Regressioni delle fasi e delle unità del rapporto comparativo U19."""

import csv

import confronto_cli_u19 as confronto
from test_indice_btree_u19 import raccolta_canonica


def test_csv_include_preparazione_e_metriche(tmp_path, monkeypatch):
    percorso = tmp_path / "rapporto.csv"
    monkeypatch.setattr(confronto, "PERCORSO_CSV", percorso)
    orologio = iter(range(10))
    monkeypatch.setattr(confronto.time, "perf_counter", lambda: next(orologio))
    preparazione = []
    indici = confronto.costruisci_tutti(raccolta_canonica().preventivi(), preparazione)
    righe, coerente = confronto.esegui_confronta(indici, preparazione)
    assert coerente is True
    assert [riga["tempo_s"] for riga in preparazione] == [1] * 5
    assert all(riga["tempo_s"] == "" for riga in righe if riga["fase"] == "query")
    with percorso.open(encoding="utf-8", newline="") as archivio:
        lettore = csv.DictReader(archivio)
        salvate = list(lettore)
        assert lettore.fieldnames == list(confronto.COLONNE_CSV)
    assert len(salvate) == 25
    assert {riga["fase"] for riga in salvate} == {"preparazione", "query"}


def test_blocchi_con_radice_residente(tmp_path, monkeypatch):
    monkeypatch.setattr(confronto, "PERCORSO_CSV", tmp_path / "rapporto.csv")
    indici = confronto.costruisci_tutti(raccolta_canonica().preventivi())
    righe, _coerente = confronto.esegui_confronta(indici, radice_residente=True)
    for riga in righe:
        if riga["nodi"] != "":
            assert riga["blocchi"] == max(0, riga["nodi"] - 1)
            assert "radice residente" in riga["cache"]


def test_rapporto_vuoto_e_metriche_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(confronto, "PERCORSO_CSV", tmp_path / "rapporto.csv")
    indici = confronto.costruisci_tutti([])
    righe, coerente = confronto.esegui_confronta(indici)
    assert coerente is True
    assert len(righe) == 25
    for riga in righe:
        if riga["fase"] == "preparazione":
            assert riga["esito"] == 0 and riga["tempo_s"] == ""
            assert "non misurata" in riga["modello"]
        elif riga["query"].startswith("cerca"):
            assert riga["esito"] == "assente"
            assert riga["confronti"] in (0, "")
            assert riga["nodi"] in (0, "")
            assert riga["blocchi"] in (0, "")


def test_conteggi_scansione_e_dicotomica():
    indici = confronto.costruisci_tutti(raccolta_canonica().preventivi())
    for codice, scansione, dicotomica in (("007", 1, 3), ("012", 2, 3), ("999", 3, 2)):
        metriche_scansione = confronto._metriche_ricerca(indici, "scansione", codice, False)
        metriche_dicotomica = confronto._metriche_ricerca(indici, "lista-ordinata", codice, False)
        assert metriche_scansione["confronti"] == scansione
        assert metriche_dicotomica["confronti"] == dicotomica
