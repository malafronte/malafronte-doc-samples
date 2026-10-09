"""Regressioni dei fix su CLI, CSV e protocollo di uguaglianza (U14)."""

import csv
import os
import tempfile

import cli_magazzino_u14 as cli
import csv_prenotazioni_u14 as persistenza
import pytest
from intervalli_u14 import Intervallo
from magazzino_composto_u14 import Magazzino
from misure_modello_dati_u14 import MisuraEsplicita
from persistenza_magazzino_u14 import carica_magazzino, salva_magazzino
from prenotazioni_u14 import Prenotazione, RegistroPrenotazioni


def avvia_cli(percorso, risposte, monkeypatch):
    """Esegue il menu con input fissati e I/O reale in una directory temporanea."""
    ingressi = iter(risposte)
    monkeypatch.setattr("builtins.input", lambda prompt: next(ingressi))
    return cli.main([str(percorso)])


@pytest.mark.parametrize("scelta", ["3", "4"])
@pytest.mark.parametrize("uscita", [["0"], ["6", "0"]])
def test_cli_inserimento_e_modifica_salvano_i_quattro_dati(
    tmp_path, monkeypatch, capsys, scelta, uscita
):
    archivio = tmp_path / "magazzino.csv"
    if scelta == "4":
        iniziale = Magazzino()
        iniziale.inserisci("007", "Vite, lunga", 4, 25)
        salva_magazzino(archivio, iniziale)

    assert avvia_cli(archivio, [scelta, "007", 'Caffè, "A"', "6", "350", *uscita], monkeypatch) == 0

    testo = capsys.readouterr().out
    assert "rifiutato" not in testo
    assert "archivio salvato:" in testo
    dati = carica_magazzino(archivio).cerca("007")
    assert (dati.codice, dati.descrizione, dati.quantita, dati.prezzo_centesimi) == (
        "007",
        'Caffè, "A"',
        6,
        350,
    )


@pytest.mark.parametrize("quantita", ["-1", "quattro"])
def test_cli_dato_invalido_non_cambia_archivio_ne_flag(tmp_path, monkeypatch, capsys, quantita):
    archivio = tmp_path / "magazzino.csv"
    magazzino = Magazzino()
    magazzino.inserisci("007", "Vite", 4, 25)
    salva_magazzino(archivio, magazzino)
    precedente = archivio.read_bytes()

    assert (
        avvia_cli(archivio, ["4", "007", "Nuova descrizione", quantita, "25", "0"], monkeypatch)
        == 0
    )

    testo = capsys.readouterr().out
    assert "aggiornamento rifiutato:" in testo
    assert "campo 'quantita'" in testo
    assert "chiusura senza modifiche pendenti" in testo
    assert "archivio salvato:" not in testo
    assert archivio.read_bytes() == precedente


def test_cli_salvataggio_di_uscita_fallito_conserva_le_modifiche(tmp_path, monkeypatch, capsys):
    archivio = tmp_path / "magazzino.csv"
    tentativi = []

    def salva_dopo_un_guasto(percorso, magazzino):
        tentativi.append(magazzino.cerca("007"))
        if len(tentativi) == 1:
            raise OSError("guasto simulato")
        return salva_magazzino(percorso, magazzino)

    monkeypatch.setattr(cli, "salva_magazzino", salva_dopo_un_guasto)
    assert avvia_cli(archivio, ["3", "007", "Vite", "4", "25", "0", "0"], monkeypatch) == 0

    assert len(tentativi) == 2
    assert tentativi[0] == tentativi[1]
    assert carica_magazzino(archivio).cerca("007").quantita == 4
    testo = capsys.readouterr().out
    assert "si resta nel menu con le modifiche in memoria" in testo
    assert testo.count("archivio salvato:") == 1


def test_importazione_csv_con_quote_non_chiuse_rifiuta_tutto_il_lotto(tmp_path):
    archivio = tmp_path / "malformato.csv"
    archivio.write_text(
        "codice,aula,inizio_min,fine_min,partecipanti\n"
        "PR-01,Lab A,540,600,20\n"
        'PR-02,Lab A,600,660,"18\n',
        encoding="utf-8",
    )
    registro = RegistroPrenotazioni()
    originale = Prenotazione("XX", "Lab Z", Intervallo(0, 30), 5)
    registro.registra(originale)
    precedente = registro.riepilogo()

    with pytest.raises(csv.Error):
        persistenza.importa_lotto(archivio, registro)

    assert registro.riepilogo() == precedente
    assert registro.prenotazioni() == (originale,)
    assert registro.cerca("XX") is originale


def test_csv_rigoroso_conserva_quoting_e_campi_multilinea_validi(tmp_path):
    archivio = tmp_path / "valido.csv"
    originale = Prenotazione("007", 'Lab, "A"\npiano 1', Intervallo(540, 600), 20)
    registro = RegistroPrenotazioni()
    registro.registra(originale)
    persistenza.esporta_registro(archivio, registro)

    nuovo = RegistroPrenotazioni()
    persistenza.importa_lotto(archivio, nuovo)

    assert nuovo.prenotazioni() == (originale,)
    assert nuovo.cerca("007") is not originale


@pytest.mark.parametrize("guasto", [False, True])
def test_esportazione_preserva_un_temporaneo_preesistente(tmp_path, monkeypatch, guasto):
    destinazione = tmp_path / "prenotazioni.csv"
    destinazione.write_bytes(b"archivio precedente\n")
    preesistente = tmp_path / "prenotazioni.csv.tmp"
    preesistente.write_bytes(b"altri dati da conservare\n")
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    sostituisci = os.replace
    temporanei = []

    def sostituzione_controllata(origine, destino):
        temporanei.append(origine)
        assert origine.parent == destinazione.parent
        assert origine != preesistente
        assert destino == destinazione
        if guasto:
            raise OSError("sostituzione simulata non riuscita")
        return sostituisci(origine, destino)

    monkeypatch.setattr(persistenza.os, "replace", sostituzione_controllata)
    if guasto:
        with pytest.raises(OSError, match="sostituzione simulata"):
            persistenza.esporta_registro(destinazione, registro)
        assert destinazione.read_bytes() == b"archivio precedente\n"
    else:
        persistenza.esporta_registro(destinazione, registro)
        assert persistenza.leggi_candidati(destinazione) == list(registro.prenotazioni())

    assert preesistente.read_bytes() == b"altri dati da conservare\n"
    assert len(temporanei) == 1
    assert not temporanei[0].exists()
    assert set(tmp_path.iterdir()) == {destinazione, preesistente}


def test_creazione_temporaneo_fallita_non_rimuove_file_preesistenti(tmp_path, monkeypatch):
    destinazione = tmp_path / "prenotazioni.csv"
    destinazione.write_bytes(b"archivio precedente\n")
    preesistente = tmp_path / "prenotazioni.csv.tmp"
    preesistente.write_bytes(b"altri dati da conservare\n")

    def creazione_fallita(*args, **kwargs):
        raise PermissionError("creazione simulata non riuscita")

    monkeypatch.setattr(tempfile, "NamedTemporaryFile", creazione_fallita)
    with pytest.raises(PermissionError, match="creazione simulata"):
        persistenza.esporta_registro(destinazione, RegistroPrenotazioni())

    assert destinazione.read_bytes() == b"archivio precedente\n"
    assert preesistente.read_bytes() == b"altri dati da conservare\n"
    assert set(tmp_path.iterdir()) == {destinazione, preesistente}


def test_scrittura_csv_fallita_rimuove_solo_il_proprio_temporaneo(tmp_path, monkeypatch):
    destinazione = tmp_path / "prenotazioni.csv"
    destinazione.write_bytes(b"archivio precedente\n")
    preesistente = tmp_path / "prenotazioni.csv.tmp"
    preesistente.write_bytes(b"altri dati da conservare\n")
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    crea_scrittore = csv.writer

    class ScrittoreDifettoso:
        def __init__(self, flusso):
            self._scrittore = crea_scrittore(flusso)
            self._righe = 0

        def writerow(self, riga):
            self._righe += 1
            if self._righe == 2:
                raise OSError("scrittura simulata non riuscita")
            return self._scrittore.writerow(riga)

    monkeypatch.setattr(persistenza.csv, "writer", ScrittoreDifettoso)
    with pytest.raises(OSError, match="scrittura simulata"):
        persistenza.esporta_registro(destinazione, registro)

    assert destinazione.read_bytes() == b"archivio precedente\n"
    assert preesistente.read_bytes() == b"altri dati da conservare\n"
    assert set(tmp_path.iterdir()) == {destinazione, preesistente}


def test_notimplemented_permette_il_confronto_dell_altro_operando():
    class ConfrontoAlternativo:
        def __eq__(self, altro):
            return isinstance(altro, MisuraEsplicita) and altro.valore_cm == 12

    misura = MisuraEsplicita("007", 12)
    altro = ConfrontoAlternativo()

    assert misura.__eq__(altro) is NotImplemented
    assert (misura == altro) is True
    assert (altro == misura) is True
