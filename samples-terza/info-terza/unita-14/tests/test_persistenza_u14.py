"""Prove di persistenza CSV/JSON, importazione lotti e guasti (U14).

Casi PREN-13/14 e le verifiche di persistenza del piano di collaudo
(§18.3), su cartelle temporanee: nessuna scrittura sui dati del corso.
"""

import csv
import json

import pytest
from csv_prenotazioni_u14 import (
    CAMPI_PRENOTAZIONE,
    esporta_registro,
    importa_lotto,
    leggi_candidati,
    prenotazione_a_riga,
    riga_a_prenotazione,
)
from intervalli_u14 import Intervallo
from magazzino_composto_u14 import Magazzino
from persistenza_magazzino_u14 import (
    carica_magazzino,
    carica_magazzino_json,
    json_a_magazzino,
    salva_magazzino,
    salva_magazzino_json,
)
from prenotazioni_u14 import ConflittoPrenotazione, Prenotazione, RegistroPrenotazioni


def righe_canoniche():
    return [
        ["codice", "aula", "inizio_min", "fine_min", "partecipanti"],
        ["PR-01", "Lab A", "540", "600", "20"],
        ["PR-02", "Lab A", "600", "660", "18"],
    ]


def scrivi_csv(percorso, righe):
    with open(percorso, "w", encoding="utf-8", newline="") as flusso:
        csv.writer(flusso, lineterminator="\n").writerows(righe)
    return percorso


# --- Conversioni delle prenotazioni ------------------------------------------


def test_riga_a_prenotazione_campi_e_tipo():
    prenotazione = riga_a_prenotazione(["PR-01", "Lab A", "540", "600", "20"], "riga 2")
    assert prenotazione.codice == "PR-01"
    assert isinstance(prenotazione.intervallo, Intervallo)
    assert prenotazione.intervallo.durata_min == 60
    assert prenotazione.partecipanti == 20


def test_riga_a_prenotazione_errori_con_riferimento():
    with pytest.raises(ValueError, match="riga 2"):
        riga_a_prenotazione(["PR-01", "Lab A", "cinque", "600", "20"], "riga 2")
    with pytest.raises(ValueError, match="riga 3"):
        riga_a_prenotazione(["PR-01", "Lab A", "600", "540", "20"], "riga 3")
    with pytest.raises(ValueError, match="attesi 5 campi"):
        riga_a_prenotazione(["PR-01", "Lab A"], "riga 4")


def test_prenotazione_a_riga_proiezione():
    prenotazione = Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20)
    assert prenotazione_a_riga(prenotazione) == ["PR-01", "Lab A", "540", "600", "20"]


# --- PREN-13: round-trip CSV delle prenotazioni -------------------------------


def test_pren_13_round_trip(tmp_path):
    archivio = tmp_path / "prenotazioni.csv"
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    registro.registra(Prenotazione("PR-02", 'Aula "Verde"', Intervallo(600, 660), 18))
    esporta_registro(archivio, registro)

    testo = archivio.read_text(encoding="utf-8")
    assert not testo.startswith("﻿")  # nessun BOM in uscita
    righe = list(csv.reader(testo.splitlines()))
    assert righe[0] == list(CAMPI_PRENOTAZIONE)
    assert righe[2] == ["PR-02", 'Aula "Verde"', "600", "660", "18"]

    altro = RegistroPrenotazioni()
    importa_lotto(archivio, altro)
    assert altro.riepilogo() == registro.riepilogo()
    assert [p.codice for p in altro.prenotazioni()] == ["PR-01", "PR-02"]


def test_pren_13_bom_in_ingresso_ammesso(tmp_path):
    archivio = tmp_path / "con_bom.csv"
    corpo = "\n".join(",".join(riga) for riga in righe_canoniche())
    archivio.write_bytes("﻿".encode() + corpo.encode("utf-8") + b"\n")
    candidati = leggi_candidati(archivio)
    assert [p.codice for p in candidati] == ["PR-01", "PR-02"]


def test_pren_13_intestazione_errata(tmp_path):
    righe = [
        ["codice", "aula", "inizio", "fine", "partecipanti"],
        ["PR-01", "Lab A", "540", "600", "20"],
    ]
    archivio = scrivi_csv(tmp_path / "errata.csv", righe)
    with pytest.raises(ValueError, match="intestazione"):
        leggi_candidati(archivio)


def test_pren_13_file_assente(tmp_path):
    with pytest.raises(FileNotFoundError):
        leggi_candidati(tmp_path / "assente.csv")


def test_pren_13_importazione_rifiutata_conserva_lo_stato(tmp_path):
    archivio = scrivi_csv(
        tmp_path / "lotto.csv",
        [
            ["codice", "aula", "inizio_min", "fine_min", "partecipanti"],
            ["PR-01", "Lab A", "540", "600", "20"],
            ["PR-09", "Lab A", "570", "630", "9"],
        ],
    )
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("XX", "Lab Z", Intervallo(0, 30), 5))
    with pytest.raises(ConflittoPrenotazione):
        importa_lotto(archivio, registro)
    assert [p.codice for p in registro.prenotazioni()] == ["XX"]


# --- PREN-14: esportazione fallita, file precedente integro ---------------------


def test_pren_14_esportazione_fallita_file_precedente_intatto(tmp_path, monkeypatch):
    import csv_prenotazioni_u14 as modulo

    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    destinazione = tmp_path / "esportazione.csv"
    esporta_registro(destinazione, registro)
    precedente = destinazione.read_bytes()

    registro.registra(Prenotazione("PR-02", "Lab A", Intervallo(600, 660), 18))

    def sostituzione_fallita(origine, destinazione):
        raise OSError("sostituzione simulata non riuscita")

    monkeypatch.setattr(modulo.os, "replace", sostituzione_fallita)
    with pytest.raises(OSError, match="sostituzione simulata"):
        esporta_registro(destinazione, registro)
    monkeypatch.undo()
    assert destinazione.read_bytes() == precedente
    assert not any(nome.endswith(".tmp") for nome in (p.name for p in tmp_path.iterdir()))


def test_pren_14_nessun_file_se_la_directory_non_esiste(tmp_path):
    registro = RegistroPrenotazioni()
    with pytest.raises(OSError):
        esporta_registro(tmp_path / "inesistente" / "f.csv", registro)


# --- Magazzino: CSV e JSON --------------------------------------------------------


def archivio_canonico(tmp_path):
    return scrivi_csv(
        tmp_path / "magazzino.csv",
        [
            ["codice", "descrizione", "quantita", "prezzo_centesimi"],
            ["007", "Vite, lunga", "4", "25"],
            ["012", 'Caffè "A"', "2", "350"],
        ],
    )


def test_magazzino_caricamento_schema_e_valori(tmp_path):
    magazzino = carica_magazzino(archivio_canonico(tmp_path))
    assert magazzino.riepilogo() == {"articoli": 2, "quantita_totale": 6, "valore_centesimi": 800}
    trovato = magazzino.cerca("012")
    assert trovato.descrizione == 'Caffè "A"'
    assert magazzino.cerca("7") is None


def test_magazzino_duplicato_in_caricamento(tmp_path):
    archivio = scrivi_csv(
        tmp_path / "dup.csv",
        [
            ["codice", "descrizione", "quantita", "prezzo_centesimi"],
            ["007", "Vite", "4", "25"],
            ["007", "Ancora", "1", "1"],
        ],
    )
    with pytest.raises(ValueError, match="già presente"):
        carica_magazzino(archivio)


def test_magazzino_file_assente_diverso_da_corrotto(tmp_path):
    with pytest.raises(FileNotFoundError):
        carica_magazzino(tmp_path / "nessuno.csv")


def test_magazzino_byte_non_utf8(tmp_path):
    archivio = tmp_path / "non_utf8.csv"
    archivio.write_bytes(b"codice,descrizione,quantita,prezzo_centesimi\n007,\xff\xfe,1,1\n")
    with pytest.raises(UnicodeDecodeError):
        carica_magazzino(archivio)


def test_magazzino_intestazione_errata(tmp_path):
    archivio = scrivi_csv(
        tmp_path / "int_err.csv",
        [
            ["codice", "descrizione", "quantita", "prezzo"],
            ["007", "Vite", "4", "25"],
        ],
    )
    with pytest.raises(ValueError, match="intestazione"):
        carica_magazzino(archivio)


def test_magazzino_intero_non_convertibile(tmp_path):
    archivio = scrivi_csv(
        tmp_path / "int_err.csv",
        [
            ["codice", "descrizione", "quantita", "prezzo_centesimi"],
            ["007", "Vite", "quattro", "25"],
        ],
    )
    with pytest.raises(ValueError, match="non è un intero"):
        carica_magazzino(archivio)


def test_magazzino_lista_vuota(tmp_path):
    archivio = scrivi_csv(
        tmp_path / "vuoto.csv", [["codice", "descrizione", "quantita", "prezzo_centesimi"]]
    )
    assert carica_magazzino(archivio).riepilogo() == {
        "articoli": 0,
        "quantita_totale": 0,
        "valore_centesimi": 0,
    }


def test_magazzino_round_trip_csv_nuove_istanze(tmp_path):
    sorgente = archivio_canonico(tmp_path)
    primo = carica_magazzino(sorgente)
    destinazione = tmp_path / "copia.csv"
    salva_magazzino(destinazione, primo)
    assert destinazione.read_bytes() == sorgente.read_bytes()
    secondo = carica_magazzino(destinazione)
    assert secondo.riepilogo() == primo.riepilogo()
    assert secondo.cerca("007") is not primo.cerca("007")


def test_magazzino_bom_ammesso_in_ingresso(tmp_path):
    archivio = tmp_path / "con_bom.csv"
    archivio.write_bytes(
        "﻿".encode() + b"codice,descrizione,quantita,prezzo_centesimi\n007,Vite,4,25\n"
    )
    assert carica_magazzino(archivio).riepilogo()["articoli"] == 1


def test_magazzino_json_round_trip(tmp_path):
    magazzino = carica_magazzino(archivio_canonico(tmp_path))
    archivio = tmp_path / "magazzino.json"
    salva_magazzino_json(archivio, magazzino)
    dati = json.loads(archivio.read_text(encoding="utf-8"))
    assert dati["versione_schema"] == 1
    assert len(dati["articoli"]) == 2
    ricostruito = carica_magazzino_json(archivio)
    assert ricostruito.riepilogo() == magazzino.riepilogo()


def test_magazzino_json_radice_o_versione_errata():
    with pytest.raises(ValueError, match="versione_schema"):
        json_a_magazzino({"articoli": []})
    with pytest.raises(ValueError, match="radice"):
        json_a_magazzino([1, 2, 3])
    with pytest.raises(ValueError, match="articoli"):
        json_a_magazzino({"versione_schema": 1})


def test_magazzino_json_campo_mancante_o_invalido():
    with pytest.raises(ValueError, match="manca il campo"):
        json_a_magazzino(
            {"versione_schema": 1, "articoli": [{"codice": "007", "descrizione": "x"}]}
        )
    with pytest.raises(ValueError, match="quantita"):
        json_a_magazzino(
            {
                "versione_schema": 1,
                "articoli": [
                    {
                        "codice": "007",
                        "descrizione": "x",
                        "quantita": -1,
                        "prezzo_centesimi": 10,
                    }
                ],
            }
        )


def test_magazzino_salvataggio_fallito_nessun_residuo(tmp_path):
    magazzino = carica_magazzino(archivio_canonico(tmp_path))
    destinazione = tmp_path / "occupata.csv"
    # una directory al posto del file rende la sostituzione impossibile:
    # guasto simulato senza permessi casuali di cartelle reali
    destinazione.mkdir()
    with pytest.raises(OSError):
        salva_magazzino(destinazione, magazzino)
    residui = [p.name for p in tmp_path.iterdir()]
    assert "occupata.csv" in residui
    assert not any(nome.endswith(".tmp") for nome in residui)
    destinazione.rmdir()


def test_magazzino_riepilogo_sul_vuoto():
    assert Magazzino().riepilogo() == {
        "articoli": 0,
        "quantita_totale": 0,
        "valore_centesimi": 0,
    }
