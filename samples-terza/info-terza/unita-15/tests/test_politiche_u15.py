import pytest

import politiche_abc_u15 as abc
import politiche_duck_u15 as duck
import politiche_protocol_u15 as protocol


@pytest.mark.parametrize("modulo", [duck, abc])
@pytest.mark.parametrize(
    "valori,atteso", [([], []), ([7, 8, 12, 13], [8, 12]), ([8, 8, 4, 12], [8, 8, 12])]
)
def test_comune(modulo, valori, atteso):
    politica = modulo.PoliticaIntervallo(8, 12)
    prima = list(valori)
    configurazione = vars(politica).copy()
    risultato = duck.seleziona(valori, politica)
    assert risultato == atteso
    assert risultato is not valori
    assert valori == prima
    assert duck.seleziona(valori, politica) == atteso
    assert vars(politica) == configurazione
    assert type(politica.ammette(8)) is bool


@pytest.mark.parametrize("modulo", [duck, abc])
def test_specifici(modulo):
    valori = [4, 8, 8, 12, 20]
    assert duck.seleziona(valori, modulo.PoliticaSogliaMinima(8)) == [8, 8, 12, 20]
    assert duck.seleziona(valori, modulo.PoliticaIntervallo(8, 12)) == [8, 8, 12]
    assert duck.seleziona(valori, modulo.PoliticaIntervallo(8, 8)) == [8, 8]


@pytest.mark.parametrize("modulo", [duck, abc])
@pytest.mark.parametrize("invalido", [True, "8", 2.5, None])
def test_invalidi(modulo, invalido):
    with pytest.raises(ValueError):
        modulo.PoliticaSogliaMinima(invalido)
    with pytest.raises(ValueError):
        modulo.PoliticaIntervallo(0, invalido)
    with pytest.raises(ValueError):
        modulo.PoliticaIntervallo(12, 8)
    politica = modulo.PoliticaSogliaMinima(8)
    valori = [8, invalido]
    with pytest.raises(ValueError):
        duck.seleziona(valori, politica)
    assert valori == [8, invalido]
    with pytest.raises(ValueError):
        politica.ammette(invalido)


def test_validazione_prima_della_delega():
    class Spia:
        def __init__(self):
            self.chiamate = 0

        def ammette(self, valore):
            self.chiamate += 1
            return True

    spia = Spia()
    with pytest.raises(ValueError):
        duck.seleziona([8, True], spia)
    assert spia.chiamate == 0


def test_abc_protocol_e_limiti():
    class Incompleta(abc.PoliticaSelezione):
        pass

    for classe in [abc.PoliticaSelezione, Incompleta]:
        with pytest.raises(TypeError):
            classe()

    class FirmaErrata:
        def ammette(self, valore, limite):
            return valore >= limite

    class TestoErrato:
        def ammette(self, valore):
            return "no"

    errata = FirmaErrata()
    assert isinstance(errata, protocol.PoliticaSelezione)
    with pytest.raises(TypeError):
        duck.seleziona([8], errata)
    with pytest.raises(TypeError):
        duck.seleziona([8], TestoErrato())
    assert protocol.seleziona([4, 8], protocol.SogliaAutonoma(8)) == [8]
