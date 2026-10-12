"""Suite dell'indice hash di consultazione (tappa U18).

Casi pubblici PU18-01–PU18-12 verificabili sul dominio, tre casi propri
motivati — un confine degli zeri significativi, un difetto plausibile
confrontato con un oracolo `dict` e una prova del ciclo di vita della
fotografia — e la regressione dei contratti mantenuti. I test usano soltanto
dati sintetici; per la regressione di persistenza usano file temporanei e la
regressione completa PU18-11 si verifica con la suite cumulativa U5–U18.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_indice_hash_u18.py
"""

import pytest
from coda_richieste_u16 import (
    CodaDequeU16,
    RichiestaConsultazione,
    ServizioConsultazione,
)
from indice_bst_u17 import costruisci_indice as costruisci_bst
from indice_hash_u18 import (
    costruisci_indice,
    hash_didattico,
)
from registro_consultazione_u15 import PoliticaSoglia
from registro_dominio import formatta_euro
from registro_modello_u14 import Preventivo, RegistroPreventivi
from registro_persistenza import carica_archivio, salva_archivio
from spedizione_u5 import totale_spedizione


def raccolta_canonica():
    """Registro di riferimento U18: 007/locale/450, 012/nazionale/0, 003/locale/1200."""
    registro = RegistroPreventivi()
    registro.inserisci("007", "locale", 450)
    registro.inserisci("012", "nazionale", 0)
    registro.inserisci("003", "locale", 1200)
    return registro


def preventivo_sintetico(codice):
    """Record sintetico distinto: destinazione fissa e totale derivato dal codice."""
    cifre = "".join(carattere for carattere in codice if carattere.isdigit())
    return Preventivo(codice, "locale", int(cifre or "0") * 100)


def indice_su_codici(codici, capacita=5):
    """Indice costruito sui record sintetici dei codici indicati."""
    return costruisci_indice(
        [preventivo_sintetico(codice) for codice in codici], capacita
    )


# --- Casi pubblici PU18-01 - PU18-12 ---


def test_pu18_01_registro_vuoto():
    registro = RegistroPreventivi()
    indice = costruisci_indice(registro.preventivi())
    assert len(indice) == 0
    assert indice.fotografia_ordinata() == []
    with pytest.raises(KeyError):
        indice.cerca("007")
    assert indice.contiene("007") is False
    indice.controlla_invarianti()


def test_pu18_02_zeri_significativi():
    registro = raccolta_canonica()
    indice = costruisci_indice(registro.preventivi())
    trovato = indice.cerca("007")
    assert (trovato.codice, trovato.destinazione, trovato.totale_cent) == (
        "007",
        "locale",
        450,
    )
    assert hash_didattico("007") == 47671


def test_pu18_03_collisioni_distinte():
    indice = indice_su_codici(["012", "003", "017"])
    assert len(indice) == 3
    for codice in ("012", "003", "017"):
        assert indice.cerca(codice).codice == codice
    with pytest.raises(ValueError):
        indice.inserisci("012", preventivo_sintetico("012"))


def test_pu18_04_duplicato_rifiutato():
    registro = raccolta_canonica()
    duplicati = list(registro.preventivi()) + [Preventivo("007", "locale", 999)]
    with pytest.raises(ValueError):
        costruisci_indice(duplicati)
    assert [p.codice for p in registro.preventivi()] == ["007", "012", "003"]


def test_pu18_05_piu_query_stessa_fotografia():
    registro = raccolta_canonica()
    indice = costruisci_indice(registro.preventivi())
    assert indice.cerca("007").totale_cent == 450
    assert indice.cerca("012").totale_cent == 0
    assert indice.cerca("003").totale_cent == 1200
    assert [p.codice for p in registro.preventivi()] == ["007", "012", "003"]
    assert len(indice) == 3


def test_pu18_06_query_assente():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    with pytest.raises(KeyError):
        indice.cerca("999")
    assert indice.contiene("999") is False


def test_pu18_07_crescita_conserva_associazioni():
    codici = [f"C{i:03d}" for i in range(12)]
    indice = indice_su_codici(codici)
    assert len(indice) == 12
    assert indice.capacita == 20
    for codice in codici:
        assert indice.cerca(codice).codice == codice
    indice.controlla_invarianti()


def test_pu18_08_ricostruzione_dopo_modifica():
    registro = raccolta_canonica()
    vecchia = costruisci_indice(registro.preventivi())
    registro.inserisci("021", "nazionale", 300)
    nuova = costruisci_indice(registro.preventivi())
    assert vecchia.contiene("021") is False
    assert nuova.cerca("021").totale_cent == 300
    assert vecchia.cerca("007").totale_cent == 450


def test_pu18_09_persistenza_e_ricostruzione(tmp_path):
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


def test_pu18_10_stessi_record_fra_indici():
    registro = raccolta_canonica()
    indice_hash = costruisci_indice(registro.preventivi())
    indice_bst = costruisci_bst(registro.preventivi())
    for codice in ("007", "012", "003"):
        assert indice_hash.cerca(codice) == indice_bst.cerca(codice)
        assert indice_hash.cerca(codice) == registro.per_codice(codice)


def test_pu18_11_regressione_tappe_precedenti():
    assert totale_spedizione(500, "nazionale", "s") == 9
    assert totale_spedizione(2500, "locale", "n") == 8
    assert formatta_euro(1200) == "12,00"
    servizio = ServizioConsultazione(CodaDequeU16())
    servizio.accoda_richiesta(RichiestaConsultazione("R01", PoliticaSoglia(500)))
    servizio.accoda_richiesta(RichiestaConsultazione("R02", PoliticaSoglia(0)))
    esiti = servizio.elabora_tutte(raccolta_canonica())
    assert [e.codice for e in esiti] == ["R01", "R02"]


def test_pu18_12_conteggi_e_costi():
    indice = indice_su_codici(["012", "003", "017"])
    assert indice.confronti_per("012") >= 1
    assert indice.confronti_per("999") >= 0
    assert indice.fattore_carico == pytest.approx(3 / indice.capacita)
    assert len(indice.fotografia_ordinata()) == 3


# --- Tre casi propri motivati ---


def test_pu18_proprio_01_confine_007_e_7():
    indice = indice_su_codici(["007", "7"])
    assert indice.cerca("007").codice == "007"
    assert indice.cerca("7").codice == "7"
    assert len(indice) == 2


def test_pu18_proprio_02_oracolo_dict_su_sequenza():
    codici = ["012", "003", "017", "007", "021", "034"]
    indice = indice_su_codici(codici)
    oracolo = {c: preventivo_sintetico(c) for c in codici}
    indice.rimuovi("017")
    del oracolo["017"]
    indice.inserisci("042", preventivo_sintetico("042"))
    oracolo["042"] = preventivo_sintetico("042")
    assert len(indice) == len(oracolo)
    for codice, record in oracolo.items():
        assert indice.cerca(codice) == record
    indice.controlla_invarianti()


def test_pu18_proprio_03_fotografia_precedente():
    registro = raccolta_canonica()
    fotografia_vecchia = costruisci_indice(registro.preventivi())
    registro.aggiorna("007", "nazionale", 500)
    fotografia_nuova = costruisci_indice(registro.preventivi())
    assert fotografia_vecchia.cerca("007").totale_cent == 450
    assert fotografia_nuova.cerca("007").totale_cent == 500
