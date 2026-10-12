"""Prove sul sondaggio lineare e sul confronto delle strategie — Unità 18.

Casi del piano §§5.5, I e M: occupazione delle posizioni 5, 6, 0, ricerca
fallita con arresto allo spazio mai usato, cancellazione con marcatore,
aggiornamento oltre il marcatore, riuso del marcatore, limite del sondaggio
ed equivalenza logica delle strategie confrontate.
"""

import pytest

from confronto_indici_u18 import (
    confronta_strategie,
    costruisci_tabella,
    misura_secondi,
    ricerca_dicotomica,
    ricerca_lineare,
)
from tracce_sondaggio_u18 import CANCELLATA, OCCUPATA, VUOTA, SondaggioLineare, traccia_canonica


def tabella_sondaggio_canonica():
    tabella = SondaggioLineare(7)
    tabella.inserisci(5, "E5")
    tabella.inserisci(12, "E12")
    tabella.inserisci(19, "E19")
    return tabella


def test_inserimenti_occupano_5_6_0():
    tabella = tabella_sondaggio_canonica()
    foto = tabella.fotografia()
    assert foto[5] == (OCCUPATA, 5, "E5")
    assert foto[6] == (OCCUPATA, 12, "E12")
    assert foto[0] == (OCCUPATA, 19, "E19")
    assert len(tabella) == 3


def test_ricerca_19_attraversa_tre_sonde():
    tabella = tabella_sondaggio_canonica()
    assert tabella.cerca(19) == "E19"
    assert tabella.sonde_per(19)[:4] == [5, 6, 0, 1]


def test_ricerca_fallita_conclude_allo_spazio_mai_usato():
    tabella = tabella_sondaggio_canonica()
    with pytest.raises(KeyError):
        tabella.cerca(26)
    assert tabella.sonde_per(26)[:4] == [5, 6, 0, 1]
    assert tabella.fotografia()[1][0] == VUOTA


def test_cancellazione_con_marcatori_e_continuita():
    tabella = tabella_sondaggio_canonica()
    assert tabella.rimuovi(12) == "E12"
    assert tabella.fotografia()[6][0] == CANCELLATA
    assert len(tabella) == 2
    assert tabella.marcatori == 1
    assert tabella.cerca(19) == "E19"
    with pytest.raises(KeyError):
        tabella.rimuovi(12)


def test_aggiornamento_oltre_il_marcatore():
    tabella = tabella_sondaggio_canonica()
    tabella.rimuovi(12)
    tabella.inserisci(19, "E19b")
    assert tabella.cerca(19) == "E19b"
    assert len(tabella) == 2


def test_chiave_nuova_riusa_il_marcatore_dopo_verifica():
    tabella = tabella_sondaggio_canonica()
    tabella.rimuovi(12)
    tabella.inserisci(26, "E26")
    assert tabella.cerca(26) == "E26"
    assert tabella.fotografia()[6] == (OCCUPATA, 26, "E26")
    assert len(tabella) == 3
    assert tabella.marcatori == 0


def test_limite_del_sondaggio_e_tabella_piena():
    tabella = SondaggioLineare(3)
    tabella.inserisci(0, "a")
    tabella.inserisci(1, "b")
    tabella.inserisci(2, "c")
    with pytest.raises(OverflowError):
        tabella.inserisci(3, "d")
    assert len(tabella.sonde_per(9)) == 3


def test_traccia_canonica():
    traccia = traccia_canonica()
    assert traccia["sonde_19"] == [5, 6, 0]
    assert traccia["valore_19_oltre_marcatore"] == "E19"
    assert traccia["valore_19_aggiornato"] == "E19b"


def test_ricerca_lineare_e_dicotomica():
    raccolta = [(12, "A"), (7, "B"), (22, "C"), (17, "D")]
    assert ricerca_lineare(raccolta, 7) == (1, 2)
    assert ricerca_lineare(raccolta, 99) == (None, 4)
    ordinata = sorted(raccolta)
    posizione, _confronti = ricerca_dicotomica(ordinata, 17)
    assert ordinata[posizione][0] == 17


def test_confronto_strategie_stessi_esiti_logici():
    coppie = [(12, "A"), (7, "B"), (22, "C"), (17, "D")]
    righe = confronta_strategie(coppie, [7, 12, 27, 4], 5)
    assert len(righe) == 16
    for chiave in (7, 12, 27, 4):
        esiti = {riga["strategia"]: riga["trovato"] for riga in righe if riga["query"] == chiave}
        assert esiti["scansione"] == esiti["dicotomica"] == esiti["hash"] == esiti["dict"]
    concentrata = costruisci_tabella([(2 + 5 * j, f"V{j}") for j in range(4)], 5)
    assert concentrata.lunghezze_bucket() == [0, 0, 4, 0, 0]


def test_misura_secondi():
    risultato, secondi = misura_secondi(lambda: 2 + 2, ripetizioni=3)
    assert risultato == 4
    assert secondi >= 0
    with pytest.raises(ValueError):
        misura_secondi(lambda: None, ripetizioni=0)
