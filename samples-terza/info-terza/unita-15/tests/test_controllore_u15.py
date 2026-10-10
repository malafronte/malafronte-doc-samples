import pytest

from controllore_adattatori_u15 import (
    AttuatoreSimulato,
    Controllore,
    ControlloreIsteresi,
    LetturaEsaurita,
    SensoreCelsius,
    SensoreDecimi,
)


@pytest.mark.parametrize("sensore", [SensoreCelsius([18, 20, 22]), SensoreDecimi([180, 200, 220])])
def test_comune(sensore):
    attuatore = AttuatoreSimulato()
    controllore = Controllore(sensore, attuatore, 20)
    assert not attuatore.acceso
    stati = []
    for indice in range(3):
        assert controllore.passo() is None
        stati.append(attuatore.acceso)
        assert controllore.passi == indice + 1
    assert stati == [True, False, False]
    with pytest.raises(LetturaEsaurita):
        controllore.passo()
    assert controllore.passi == 3
    assert not attuatore.acceso
    assert sensore.consumate == 3


@pytest.mark.parametrize("classe", [SensoreCelsius, SensoreDecimi])
@pytest.mark.parametrize("invalido", [True, "20", float("nan"), float("inf")])
def test_errore_conserva_attuatore(classe, invalido):
    sensore = classe([invalido])
    attuatore = AttuatoreSimulato()
    attuatore.accendi()
    controllore = Controllore(sensore, attuatore, 20)
    with pytest.raises(ValueError):
        controllore.passo()
    assert attuatore.acceso
    assert controllore.passi == 0
    assert sensore.consumate == 1


def test_conversione_e_copia():
    origine = [180, 200, 220]
    sensore = SensoreDecimi(origine)
    origine[0] = 0
    assert [sensore.leggi() for _ in range(3)] == [18.0, 20.0, 22.0]
    with pytest.raises(ValueError):
        SensoreDecimi([18.5]).leggi()


def test_isteresi():
    sensore = SensoreCelsius([17, 18, 20, 22, 21, 17, "errato"])
    attuatore = AttuatoreSimulato()
    controllore = ControlloreIsteresi(sensore, attuatore, 18, 22)
    stati = []
    for _ in range(6):
        controllore.passo()
        stati.append(attuatore.acceso)
    assert stati == [True, True, True, False, False, True]
    with pytest.raises(ValueError):
        controllore.passo()
    assert attuatore.acceso
    assert controllore.passi == 6
    with pytest.raises(LetturaEsaurita):
        controllore.passo()
    with pytest.raises(ValueError):
        ControlloreIsteresi(sensore, attuatore, 22, 18)
