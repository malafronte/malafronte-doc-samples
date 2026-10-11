"""Suite del modello robusto del registro dei preventivi (tappa U14).

Casi pubblici PU14-01-PU14-08, due casi propri motivati e la prova della
modifica breve `per_destinazione`. I guasti di salvataggio sono provocati in
modo deterministico intercettando la scrittura del temporaneo: non si usano i
permessi della cartella. Dati soltanto sintetici.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_modello_u14.py
"""
from pathlib import Path

import pytest

import registro_persistenza
from registro_dominio import (
    riepilogo_per_destinazione,
    vista_per_codice,
    vista_per_totale,
)
from registro_modello_u14 import (
    CodiceAssente,
    CodiceDuplicato,
    DatoNonAmmesso,
    Preventivo,
    RegistroPreventivi,
    preventivo_da_record,
    record_da_preventivo,
)
from registro_persistenza import (
    carica_archivio,
    documento_del_registro,
    salva_archivio,
)

DATI = Path(__file__).resolve().parent.parent / "dati" / "unita-12"


def percorso(nome):
    """Percorso di una fixture nella cartella dati delle tappe U12-U14."""
    return DATI / nome


def raccolta_canonica():
    """Raccolta di riferimento: 007/450, 012/0, 003/1200 nell'ordine noto."""
    raccolta = RegistroPreventivi()
    raccolta.inserisci("007", "locale", 450)
    raccolta.inserisci("012", "nazionale", 0)
    raccolta.inserisci("003", "locale", 1200)
    return raccolta


# --- PU14-01: uguaglianza dichiarata, is distinto da == ---


def test_pu14_01_uguaglianza_per_contenuto():
    primo = Preventivo("007", "locale", 450)
    secondo = Preventivo("007", "locale", 450)
    assert primo == secondo
    assert primo is not secondo
    assert Preventivo("007", "locale", 450) != Preventivo("7", "locale", 450)
    assert Preventivo("007", "locale", 450) != Preventivo("007", "nazionale", 450)
    assert record_da_preventivo(primo) == record_da_preventivo(secondo)


# --- PU14-02: totale zero e codici 007/7 distinti in ogni rappresentazione ---


def test_pu14_02_zeri_codici_distinti():
    raccolta = RegistroPreventivi()
    raccolta.inserisci("007", "locale", 450)
    raccolta.inserisci("7", "locale", 0)
    assert raccolta.per_codice("007") is not raccolta.per_codice("7")
    assert raccolta.per_codice("7").totale_cent == 0
    ordinata = vista_per_totale(raccolta.per_lista())
    assert [record["codice"] for record in ordinata] == ["7", "007"]
    assert [record["codice"] for record in raccolta.per_lista()] == ["007", "7"]


# --- PU14-03: modifica con ultimo campo invalido, nessun effetto parziale ---


def test_pu14_03_modifica_invalida_senza_effetti():
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    ordine = raccolta.preventivi()
    with pytest.raises(DatoNonAmmesso):
        raccolta.aggiorna("007", "locale", True)
    with pytest.raises(DatoNonAmmesso):
        raccolta.aggiorna("007", "locale", -1)
    with pytest.raises(DatoNonAmmesso):
        raccolta.aggiorna("007", "estera", 100)
    assert raccolta.per_lista() == prima
    assert raccolta.preventivi() == ordine


# --- PU14-04: duplicato e due sessioni indipendenti ---


def test_pu14_04_duplicato_e_sessioni():
    raccolta = raccolta_canonica()
    with pytest.raises(CodiceDuplicato):
        raccolta.inserisci("007", "locale", 900)
    assert raccolta.numero == 3
    with pytest.raises(CodiceAssente):
        raccolta.aggiorna("999", "locale", 100)
    seconda = RegistroPreventivi()
    seconda.inserisci("020", "nazionale", 75)
    assert seconda.numero == 1
    assert raccolta.numero == 3


# --- PU14-05: snapshot protetto ed effetti degli alias documentati ---


def test_pu14_05_snapshot_e_alias():
    raccolta = raccolta_canonica()
    snapshot = raccolta.preventivi()
    assert isinstance(snapshot, tuple)
    assert snapshot[0] == Preventivo("007", "locale", 450)
    # I valori sono frozen: nessuna mutazione degli elementi è possibile.
    with pytest.raises(AttributeError):
        snapshot[0].totale_cent = 0
    # La proiezione per_lista è autonoma: modificarla non tocca la raccolta.
    lista = raccolta.per_lista()
    lista[0]["totale_cent"] = 0
    assert raccolta.per_codice("007").totale_cent == 450
    # Effetto alias dichiarato: chi conserva il valore precedente lo osserva
    # ancora, mentre la raccolta espone il valore nuovo.
    precedente = raccolta.per_codice("007")
    raccolta.aggiorna("007", "locale", 500)
    assert precedente.totale_cent == 450
    assert raccolta.per_codice("007").totale_cent == 500


# --- PU14-06: salvataggio e ricostruzione con valori e tipi equivalenti ---


def test_pu14_06_salvataggio_e_ricostruzione(tmp_path):
    raccolta = raccolta_canonica()
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, raccolta.per_lista()) is True
    caricato, esito, dettaglio = carica_archivio(archivio)
    assert esito == ""
    assert documento_del_registro(raccolta.per_lista()) == documento_del_registro(
        caricato
    )
    ricostruita = RegistroPreventivi()
    ricostruita.sostituisci_da_lista(caricato)
    assert ricostruita.per_lista() == raccolta.per_lista()
    for preventivo in ricostruita.preventivi():
        assert isinstance(preventivo, Preventivo)
        assert isinstance(preventivo.codice, str)
        assert isinstance(preventivo.totale_cent, int)
        assert not isinstance(preventivo.totale_cent, bool)


# --- PU14-07: archivio corrotto e salvataggio fallito, politiche U12 ---


def test_pu14_07_corrotto_e_salvataggio_fallito(tmp_path, monkeypatch):
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()

    corrotto, esito, dettaglio = carica_archivio(percorso("archivio_sintassi_corrotta.json"))
    assert corrotto is None
    assert esito == "sintassi"

    with pytest.raises(DatoNonAmmesso):
        raccolta.sostituisci_da_lista(
            [{"codice": "020", "destinazione": "estera", "totale_cent": 75}]
        )
    assert raccolta.per_lista() == prima

    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, raccolta.per_lista()) is True
    byte_prima = archivio.read_bytes()

    def guasto(percorso_temporaneo, testo):
        raise OSError("guasto simulato di scrittura")

    monkeypatch.setattr(registro_persistenza, "_scrivi_temporaneo", guasto)
    assert salva_archivio(archivio, raccolta.per_lista()) is False
    assert archivio.read_bytes() == byte_prima
    assert not (tmp_path / "archivio.json.tmp").exists()
    assert raccolta.per_lista() == prima


# --- PU14-08: calcolo, riepilogo e vista storica sui dataset noti ---


def test_pu14_08_risultati_storici():
    raccolta = raccolta_canonica()
    lista = raccolta.per_lista()
    assert raccolta.riepilogo_per_destinazione() == riepilogo_per_destinazione(lista)
    assert [record["codice"] for record in vista_per_codice(lista)] == [
        "003",
        "007",
        "012",
    ]
    assert [record["codice"] for record in vista_per_totale(lista)] == [
        "012",
        "007",
        "003",
    ]
    assert preventivo_da_record(lista[0]) == Preventivo("007", "locale", 450)


# --- Casi propri PR-14-1 e PR-14-2 ---


def test_proprio_sostituzione_atomica():
    """PR-14-1: duplicati nella lista di sostituzione rifiutano tutto."""
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    with pytest.raises(CodiceDuplicato):
        raccolta.sostituisci_da_lista(
            [
                {"codice": "020", "destinazione": "nazionale", "totale_cent": 75},
                {"codice": "020", "destinazione": "locale", "totale_cent": 1},
            ]
        )
    assert raccolta.per_lista() == prima


def test_proprio_dati_derivati_aggiornati():
    """PR-14-2: le proprietà derivate seguono lo stato, senza duplicarlo."""
    raccolta = raccolta_canonica()
    assert raccolta.numero == 3
    assert raccolta.totale_complessivo_cent == 1650
    raccolta.elimina("003")
    assert raccolta.numero == 2
    assert raccolta.totale_complessivo_cent == 450
    assert raccolta.per_destinazione("locale") == (Preventivo("007", "locale", 450),)


# --- Modifica breve: selezione per destinazione ---


def test_modifica_breve_per_destinazione():
    raccolta = raccolta_canonica()
    assert raccolta.per_destinazione("locale") == (
        Preventivo("007", "locale", 450),
        Preventivo("003", "locale", 1200),
    )
    assert raccolta.per_destinazione("nazionale") == (
        Preventivo("012", "nazionale", 0),
    )
    solo_locale = RegistroPreventivi()
    solo_locale.inserisci("007", "locale", 450)
    assert solo_locale.per_destinazione("nazionale") == ()
    with pytest.raises(DatoNonAmmesso):
        raccolta.per_destinazione("estera")
