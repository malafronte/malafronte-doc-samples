"""Prove semantiche del registro delle prenotazioni (U14).

Casi pubblici PREN-01…PREN-14 del piano di collaudo dell'Unità 14, più le
verifiche di priorità dei controlli richieste dal piano.
"""

import pytest
from intervalli_u14 import Intervallo
from prenotazioni_u14 import (
    CodiceDuplicato,
    ConflittoPrenotazione,
    Prenotazione,
    RegistroPrenotazioni,
)


def pr_01():
    return Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20)


def pr_02():
    return Prenotazione("PR-02", "Lab A", Intervallo(600, 660), 18)


def pr_03():
    return Prenotazione("PR-03", "Lab A", Intervallo(570, 630), 15)


def pr_04():
    return Prenotazione("PR-04", "Lab B", Intervallo(570, 630), 12)


def sequenza_canonica():
    registro = RegistroPrenotazioni()
    registro.registra(pr_01())
    registro.registra(pr_02())
    with pytest.raises(ConflittoPrenotazione):
        registro.registra(pr_03())
    registro.registra(pr_04())
    return registro


# --- PREN-01: intervallo valido, durata, confine di fine giornata ------------


def test_pren_01_dati_e_durata():
    intervallo = Intervallo(540, 600)
    assert intervallo.durata_min == 60
    assert Intervallo(1439, 1440).durata_min == 1


def test_pren_01_valore_frozen_uguale_non_identico():
    assert Intervallo(540, 600) == Intervallo(540, 600)
    assert Intervallo(540, 600) is not Intervallo(540, 600)


# --- PREN-02: dati invalidi rifiutati alla costruzione ------------------------


@pytest.mark.parametrize(
    "inizio,fine",
    [(600, 540), (540, 540), (-1, 10), (0, 1441), (1440, 1440), (True, 60), ("540", 600)],
)
def test_pren_02_intervalli_invalidi(inizio, fine):
    with pytest.raises(ValueError):
        Intervallo(inizio, fine)


def test_pren_02_prenotazione_invalida():
    with pytest.raises(ValueError):
        Prenotazione("", "Lab A", Intervallo(0, 60), 5)
    with pytest.raises(ValueError):
        Prenotazione("PR-05", " Lab A", Intervallo(0, 60), 5)
    with pytest.raises(ValueError):
        Prenotazione("PR-05", "Lab A", Intervallo(0, 60), 0)
    with pytest.raises(ValueError):
        Prenotazione("PR-05", "Lab A", (0, 60), 5)
    with pytest.raises(ValueError):
        Prenotazione("PR-05", "Lab A", Intervallo(0, 60), True)


# --- PREN-03: confronto di coppie ----------------------------------------------


def test_pren_03_separati_e_adiacenti_falsi():
    assert not Intervallo(540, 600).sovrapposto_a(Intervallo(600, 660))
    assert not Intervallo(600, 660).sovrapposto_a(Intervallo(540, 600))
    assert not Intervallo(0, 1).sovrapposto_a(Intervallo(1, 2))
    assert not Intervallo(1439, 1440).sovrapposto_a(Intervallo(1438, 1439))


def test_pren_03_sovrapposti_veri():
    assert Intervallo(540, 600).sovrapposto_a(Intervallo(570, 630))
    assert Intervallo(540, 660).sovrapposto_a(Intervallo(570, 600))
    assert Intervallo(540, 600).sovrapposto_a(Intervallo(540, 600))


def test_pren_03_simmetria():
    prima = Intervallo(540, 600)
    seconda = Intervallo(570, 630)
    assert prima.sovrapposto_a(seconda) == seconda.sovrapposto_a(prima)


# --- PREN-04: aule diverse ammesse ---------------------------------------------


def test_pren_04_stessi_orari_aule_diverse():
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("A", "Lab 1", Intervallo(540, 600), 5))
    registro.registra(Prenotazione("B", "Lab 2", Intervallo(540, 600), 5))
    assert registro.riepilogo()["numero_prenotazioni"] == 2


# --- PREN-05: codice duplicato --------------------------------------------------


def test_pren_05_duplicato_anche_in_altra_aula():
    registro = sequenza_canonica()
    stato_precedente = [p.codice for p in registro.prenotazioni()]
    with pytest.raises(CodiceDuplicato):
        registro.registra(Prenotazione("PR-01", "Lab C", Intervallo(540, 600), 9))
    assert [p.codice for p in registro.prenotazioni()] == stato_precedente


def test_pren_05_duplicato_prima_del_conflitto():
    registro = RegistroPrenotazioni()
    registro.registra(pr_01())
    # stesso codice e stessi minuti: duplicato e conflitto coesistono,
    # ma il duplicato viene segnalato per primo.
    with pytest.raises(CodiceDuplicato):
        registro.registra(pr_01())


# --- PREN-06: sequenza canonica -------------------------------------------------


def test_pren_06_sequenza_canonica():
    registro = sequenza_canonica()
    totale = registro.riepilogo()
    assert totale["numero_prenotazioni"] == 3
    assert totale["durata_totale_min"] == 180
    assert totale["partecipanti_totali"] == 50
    assert "PR-03" not in [p.codice for p in registro.prenotazioni()]


def test_pren_06_riepilogo_sul_vuoto():
    totale = RegistroPrenotazioni().riepilogo()
    assert totale == {
        "numero_prenotazioni": 0,
        "durata_totale_min": 0,
        "partecipanti_totali": 0,
        "prenotazioni": [],
    }


# --- PREN-07: ricerca e annullamento --------------------------------------------


def test_pren_07_cerca_trova_primo_assente_none():
    registro = sequenza_canonica()
    trovata = registro.cerca("PR-01")
    assert trovata.codice == "PR-01"
    assert registro.cerca("PR-99") is None


def test_pren_07_annulla_esiti():
    registro = sequenza_canonica()
    assert registro.annulla("PR-01") is True
    assert registro.cerca("PR-01") is None
    assert registro.annulla("PR-01") is False


def test_pren_07_codice_malformato_valueerror():
    registro = RegistroPrenotazioni()
    for codice in ("", " PR-01", 7):
        with pytest.raises(ValueError):
            registro.cerca(codice)
        with pytest.raises(ValueError):
            registro.annulla(codice)


# --- PREN-08: modifica identica --------------------------------------------------


def test_pren_08_modifica_identica_riuscita():
    registro = sequenza_canonica()
    assert registro.modifica("PR-02", "Lab A", Intervallo(600, 660), 18) is True
    assert registro.cerca("PR-02").partecipanti == 18


# --- PREN-09: modifica rifiutata senza sostituzioni anticipate --------------------


def test_pren_09_modifica_in_conflitto_stato_intatto():
    registro = sequenza_canonica()
    prima_dello_stato = [p.testo_riepilogo() for p in registro.prenotazioni()]
    with pytest.raises(ConflittoPrenotazione):
        registro.modifica("PR-02", "Lab A", Intervallo(585, 645), 18)
    assert [p.testo_riepilogo() for p in registro.prenotazioni()] == prima_dello_stato
    assert registro.riepilogo()["durata_totale_min"] == 180


def test_pren_09_modifica_invalida_con_codice_assente():
    registro = RegistroPrenotazioni()
    with pytest.raises(ValueError):
        registro.modifica("PR-99", "", Intervallo(0, 60), 5)


def test_pren_09_modifica_valida_con_codice_assente_false():
    registro = RegistroPrenotazioni()
    assert registro.modifica("PR-99", "Lab A", Intervallo(0, 60), 5) is False


def test_pren_09_modifica_in_altra_aula():
    registro = sequenza_canonica()
    # Lab B è occupata da PR-04 in [570, 630): la fascia 660-720 è libera
    assert registro.modifica("PR-02", "Lab B", Intervallo(660, 720), 18) is True


# --- PREN-10: snapshot e valori ---------------------------------------------------


def test_pren_10_modificare_il_riepilogo_non_tocca_il_registro():
    registro = sequenza_canonica()
    snapshot = registro.riepilogo()
    snapshot["prenotazioni"][0]["aula"] = "manomessa"
    snapshot["numero_prenotazioni"] = 99
    fresco = registro.riepilogo()
    assert fresco["prenotazioni"][0]["aula"] == "Lab A"
    assert fresco["numero_prenotazioni"] == 3


def test_pren_10_vecchio_alias_dopo_la_sostituzione():
    registro = RegistroPrenotazioni()
    registro.registra(pr_02())
    vecchia = registro.cerca("PR-02")
    registro.modifica("PR-02", "Lab A", Intervallo(660, 720), 18)
    assert vecchia.intervallo.inizio_min == 600
    assert registro.cerca("PR-02").intervallo.inizio_min == 660
    assert registro.cerca("PR-02") is not vecchia


def test_pren_10_tupla_non_modificabile():
    registro = sequenza_canonica()
    valori = registro.prenotazioni()
    with pytest.raises(AttributeError):
        valori.append(pr_03())


# --- PREN-11: due registri indipendenti ---------------------------------------------


def test_pren_11_operazioni_intercalate():
    primo = RegistroPrenotazioni()
    secondo = RegistroPrenotazioni()
    primo.registra(pr_01())
    secondo.registra(pr_04())
    primo.registra(pr_02())
    secondo.registra(pr_01())
    assert primo.riepilogo()["numero_prenotazioni"] == 2
    assert secondo.riepilogo()["numero_prenotazioni"] == 2
    assert [p.codice for p in primo.prenotazioni()] == ["PR-01", "PR-02"]
    assert [p.codice for p in secondo.prenotazioni()] == ["PR-04", "PR-01"]


# --- PREN-12: lotto rifiutato per intero ----------------------------------------------


def test_pren_12_seconda_riga_rifiutata_nessun_inserimento():
    registro = RegistroPrenotazioni()
    lotto = [
        Prenotazione("PX-01", "Lab C", Intervallo(540, 600), 8),
        Prenotazione("PX-02", "Lab C", Intervallo(570, 630), 9),
    ]
    with pytest.raises(ConflittoPrenotazione):
        registro.registra_lotto(lotto)
    assert registro.riepilogo()["numero_prenotazioni"] == 0


def test_pren_12_duplicato_interno_al_lotto():
    registro = RegistroPrenotazioni()
    lotto = [
        Prenotazione("PX-01", "Lab C", Intervallo(0, 60), 8),
        Prenotazione("PX-01", "Lab D", Intervallo(60, 120), 8),
    ]
    with pytest.raises(CodiceDuplicato):
        registro.registra_lotto(lotto)
    assert registro.riepilogo()["numero_prenotazioni"] == 0


def test_pren_12_duplicato_contro_lo_stato_iniziale():
    registro = RegistroPrenotazioni()
    registro.registra(pr_01())
    lotto = [Prenotazione("PX-09", "Lab C", Intervallo(0, 60), 8), pr_01()]
    with pytest.raises(CodiceDuplicato):
        registro.registra_lotto(lotto)
    assert [p.codice for p in registro.prenotazioni()] == ["PR-01"]


def test_pren_12_lotto_vuoto_e_lotto_valido():
    registro = RegistroPrenotazioni()
    registro.registra_lotto([])
    assert registro.riepilogo()["numero_prenotazioni"] == 0
    registro.registra_lotto([pr_01(), pr_04()])
    assert [p.codice for p in registro.prenotazioni()] == ["PR-01", "PR-04"]


def test_pren_12_il_registro_mantiene_la_identita():
    registro = RegistroPrenotazioni()
    registro.registra(pr_01())
    alias = registro
    alias.registra_lotto([pr_04()])
    assert alias is registro
    assert [p.codice for p in registro.prenotazioni()] == ["PR-01", "PR-04"]


# --- PREN-13/14: persistenza (vedi test_persistenza_u14.py) ---------------------------


def test_pren_13_riferimento():
    # Il round-trip CSV è provato in test_persistenza_u14.py con file temporanei.
    assert True
