import pytest

from soglia_algoritmi_u15 import da_soglia_dicotomica, da_soglia_scansione


@pytest.mark.parametrize("valori", [[], [8], [4, 8, 8, 12, 20], [-3, -3, 0, 8]])
@pytest.mark.parametrize("minimo", [-4, 4, 8, 12, 20, 21])
def test_equivalenza(valori, minimo):
    prima = list(valori)
    atteso = [valore for valore in valori if valore >= minimo]
    for algoritmo in [da_soglia_scansione, da_soglia_dicotomica]:
        risultato = algoritmo(valori, minimo)
        assert risultato == atteso
        assert risultato is not valori
        assert valori == prima


@pytest.mark.parametrize("algoritmo", [da_soglia_scansione, da_soglia_dicotomica])
@pytest.mark.parametrize("valori,minimo", [([8, 4], 8), ([True], 8), ([8], True), (["8"], 8)])
def test_precondizione(algoritmo, valori, minimo):
    with pytest.raises(ValueError):
        algoritmo(valori, minimo)
