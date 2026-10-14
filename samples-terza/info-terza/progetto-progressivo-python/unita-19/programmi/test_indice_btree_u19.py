"""Suite dell'indice B-tree di consultazione e del confronto (tappa U19).

Casi pubblici PU19-01–PU19-10 verificabili sul dominio, tre casi propri
motivati — un confine degli zeri significativi, un difetto plausibile
confrontato con un oracolo `dict` e una prova del ciclo di vita della
fotografia — e la regressione dei contratti mantenuti. I test usano
soltanto dati sintetici; per la regressione di persistenza usano file
temporanei e la regressione completa PU19-10 si verifica con la suite
cumulativa U5–U19.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_indice_btree_u19.py
"""

import pytest

import confronto_cli_u19
from coda_richieste_u16 import (
    CodaDequeU16,
    RichiestaConsultazione,
    ServizioConsultazione,
)
from confronto_cli_u19 import costruisci_tutti, esegui_confronta
from indice_bst_u17 import costruisci_indice as costruisci_bst
from indice_btree_u19 import costruisci_indice
from indice_hash_u18 import costruisci_indice as costruisci_hash
from registro_consultazione_u15 import PoliticaSoglia
from registro_dominio import formatta_euro
from registro_modello_u14 import Preventivo, RegistroPreventivi
from registro_persistenza import carica_archivio, salva_archivio
from spedizione_u5 import totale_spedizione


def raccolta_canonica():
    """Registro di riferimento U19: 007/locale/450, 012/nazionale/0, 003/locale/1200."""
    registro = RegistroPreventivi()
    registro.inserisci("007", "locale", 450)
    registro.inserisci("012", "nazionale", 0)
    registro.inserisci("003", "locale", 1200)
    return registro


def preventivo_sintetico(codice):
    """Record sintetico distinto: destinazione fissa e totale derivato dal codice."""
    cifre = "".join(carattere for carattere in codice if carattere.isdigit())
    return Preventivo(codice, "locale", int(cifre or "0") * 100)


def indice_su_codici(codici):
    """Indice B-tree costruito sui record sintetici dei codici indicati."""
    return costruisci_indice([preventivo_sintetico(codice) for codice in codici])


# --- Casi pubblici PU19-01 - PU19-10 ---


def test_pu19_01_registro_vuoto():
    registro = RegistroPreventivi()
    indice = costruisci_indice(registro.preventivi())
    assert len(indice) == 0
    assert indice.fotografia_ordinata() == []
    assert indice.intervallo("003", "012") == []
    with pytest.raises(KeyError):
        indice.cerca("007")
    assert indice.contiene("007") is False
    indice.controlla_invarianti()


def test_pu19_02_stessi_record():
    registro = raccolta_canonica()
    indice = costruisci_indice(registro.preventivi())
    for codice, destinazione, totale in (
        ("007", "locale", 450),
        ("012", "nazionale", 0),
        ("003", "locale", 1200),
    ):
        trovato = indice.cerca(codice)
        assert (trovato.codice, trovato.destinazione, trovato.totale_cent) == (
            codice,
            destinazione,
            totale,
        )
    assert indice.cerca("007") == registro.per_codice("007")


def test_pu19_03_zeri_significativi():
    indice = indice_su_codici(["007", "7"])
    assert indice.cerca("007").codice == "007"
    assert indice.cerca("7").codice == "7"
    assert len(indice) == 2
    indice.controlla_invarianti()


def test_pu19_04_duplicato_sorgente():
    registro = raccolta_canonica()
    duplicati = list(registro.preventivi()) + [Preventivo("007", "locale", 999)]
    with pytest.raises(ValueError):
        costruisci_indice(duplicati)
    assert [p.codice for p in registro.preventivi()] == ["007", "012", "003"]


def test_pu19_05_assenze():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    for codice in ("000", "999", "014"):
        with pytest.raises(KeyError):
            indice.cerca(codice)
        assert indice.contiene(codice) is False
    with pytest.raises(ValueError):
        indice.intervallo("012", "003")


def test_pu19_06_ordine_e_intervallo():
    registro = raccolta_canonica()
    indice = costruisci_indice(registro.preventivi())
    assert [c for c, _r in indice.fotografia_ordinata()] == ["003", "007", "012"]
    assert [c for c, _r in indice.intervallo("003", "012")] == ["003", "007", "012"]
    assert [c for c, _r in indice.intervallo("007", "007")] == ["007"]
    assert indice.intervallo("030", "031") == []


def test_pu19_07_voce_interna_e_split():
    codici = ["007", "012", "003", "017", "021", "034", "042", "009"]
    indice = indice_su_codici(codici)
    assert len(indice) == 8
    assert indice.altezza >= 1
    for codice in codici:
        assert indice.cerca(codice).codice == codice
    strumento = indice.ricerca_con_conteggi("007")
    assert strumento["trovato"] is True
    assert strumento["nodi"] >= 1
    indice.controlla_invarianti()


def test_pu19_08_fotografia_e_ricostruzione():
    registro = raccolta_canonica()
    vecchia = costruisci_indice(registro.preventivi())
    registro.inserisci("021", "nazionale", 300)
    nuova = costruisci_indice(registro.preventivi())
    assert vecchia.contiene("021") is False
    assert nuova.cerca("021").totale_cent == 300
    assert vecchia.cerca("007").totale_cent == 450
    assert [c for c, _r in nuova.fotografia_ordinata()] == ["003", "007", "012", "021"]


def test_pu19_09_costi_distinti(tmp_path, monkeypatch):
    registro = raccolta_canonica()
    preparazione = []
    indici = costruisci_tutti(registro.preventivi(), preparazione)
    monkeypatch.setattr(confronto_cli_u19, "PERCORSO_CSV", tmp_path / "confronto.csv")
    righe, coerente = esegui_confronta(indici, preparazione)
    assert coerente is True
    assert len(righe) == 5 + 5 * 4
    assert sum(riga["fase"] == "preparazione" for riga in righe) == 5
    assert all(riga["tempo_s"] >= 0 for riga in preparazione)
    for riga in righe:
        assert set(riga) == set(confronto_cli_u19.COLONNE_CSV)
        assert riga["modello"] and riga["cache"]
        if riga["fase"] == "query" and riga["query"].startswith("cerca"):
            if riga["struttura"] == "b-tree":
                assert riga["nodi"] >= 1 and riga["confronti"] >= 1
                assert riga["blocchi"] == riga["nodi"]
            if riga["struttura"] == "bst":
                assert riga["confronti"] == "" and riga["blocchi"] == riga["nodi"]


def test_pu19_10_persistenza_e_regressione(tmp_path):
    registro = raccolta_canonica()
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, registro.per_lista()) is True
    caricato, esito, dettaglio = carica_archivio(archivio)
    assert esito == ""
    assert dettaglio == ""
    registro2 = RegistroPreventivi()
    registro2.sostituisci_da_lista(caricato)
    indice = costruisci_indice(registro2.preventivi())
    assert [c for c, _r in indice.fotografia_ordinata()] == ["003", "007", "012"]
    assert indice.cerca("007").totale_cent == 450
    assert totale_spedizione(500, "nazionale", "s") == 9
    assert formatta_euro(1200) == "12,00"
    servizio = ServizioConsultazione(CodaDequeU16())
    servizio.accoda_richiesta(RichiestaConsultazione("R01", PoliticaSoglia(500)))
    esiti = servizio.elabora_tutte(raccolta_canonica())
    assert [e.codice for e in esiti] == ["R01"]
    indice_bst = costruisci_bst(registro.preventivi())
    indice_hash = costruisci_hash(registro.preventivi())
    for codice in ("007", "012", "003"):
        assert (
            indice.cerca(codice)
            == indice_bst.cerca(codice)
            == indice_hash.cerca(codice)
        )


# --- Tre casi propri motivati ---


def test_pu19_proprio_01_confine_007_e_7_con_intervallo():
    indice = indice_su_codici(["007", "7", "012"])
    assert [c for c, _r in indice.intervallo("007", "7")] == ["007", "012", "7"]
    assert indice.cerca("007") != indice.cerca("7")


def test_pu19_proprio_02_oracolo_dict_su_sequenza():
    codici = ["012", "003", "017", "007", "021", "034"]
    indice = indice_su_codici(codici)
    oracolo = {c: preventivo_sintetico(c) for c in codici}
    assert len(indice) == len(oracolo)
    for codice, record in oracolo.items():
        assert indice.cerca(codice) == record
    assert [c for c, _r in indice.fotografia_ordinata()] == sorted(oracolo)
    indice.controlla_invarianti()


def test_pu19_proprio_03_fotografia_precedente():
    registro = raccolta_canonica()
    fotografia_vecchia = costruisci_indice(registro.preventivi())
    registro.aggiorna("007", "nazionale", 500)
    fotografia_nuova = costruisci_indice(registro.preventivi())
    assert fotografia_vecchia.cerca("007").totale_cent == 450
    assert fotografia_nuova.cerca("007").totale_cent == 500
