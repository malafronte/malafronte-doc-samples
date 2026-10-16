"""Regressioni sull'infrastruttura CLI, senza completare gli algoritmi assegnati."""

from pathlib import Path

from frattali import __main__ as comandi


def test_stato_fornito_termina_senza_generare(monkeypatch, capsys) -> None:
    monkeypatch.setattr(comandi, "operazioni_stato", lambda: {"esempio": False})
    assert comandi.main(["stato"]) == 0
    assert "Operazioni da completare: 1 su 1." in capsys.readouterr().out


def test_genera_incompleto_non_scrive_png(monkeypatch, tmp_path, capsys) -> None:
    # Il sostituto mantiene valida la prova anche dopo il completamento del progetto.
    def incompleta(percorso):
        raise NotImplementedError("immagine_da_configurazione da completare")

    monkeypatch.setattr(comandi, "immagine_da_configurazione", incompleta)
    destinazione = tmp_path / "assente.png"
    assert comandi.main(["genera", "--config", "assente.json", "--png", str(destinazione)]) == 2
    assert not destinazione.exists()
    assert "immagine_da_configurazione" in capsys.readouterr().out


def test_genera_collega_risultato_e_destinazione(monkeypatch, tmp_path, capsys) -> None:
    from frattali.rendering import immagini

    immagine = object()
    chiamate = []

    def prepara(percorso):
        chiamate.append(("prepara", percorso))
        return immagine

    def salva(risultato, percorso):
        chiamate.append(("salva", risultato, percorso))
        return Path(percorso)

    monkeypatch.setattr(comandi, "immagine_da_configurazione", prepara)
    monkeypatch.setattr(immagini, "salva_png", salva)
    destinazione = str(tmp_path / "risultato.png")
    assert comandi.main(["genera", "--config", "julia.json", "--png", destinazione]) == 0
    assert chiamate == [("prepara", "julia.json"), ("salva", immagine, destinazione)]
    assert f"Immagine scritta in {destinazione}." in capsys.readouterr().out
