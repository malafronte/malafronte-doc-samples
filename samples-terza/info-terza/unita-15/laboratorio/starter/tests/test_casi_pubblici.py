"""Suite DELIBERATAMENTE non soddisfatta dallo starter; fuori da testpaths."""

from pathlib import Path

import pytest

from componenti_starter import (
    EsportatoreMemoriaLaboratorio,
    PoliticaIntervalloLaboratorio,
    genera_rapporto,
    seleziona_rilevazioni,
)
from politiche_duck_u15 import PoliticaSogliaMinima
from rilevazioni_u15 import dataset, proiezioni


def test_client_iniziale():
    dati = dataset()
    prima = list(dati)
    risultato = seleziona_rilevazioni(dati, PoliticaSogliaMinima(18))
    assert [r.codice for r in risultato] == ["007", "Lab, A", "007"]
    assert risultato is not dati and dati == prima


def test_intervallo_l03():
    politica = PoliticaIntervalloLaboratorio(-2, 18)
    risultato = seleziona_rilevazioni(dataset(), politica)
    assert [r.valore for r in risultato] == [18, -2, 18]
    assert politica.ammette(-2) is True and politica.ammette(18) is True
    assert politica.ammette(19) is False


def test_errori_l03():
    with pytest.raises(ValueError):
        PoliticaIntervalloLaboratorio(18, -2)
    with pytest.raises(ValueError):
        PoliticaIntervalloLaboratorio(-2, 18).ammette(True)


def test_delega_l05():
    dati = dataset()
    prima = list(dati)
    esportatore = EsportatoreMemoriaLaboratorio()
    percorso = Path("rapporto.csv")
    assert genera_rapporto(dati, PoliticaSogliaMinima(18), esportatore, percorso) == 3
    assert esportatore.chiamate == 1 and esportatore.percorso == percorso
    assert esportatore.record == proiezioni([dati[0], dati[1], dati[3]])
    assert dati == prima
