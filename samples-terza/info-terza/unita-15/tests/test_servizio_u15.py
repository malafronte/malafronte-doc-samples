import pytest

import cli_rapporto_u15 as cli
from rilevazioni_u15 import dataset
from servizio_rapporto_u15 import EsportatoreMemoria, ServizioRapporto


def test_memoria(tmp_path):
    uno, due = EsportatoreMemoria(), EsportatoreMemoria()
    dati = dataset()
    prima = list(dati)
    percorso = tmp_path / "rapporto"
    assert ServizioRapporto(uno).genera(dati, percorso) == 4
    assert uno.chiamate == 1
    assert uno.record[0] == {"codice": "007", "valore": 18, "unita": "°C"}
    assert uno.percorso == percorso
    assert due.chiamate == 0
    assert dati == prima
    assert not percorso.exists()
    assert ServizioRapporto(due).genera([], percorso) == 0
    assert due.record == []


def test_errore_prima_delega(tmp_path):
    memoria = EsportatoreMemoria()
    servizio = ServizioRapporto(memoria)
    with pytest.raises(ValueError):
        servizio.genera(["errato"], tmp_path / "rapporto")
    assert memoria.chiamate == 0


@pytest.mark.parametrize("formato", ["csv", "json"])
def test_cli_successo(tmp_path, monkeypatch, capsys, formato):
    richieste = iter([formato, str(tmp_path / "rapporto")])
    monkeypatch.setattr("builtins.input", lambda prompt: next(richieste))
    assert cli.main() == 0
    assert capsys.readouterr().out == "rilevazioni esportate: 4\n"


@pytest.mark.parametrize("formato", ["csv", "json"])
def test_cli_guasto(tmp_path, monkeypatch, capsys, formato):
    richieste = iter([formato, str(tmp_path / "rapporto")])
    monkeypatch.setattr("builtins.input", lambda prompt: next(richieste))

    def guasto(self, rilevazioni, percorso):
        raise OSError("guasto controllato")

    monkeypatch.setattr(cli.ServizioRapporto, "genera", guasto)
    assert cli.main() == 1
    messaggio = capsys.readouterr().out
    assert "esportazione fallita" in messaggio
    assert "rilevazioni esportate:" not in messaggio
