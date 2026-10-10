from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import esportatori_u15 as formati
from rilevazioni_u15 import Rilevazione, dataset, rilevazione_da_record

FORMATI = [
    (formati.EsportatoreCSV, formati.leggi_csv),
    (formati.EsportatoreJSON, formati.leggi_json),
]


@pytest.mark.parametrize(
    "nome,leggi", [("rilevazioni.csv", formati.leggi_csv), ("rilevazioni.json", formati.leggi_json)]
)
def test_fixture_dataset(nome, leggi):
    directory = Path(__file__).resolve().parents[1] / "dati"
    assert leggi(directory / nome) == dataset()


@pytest.mark.parametrize(
    "nome,leggi",
    [("valore-testuale.csv", formati.leggi_csv), ("valore-booleano.json", formati.leggi_json)],
)
def test_fixture_invalida(nome, leggi):
    directory = Path(__file__).resolve().parents[1] / "dati" / "casi-invalidi"
    with pytest.raises(ValueError):
        leggi(directory / nome)


@pytest.mark.parametrize("classe,leggi", FORMATI)
@pytest.mark.parametrize(
    "rilevazioni", [dataset(), [], [Rilevazione("007", 0), Rilevazione("è", -5)]]
)
def test_round_trip(tmp_path, classe, leggi, rilevazioni):
    percorso = tmp_path / "rapporto"
    prima = list(rilevazioni)
    assert classe().esporta(rilevazioni, percorso) is None
    assert leggi(percorso) == rilevazioni
    assert rilevazioni == prima
    assert not percorso.read_bytes().startswith(b"\xef\xbb\xbf")
    assert list(tmp_path.glob(".rapporto-*.tmp")) == []


@pytest.mark.parametrize("classe,leggi", FORMATI)
@pytest.mark.parametrize("fase", ["scrittura", "sostituzione"])
def test_guasto(tmp_path, monkeypatch, classe, leggi, fase):
    percorso = tmp_path / "rapporto"
    classe().esporta(dataset(), percorso)
    prima = percorso.read_bytes()

    def guasto(*argomenti, **opzioni):
        raise OSError("guasto deterministico")

    if fase == "scrittura":
        nome = "scrivi_csv" if classe is formati.EsportatoreCSV else "scrivi_json"
        monkeypatch.setattr(formati, nome, guasto)
    else:
        monkeypatch.setattr(Path, "replace", guasto)
    with pytest.raises(OSError, match="guasto deterministico"):
        classe().esporta(dataset(), percorso)
    assert percorso.read_bytes() == prima
    assert leggi(percorso) == dataset()
    assert list(tmp_path.glob(".rapporto-*.tmp")) == []


@pytest.mark.parametrize("classe,leggi", FORMATI)
def test_dato_e_cartella_invalidi(tmp_path, classe, leggi):
    percorso = tmp_path / "rapporto"
    percorso.write_bytes(b"precedente")
    with pytest.raises(ValueError):
        classe().esporta(["errato"], percorso)
    assert percorso.read_bytes() == b"precedente"
    with pytest.raises(OSError):
        classe().esporta(dataset(), tmp_path / "assente" / "rapporto")


@pytest.mark.parametrize(
    "codice,valore,unita", [("", 0, "°C"), (" ", 0, "°C"), ("007", True, "°C"), ("007", 0, "K")]
)
def test_modello(codice, valore, unita):
    with pytest.raises(ValueError):
        Rilevazione(codice, valore, unita)


def test_schema_frozen(tmp_path):
    with pytest.raises(FrozenInstanceError):
        dataset()[0].valore = 19
    for record in [
        {},
        {"codice": "007", "valore": True, "unita": "°C"},
        {"codice": "007", "valore": 0, "unita": "°C", "extra": 0},
    ]:
        with pytest.raises(ValueError):
            rilevazione_da_record(record)
    percorso = tmp_path / "errato.csv"
    percorso.write_text("codice,valore,unita\n007,no,°C\n", encoding="utf-8")
    with pytest.raises(ValueError, match="riga 2"):
        formati.leggi_csv(percorso)
