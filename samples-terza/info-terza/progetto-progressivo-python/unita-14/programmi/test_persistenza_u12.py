"""Suite di verifica di persistenza, errori e riproducibilità (tappa U12).

Casi pubblici PU12-01-PU12-10, tre casi propri e dieci regressioni CLI.
I guasti di scrittura e
sostituzione sono provocati in modo deterministico intercettando le operazioni
interne del modulo di persistenza: non si usano i permessi della cartella.
Dati soltanto sintetici.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_persistenza_u12.py
"""
from pathlib import Path

import registro_persistenza
import registro_cli
from registro_dominio import (
    aggiorna_record,
    crea_record,
    elimina_record,
    formatta_euro,
    inserisci_record,
    riepilogo_per_destinazione,
    valida_dominio_record,
    valida_struttura_documento,
    vista_per_totale,
)
from registro_persistenza import (
    carica_archivio,
    documento_del_registro,
    esporta_csv,
    salva_archivio,
)

DATI = Path(__file__).resolve().parent.parent / "dati" / "unita-12"


def percorso(nome):
    """Percorso di una fixture nella cartella dati della tappa."""
    return DATI / nome


def registro_canonico():
    """Registro di riferimento U12: codici 007, 012, 003; totali 450, 0, 1200."""
    return [
        crea_record("007", "locale", 450),
        crea_record("012", "nazionale", 0),
        crea_record("003", "locale", 1200),
    ]


# --- PU12-01: archivio vuoto valido, distinto da assente e corrotto ---


def test_pu12_01_archivio_vuoto_valido():
    registro, esito, dettaglio = carica_archivio(percorso("archivio_vuoto.json"))
    assert esito == ""
    assert registro == []

    assente, esito_assente, dettaglio_assente = carica_archivio(percorso("non_esiste.json"))
    assert (assente, esito_assente) == (None, "assente")

    corrotto, esito_corrotto, dettaglio_corrotto = carica_archivio(
        percorso("archivio_sintassi_corrotta.json")
    )
    assert (corrotto, esito_corrotto) == (None, "sintassi")

    # Il documento vuoto è riscritto come vuoto coerente con lo schema.
    assert documento_del_registro([]) == {"versione_schema": 1, "preventivi": []}


# --- PU12-02 e PU12-03: zeri iniziali e totale zero ---


def test_pu12_02_codice_007_nel_round_trip(tmp_path):
    registro = registro_canonico()
    percorso_archivio = tmp_path / "archivio.json"
    assert salva_archivio(percorso_archivio, registro) is True

    riletto, esito, dettaglio = carica_archivio(percorso_archivio)
    assert esito == ""
    assert riletto[0]["codice"] == "007"
    assert riletto[0]["codice"] != "7"
    assert riletto == registro

    # Ricerca, aggiornamento ed eliminazione lavorano sul codice stringa.
    assert aggiorna_record(riletto, "007", "nazionale", 500) is True
    assert aggiorna_record(riletto, "7", "nazionale", 500) is False
    assert elimina_record(riletto, "007") is True
    assert elimina_record(riletto, "007") is False
    assert len(riletto) == 2


def test_pu12_03_totale_zero_ammesso_e_presentato():
    registro = registro_canonico()
    assert registro[1]["totale_cent"] == 0
    assert valida_dominio_record(registro[1]) == ""
    assert formatta_euro(0) == "0,00"
    assert formatta_euro(450) == "4,50"
    assert formatta_euro(1200) == "12,00"
    assert aggiorna_record(registro, "012", "nazionale", 0) is True
    assert registro[1]["totale_cent"] == 0


# --- PU12-04 e PU12-05: rifiuti con diagnosi e senza effetti parziali ---


def test_pu12_04_destinazione_invalida_rifiutata():
    registro, esito, dettaglio = carica_archivio(percorso("archivio_dominio_invalido.json"))
    assert (registro, esito) == (None, "dominio")
    assert "destinazione" in dettaglio
    assert "estero" in dettaglio

    ancora_valido, esito_valido, dettaglio_valido = carica_archivio(
        percorso("archivio_canonico.json")
    )
    assert esito_valido == ""
    assert len(ancora_valido) == 3
    assert inserisci_record(ancora_valido, "020", "estero", 100) is False
    assert len(ancora_valido) == 3


def test_pu12_05_codice_duplicato_rifiutato(tmp_path):
    registro, esito, dettaglio = carica_archivio(percorso("archivio_duplicati.json"))
    assert (registro, esito) == (None, "dominio")
    assert "duplicato" in dettaglio

    # Il registro in memoria resta invariato e nessun file viene sovrascritto.
    memoria = registro_canonico()
    percorso_archivio = tmp_path / "archivio.json"
    assert salva_archivio(percorso_archivio, memoria) is True
    prima_dei_byte = percorso_archivio.read_bytes()

    assert inserisci_record(memoria, "007", "locale", 100) is False
    assert salva_archivio(percorso_archivio, memoria) is True
    assert percorso_archivio.read_bytes() == prima_dei_byte
    assert len(memoria) == 3
    assert memoria[0]["totale_cent"] == 450


# --- PU12-06 e PU12-07: sintassi contro struttura ---


def test_pu12_06_sintassi_con_posizione():
    registro, esito, dettaglio = carica_archivio(percorso("archivio_sintassi_corrotta.json"))
    assert (registro, esito) == (None, "sintassi")
    assert "riga" in dettaglio
    assert "colonna" in dettaglio


def test_pu12_07_valido_sintatticamente_ma_fuori_schema():
    registro, esito, dettaglio = carica_archivio(percorso("archivio_struttura_invalida.json"))
    assert (registro, esito) == (None, "struttura")
    assert "struttura" in dettaglio

    # Il parser ha già lavorato: è la validazione di struttura a rifiutare.
    assert valida_struttura_documento({"versione_schema": 1, "preventivi": []}) == ""
    assert valida_struttura_documento([1, 2]) != ""


# --- PU12-08: guasto di salvataggio con archivio precedente valido ---


def test_pu12_08_guasto_di_sostituzione_preserva_il_file(tmp_path, monkeypatch):
    percorso_archivio = tmp_path / "archivio.json"
    memoria = registro_canonico()
    assert salva_archivio(percorso_archivio, memoria) is True
    byte_prima = percorso_archivio.read_bytes()

    memoria.append(crea_record("020", "locale", 100))

    def sostituzione_fallita(sorgente, destinazione):
        raise OSError("guasto simulato durante la sostituzione")

    monkeypatch.setattr(registro_persistenza, "_sostituisci_file", sostituzione_fallita)
    esito = salva_archivio(percorso_archivio, memoria)
    monkeypatch.undo()

    # Nessun successo, file precedente identico nei byte, temporaneo eliminato,
    # modifiche ancora disponibili in memoria.
    assert esito is False
    assert percorso_archivio.read_bytes() == byte_prima
    assert not (tmp_path / "archivio.json.tmp").exists()
    assert len(memoria) == 4


def test_pu12_08_bis_guasto_di_scrittura_preserva_il_file(tmp_path, monkeypatch):
    percorso_archivio = tmp_path / "archivio.json"
    memoria = registro_canonico()
    assert salva_archivio(percorso_archivio, memoria) is True
    byte_prima = percorso_archivio.read_bytes()

    def scrittura_fallita(percorso_temporaneo, testo):
        raise OSError("guasto simulato durante la scrittura")

    monkeypatch.setattr(registro_persistenza, "_scrivi_temporaneo", scrittura_fallita)
    esito = salva_archivio(percorso_archivio, memoria)
    monkeypatch.undo()

    assert esito is False
    assert percorso_archivio.read_bytes() == byte_prima
    assert not (tmp_path / "archivio.json.tmp").exists()


# --- PU12-09: riavvio dopo un salvataggio riuscito ---


def test_pu12_09_riavvio_equivalente(tmp_path):
    percorso_archivio = tmp_path / "archivio.json"
    sessione = registro_canonico()
    assert inserisci_record(sessione, "020", "nazionale", 75) is True
    assert elimina_record(sessione, "012") is True
    assert salva_archivio(percorso_archivio, sessione) is True

    # Nuovo avvio: il registro nasce vuoto e si carica dall'archivio.
    riletto, esito, dettaglio = carica_archivio(percorso_archivio)
    assert esito == ""
    assert riletto == sessione
    assert [record["codice"] for record in riletto] == ["007", "003", "020"]
    for record in riletto:
        assert isinstance(record["totale_cent"], int)
        assert record["codice"] == record["codice"].strip()


# --- PU12-10: regressione degli aggregati e delle viste ---


def test_pu12_10_aggregati_e_viste_sui_record_caricati():
    registro, esito, dettaglio = carica_archivio(percorso("archivio_canonico.json"))
    assert esito == ""

    riepilogo = riepilogo_per_destinazione(registro)
    assert riepilogo["locale"] == {"conteggio": 2, "totale_cent": 1650}
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 0}

    vista = vista_per_totale(registro)
    assert [record["codice"] for record in vista] == ["012", "007", "003"]

    # Le unità non cambiano: i totali restano centesimi interi.
    totale_cent = 0
    for record in registro:
        totale_cent = totale_cent + record["totale_cent"]
    assert totale_cent == 1650


# --- Casi propri motivati ---


def test_proprio_1_versione_schema_booleana_rifiutata():
    """PR-1: `true` non è l'intero 1 dello schema.

    Discrimina chi accetta i booleani come interi: in Python `True == 1`.
    """
    registro, esito, dettaglio = carica_archivio(percorso("archivio_versione_booleana.json"))
    assert (registro, esito) == (None, "struttura")
    assert "versione_schema" in dettaglio


def test_proprio_2_campo_extra_nel_record_rifiutato():
    """PR-2: il record con un campo in più viola lo schema, anche se valido come valori."""
    registro, esito, dettaglio = carica_archivio(percorso("archivio_campo_extra.json"))
    assert (registro, esito) == (None, "struttura")
    assert "campi" in dettaglio


def test_proprio_3_esportazione_csv_di_consultazione(tmp_path):
    """PR-3: il CSV di consultazione è coerente con i dati, non il documento canonico."""
    registro = registro_canonico()
    percorso_csv = tmp_path / "esportazione.csv"
    assert esporta_csv(percorso_csv, registro) is True
    righe = percorso_csv.read_text(encoding="utf-8").splitlines()
    assert righe[0] == "codice,destinazione,totale_cent"
    assert righe[1] == "007,locale,450"
    assert righe[2] == "012,nazionale,0"
    assert righe[3] == "003,locale,1200"
    assert not percorso_csv.read_bytes().startswith(b"\xef\xbb\xbf")


# --- Regressioni della sessione CLI: inizializzazione e modifiche pendenti ---


def esegui_sessione_cli(monkeypatch, capsys, percorso_archivio, comandi):
    """Esegue una sessione con input predisposti; None rappresenta EOF.

    Le domande restano nell'output, così si controlla anche la conferma di
    uscita. Una lettura inattesa esaurisce l'iteratore e fa fallire il test.
    """
    risposte = iter(comandi)

    def leggi(prompt):
        print(prompt, end="")
        risposta = next(risposte)
        if risposta is None:
            raise EOFError
        return risposta

    monkeypatch.setattr(registro_cli, "PERCORSO_PREDEFINITO", percorso_archivio)
    monkeypatch.setattr(registro_cli, "PERCORSO_CSV", percorso_archivio.with_suffix(".csv"))
    monkeypatch.setattr("builtins.input", leggi)
    registro_cli.main()
    assert list(risposte) == []
    return capsys.readouterr().out


def test_cli_salva_prima_di_caricare_preserva_archivio(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    byte_prima = percorso("archivio_canonico.json").read_bytes()
    archivio.write_bytes(byte_prima)
    output = esegui_sessione_cli(monkeypatch, capsys, archivio, ["salva", "esci"])
    assert archivio.read_bytes() == byte_prima
    assert "Registro non inizializzato" in output
    assert "Archivio salvato." not in output


def test_cli_operazioni_prima_di_caricare_senza_effetti(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    output = esegui_sessione_cli(
        monkeypatch, capsys, archivio,
        ["elenco", "cerca", "inserisci", "aggiorna", "elimina", "esporta", "salva", "esci"],
    )
    assert output.count("Registro non inizializzato") == 7
    assert not archivio.exists()
    assert not archivio.with_suffix(".csv").exists()


def test_cli_archivio_assente_inizializzato_da_carica(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    output = esegui_sessione_cli(monkeypatch, capsys, archivio, ["carica", "salva", "esci"])
    assert "Archivio assente: nuovo registro vuoto." in output
    assert "Archivio salvato." in output
    registro, esito, dettaglio = carica_archivio(archivio)
    assert esito == ""
    assert registro == []


def test_cli_caricamento_invalido_non_autorizza_salvataggio(tmp_path, monkeypatch, capsys):
    for nome in (
        "archivio_sintassi_corrotta.json",
        "archivio_struttura_invalida.json",
        "archivio_dominio_invalido.json",
    ):
        archivio = tmp_path / "archivio.json"
        byte_prima = percorso(nome).read_bytes()
        archivio.write_bytes(byte_prima)
        output = esegui_sessione_cli(monkeypatch, capsys, archivio, ["carica", "salva", "esci"])
        assert "Caricamento non riuscito" in output
        assert "Registro non inizializzato" in output
        assert "Archivio salvato." not in output
        assert archivio.read_bytes() == byte_prima


def test_cli_ricaricamento_pendente_conserva_record_e_avviso(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, registro_canonico()) is True
    output = esegui_sessione_cli(
        monkeypatch, capsys, archivio,
        ["carica", "inserisci", "020", "nazionale", "75", "carica",
         "cerca", "020", "esci", "n", "salva", "esci"],
    )
    assert "Caricamento rifiutato: ci sono modifiche non salvate." in output
    assert "020 | nazionale | 0,75 euro (75 centesimi)" in output
    assert "Ci sono modifiche non salvate. Uscire comunque?" in output
    assert "Uscita annullata." in output
    registro, esito, dettaglio = carica_archivio(archivio)
    assert esito == ""
    assert registro[-1] == crea_record("020", "nazionale", 75)


def test_cli_ricaricamento_dopo_salvataggio_ammesso(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, registro_canonico()) is True
    output = esegui_sessione_cli(
        monkeypatch, capsys, archivio,
        ["carica", "inserisci", "020", "nazionale", "75", "salva",
         "carica", "cerca", "020", "esci"],
    )
    assert "Archivio caricato: 4 record." in output
    assert "Caricamento rifiutato" not in output
    assert "020 | nazionale | 0,75 euro (75 centesimi)" in output
    assert "Ci sono modifiche non salvate. Uscire comunque?" not in output


def test_cli_guasto_salvataggio_conserva_modifiche_pendenti(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, registro_canonico()) is True
    byte_prima = archivio.read_bytes()

    def scrittura_fallita(percorso_temporaneo, testo):
        raise OSError("guasto simulato durante la scrittura")

    monkeypatch.setattr(registro_persistenza, "_scrivi_temporaneo", scrittura_fallita)
    output = esegui_sessione_cli(
        monkeypatch, capsys, archivio,
        ["carica", "inserisci", "020", "nazionale", "75", "salva",
         "carica", "cerca", "020", "esci", "s"],
    )
    assert "Salvataggio non riuscito" in output
    assert "Archivio salvato." not in output
    assert "Caricamento rifiutato" in output
    assert "020 | nazionale | 0,75 euro (75 centesimi)" in output
    assert "Ci sono modifiche non salvate. Uscire comunque?" in output
    assert archivio.read_bytes() == byte_prima
    assert not archivio.with_name("archivio.json.tmp").exists()


def test_cli_eof_prima_di_caricare_non_scrive(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    byte_prima = percorso("archivio_canonico.json").read_bytes()
    archivio.write_bytes(byte_prima)
    output = esegui_sessione_cli(monkeypatch, capsys, archivio, [None])
    assert "Input terminato" in output
    assert archivio.read_bytes() == byte_prima


def test_cli_eof_con_modifiche_non_salva(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, registro_canonico()) is True
    byte_prima = archivio.read_bytes()
    output = esegui_sessione_cli(
        monkeypatch, capsys, archivio,
        ["carica", "inserisci", "020", "nazionale", "75", None],
    )
    assert "Record inserito." in output
    assert "Input terminato" in output
    assert "Archivio salvato." not in output
    assert archivio.read_bytes() == byte_prima


def test_cli_eliminazione_completa_salva_vuoto_intenzionale(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "archivio.json"
    assert salva_archivio(archivio, registro_canonico()) is True
    output = esegui_sessione_cli(
        monkeypatch, capsys, archivio,
        ["carica", "elimina", "007", "elimina", "012", "elimina", "003", "salva", "esci"],
    )
    assert output.count("Record eliminato.") == 3
    assert "Archivio salvato." in output
    registro, esito, dettaglio = carica_archivio(archivio)
    assert esito == ""
    assert registro == []
