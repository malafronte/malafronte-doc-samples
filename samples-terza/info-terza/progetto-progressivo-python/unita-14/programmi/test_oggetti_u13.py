"""Suite della variante a oggetti del registro dei preventivi (tappa U13).

Casi pubblici PU13-01-PU13-08, due casi propri motivati e la prova della
modifica breve `totale_complessivo_cent`. Il guasto di salvataggio è provocato
in modo deterministico intercettando la scrittura del temporaneo: non si
usano i permessi della cartella. Dati soltanto sintetici.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_oggetti_u13.py
"""
from pathlib import Path

import registro_persistenza
from registro_dominio import crea_record, riepilogo_per_destinazione
from registro_oggetti_u13 import RegistroPreventivi
from registro_persistenza import carica_archivio, salva_archivio

DATI = Path(__file__).resolve().parent.parent / "dati" / "unita-12"


def percorso(nome):
    """Percorso di una fixture nella cartella dati delle tappe U12-U13."""
    return DATI / nome


def sessione_canonica():
    """Sessione di riferimento: 007/450, 012/0, 003/1200 nell'ordine noto."""
    sessione = RegistroPreventivi()
    sessione.inserisci("007", "locale", 450)
    sessione.inserisci("012", "nazionale", 0)
    sessione.inserisci("003", "locale", 1200)
    return sessione


# --- PU13-01: due sessioni inizialmente vuote, nessun contenitore condiviso ---


def test_pu13_01_due_registri_indipendenti():
    prima = RegistroPreventivi()
    seconda = RegistroPreventivi()
    assert prima.numero() == 0
    assert seconda.numero() == 0
    assert prima.inserisci("007", "locale", 450) is True
    assert prima.numero() == 1
    assert seconda.numero() == 0
    assert seconda.per_lista() == []


# --- PU13-02: codici 007 e 7 distinti in memoria, ricerca ed esportazione ---


def test_pu13_02_codici_distinti():
    sessione = RegistroPreventivi()
    assert sessione.inserisci("007", "locale", 450) is True
    assert sessione.inserisci("7", "locale", 450) is True
    assert sessione.numero() == 2
    assert sessione.cerca("007")["totale_cent"] == 450
    assert sessione.cerca("7")["totale_cent"] == 450
    codici = [record["codice"] for record in sessione.per_lista()]
    assert codici == ["007", "7"]


# --- PU13-03: totale zero e destinazione valida conservati nel round-trip ---


def test_pu13_03_totale_zero_e_destinazione_valida():
    sessione = RegistroPreventivi()
    assert sessione.inserisci("012", "nazionale", 0) is True
    caricata = RegistroPreventivi()
    assert caricata.sostituisci_da_lista(sessione.per_lista()) is True
    assert caricata.per_lista() == [
        {"codice": "012", "destinazione": "nazionale", "totale_cent": 0}
    ]
    riepilogo = caricata.riepilogo_per_destinazione()
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 0}


# --- PU13-04: rifiuti con esito dichiarato e stato interamente conservato ---


def test_pu13_04_rifiuti_senza_effetti():
    sessione = sessione_canonica()
    prima = sessione.per_lista()
    assert sessione.inserisci("007", "locale", 900) is False
    assert sessione.per_lista() == prima
    assert sessione.aggiorna("007", "locale", -1) is False
    assert sessione.per_lista() == prima
    assert sessione.aggiorna("007", "locale", True) is False
    assert sessione.per_lista() == prima
    assert sessione.aggiorna("999", "locale", 100) is False
    assert sessione.per_lista() == prima


# --- PU13-05: salvataggio e nuovo caricamento con dati e ordine equivalenti ---


def test_pu13_05_salvataggio_e_ricarico(tmp_path):
    sessione = sessione_canonica()
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, sessione.per_lista()) is True
    caricato, esito, dettaglio = carica_archivio(archivio)
    assert esito == ""
    nuova = RegistroPreventivi()
    assert nuova.sostituisci_da_lista(caricato) is True
    assert nuova.per_lista() == sessione.per_lista()
    assert nuova.per_lista()[0]["codice"] == "007"
    assert nuova is not sessione


# --- PU13-06: archivio corrotto e guasto di salvataggio, politiche U12 ---


def test_pu13_06_archivio_corrotto_e_guasto(tmp_path, monkeypatch):
    sessione = sessione_canonica()
    prima = sessione.per_lista()

    # Archivio corrotto: esito distinto e nessuna sostituzione della sessione.
    corrotto, esito, dettaglio = carica_archivio(percorso("archivio_sintassi_corrotta.json"))
    assert corrotto is None
    assert esito == "sintassi"
    assert sessione.per_lista() == prima

    # Guasto di scrittura: il file precedente resta identico nei byte.
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, sessione.per_lista()) is True
    byte_prima = archivio.read_bytes()

    def guasto(percorso_temporaneo, testo):
        raise OSError("guasto simulato di scrittura")

    monkeypatch.setattr(registro_persistenza, "_scrivi_temporaneo", guasto)
    assert salva_archivio(archivio, sessione.per_lista()) is False
    assert archivio.read_bytes() == byte_prima
    assert not (tmp_path / "archivio.json.tmp").exists()
    assert sessione.per_lista() == prima


# --- PU13-07: riepilogo equivalente alla versione precedente sul dataset ---


def test_pu13_07_riepilogo_equivalente():
    sessione = sessione_canonica()
    lista_storica = [
        crea_record("007", "locale", 450),
        crea_record("012", "nazionale", 0),
        crea_record("003", "locale", 1200),
    ]
    assert sessione.riepilogo_per_destinazione() == riepilogo_per_destinazione(
        lista_storica
    )
    assert sessione.riepilogo_per_destinazione() == {
        "locale": {"conteggio": 2, "totale_cent": 1650},
        "nazionale": {"conteggio": 1, "totale_cent": 0},
    }


# --- PU13-08: snapshot protetto, nessuna mutazione esterna dello stato ---


def test_pu13_08_snapshot_protetto():
    sessione = sessione_canonica()
    snapshot = sessione.per_lista()
    snapshot.append({"codice": "999", "destinazione": "locale", "totale_cent": 1})
    snapshot[0]["totale_cent"] = 0
    assert sessione.numero() == 3
    assert sessione.cerca("007")["totale_cent"] == 450

    consultato = sessione.cerca("012")
    consultato["totale_cent"] = 999
    assert sessione.cerca("012")["totale_cent"] == 0


# --- Casi propri PR-13-1 e PR-13-2 ---


def test_proprio_sostituzione_indipendente():
    """PR-13-1: la lista ricevuta da sostituisci_da_lista resta autonoma."""
    sessione = RegistroPreventivi()
    esterna = [{"codice": "020", "destinazione": "nazionale", "totale_cent": 75}]
    assert sessione.sostituisci_da_lista(esterna) is True
    esterna[0]["totale_cent"] = 999
    esterna.append({"codice": "021", "destinazione": "locale", "totale_cent": 1})
    assert sessione.per_lista() == [
        {"codice": "020", "destinazione": "nazionale", "totale_cent": 75}
    ]


def test_proprio_conversione_sempre_nuova():
    """PR-13-2: ogni conversione produce contenitori nuovi, mai gli stessi."""
    sessione = sessione_canonica()
    prima_lista = sessione.per_lista()
    seconda_lista = sessione.per_lista()
    assert prima_lista == seconda_lista
    assert prima_lista is not seconda_lista
    assert prima_lista[0] is not seconda_lista[0]
    assert prima_lista[0] is not sessione.cerca("007")


# --- Modifica breve: totale complessivo in centesimi ---


def test_modifica_breve_totale_complessivo():
    """La modifica breve somma i totali senza duplicare stato."""
    sessione = RegistroPreventivi()
    assert sessione.totale_complessivo_cent() == 0
    sessione = sessione_canonica()
    assert sessione.totale_complessivo_cent() == 1650
    assert sessione.numero() == 3
