import pytest

from componenti_u15 import (
    EsportatoreTSV,
    PoliticaCongiunzione,
    PoliticaMultipli,
    VistaEtichettata,
    leggi_tsv,
    primo_ammesso,
    primo_uguale_dicotomico,
    primo_uguale_lineare,
    seleziona_con_funzione,
)
from orologi_base_u15 import OrologioDigitale
from politiche_duck_u15 import PoliticaSogliaMinima, seleziona
from rilevazioni_u15 import Rilevazione, dataset
from servizio_rapporto_u15 import ServizioRapporto


def test_multipli():
    assert seleziona([0, 1, 3, 6, -3], PoliticaMultipli(3)) == [0, 3, 6, -3]
    for divisore in [0, -1, True]:
        with pytest.raises(ValueError):
            PoliticaMultipli(divisore)


@pytest.mark.parametrize(
    "valori,minimo,atteso",
    [([4, 8, 8, 12], 8, 1), ([4, 8, 8, 12], 4, 0), ([4, 8, 8, 12], 13, None), ([], 8, None)],
)
def test_primo(valori, minimo, atteso):
    assert primo_ammesso(valori, PoliticaSogliaMinima(minimo)) == atteso


def test_congiunzione_funzione():
    valori = [4, 8, 8, 12, 20, 9, 10]
    combinata = PoliticaCongiunzione(PoliticaSogliaMinima(8), PoliticaMultipli(4))
    assert seleziona(valori, combinata) == [8, 8, 12, 20]
    assert seleziona_con_funzione(valori, lambda valore: valore >= 8 and valore % 4 == 0) == [
        8,
        8,
        12,
        20,
    ]


def test_tsv(tmp_path):
    valori = dataset() + [Rilevazione("Tab\tè", 0)]
    percorso = tmp_path / "rapporto.tsv"
    assert ServizioRapporto(EsportatoreTSV()).genera(valori, percorso) == 5
    assert leggi_tsv(percorso) == valori


def test_wrapper():
    base = OrologioDigitale(8, 15)
    vista = VistaEtichettata(base, "Laboratorio")
    assert vista.avanza(1440) is None
    assert vista.testo() == "08:15"
    assert vista.imposta(12, 0) is None
    assert base.testo() == "12:00"


@pytest.mark.parametrize(
    "valori,cercato,atteso",
    [
        ([], 8, None),
        ([8], 8, 0),
        ([4, 8, 8, 12], 8, 1),
        ([4, 8, 8, 12], 12, 3),
        ([4, 8, 8, 12], 7, None),
        ([4, 8, 8, 12], 13, None),
    ],
)
def test_ricerche(valori, cercato, atteso):
    assert primo_uguale_lineare(valori, cercato) == atteso
    assert primo_uguale_dicotomico(valori, cercato) == atteso
