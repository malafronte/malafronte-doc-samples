"""Prove del controllore simulato: sequenza, esaurimento, dato invalido (U14).

Niente attese, casualità o GPIO: la sequenza è deterministica. Si verifica
anche l'ordine lettura → decisione → aggiornamento: un'esaurimento o una
lettura invalida non toccano l'attuatore prima della diagnosi.
"""

import pytest
from controllore_simulato_u14 import (
    AttuatoreSimulato,
    Controllore,
    LetturaEsaurita,
    SensoreSimulato,
)


def costruisci(sequenza, soglia=20):
    sensore = SensoreSimulato(sequenza)
    attuatore = AttuatoreSimulato()
    controllore = Controllore(sensore, attuatore, soglia=soglia)
    return sensore, attuatore, controllore


def test_sequenza_canonica_acceso_spento_spento():
    _, attuatore, controllore = costruisci([18, 20, 22])
    stati = []
    for _ in range(3):
        controllore.passo()
        stati.append(attuatore.acceso)
    assert stati == [True, False, False]
    assert controllore.passi == 3


def test_soglia_stretta_minore_della_soglia_accende():
    _, attuatore, controllore = costruisci([19.9], soglia=20)
    controllore.passo()
    assert attuatore.acceso is True


def test_esecuzione_finita():
    _, attuatore, controllore = costruisci([15, 25, 15, 25])
    controllore.esegui(4)
    assert controllore.passi == 4
    assert attuatore.acceso is False  # ultima lettura 25: spento


def test_esaurimento_segnalato_e_attuatore_non_toccato():
    _, attuatore, controllore = costruisci([15])
    controllore.passo()
    assert attuatore.acceso is True
    with pytest.raises(LetturaEsaurita):
        controllore.passo()
    assert attuatore.acceso is True  # nessun aggiornamento prima della diagnosi
    assert controllore.passi == 1


def test_lettura_invalida_valueerror_attuatore_non_toccato():
    attuatore = AttuatoreSimulato()
    attuatore.accendi()
    controllore = Controllore(SensoreSimulato([True]), attuatore, soglia=20)
    with pytest.raises(ValueError):
        controllore.passo()
    assert attuatore.acceso is True
    assert controllore.passi == 0


def test_lettura_invalida_nel_mezzo_della_sequenza():
    _, attuatore, controllore = costruisci([18, "ventidue"])
    controllore.passo()
    assert attuatore.acceso is True
    with pytest.raises(ValueError):
        controllore.passo()
    assert attuatore.acceso is True


def test_due_sensori_indipendenti():
    _, attuatore_a, controllore_a = costruisci([18])
    _, attuatore_b, controllore_b = costruisci([25])
    controllore_a.passo()
    controllore_b.passo()
    assert attuatore_a.acceso is True
    assert attuatore_b.acceso is False


def test_soglia_invalida_rifiutata():
    with pytest.raises(ValueError):
        Controllore(SensoreSimulato([1]), AttuatoreSimulato(), soglia=True)


def test_attuatore_parte_spento():
    assert AttuatoreSimulato().acceso is False
