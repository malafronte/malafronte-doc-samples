"""Prove di costruzione e simulazioni — Unità 19."""

import random

import pytest

from btree_costruzione_u19 import costruisci_btree_riferimento, traccia_inserimenti
from btree_modello_u19 import BTreeDidattico
from dati_btree_u19 import costruisci_d1, costruisci_d2_finale
from simulazioni_btree_u19 import SCENARI, applica_scenario, nomi_scenari, verifica_d5


def test_d2_dopo_ogni_inserimento():
    """Gli stati intermedi di D2 seguono la tabella canonica del capitolo."""
    attese = [
        (1, [1], 0),
        (2, [1, 2], 0),
        (3, [1, 2, 3], 0),
        (4, [2], 1),
        (5, [2], 1),
        (6, [2, 4], 1),
        (7, [2, 4], 1),
        (8, [2, 4, 6], 1),
        (9, [2, 4, 6], 1),
        (10, [4], 2),
    ]
    inserimenti = traccia_inserimenti(range(1, 11))
    for passo, (chiave, radice, altezza) in zip(inserimenti, attese, strict=True):
        assert passo["dopo"] == chiave
        assert passo["radice"] == radice
        assert passo["altezza"] == altezza


def test_split_interno_e_radice():
    """L'inserimento di `10` divide foglia, padre e vecchia radice."""
    finale = costruisci_d2_finale()
    assert finale.radice.figli[1].chiavi() == [6, 8]
    assert finale.radice.figli[1].figli[2].chiavi() == [9, 10]


def test_duplicato_rifiutato():
    """Chiavi duplicate sollevano `ValueError` con stato conservato."""
    with pytest.raises(ValueError):
        costruisci_btree_riferimento([(1, "a"), (2, "b"), (1, "c")])
    albero = costruisci_d1()
    with pytest.raises(ValueError):
        albero.inserisci(10, "altro")
    assert len(albero) == 8


def test_ordine_inverso_e_mescolato():
    """Ordine inverso e mescolato riproducibile danno insiemi ordinati uguali."""
    voci = [(chiave, f"dato-{chiave}") for chiave in range(1, 21)]
    inverso = costruisci_btree_riferimento(list(reversed(voci)))
    mescolate = list(voci)
    random.Random(19).shuffle(mescolate)
    mescolato = costruisci_btree_riferimento(mescolate)
    assert [c for c, _d in inverso.voci_ordinate()] == [c for c, _d in mescolato.voci_ordinate()]


def test_tutti_gli_scenari():
    """Ogni scenario di cancellazione raggiunge la fotografia attesa."""
    assert set(nomi_scenari()) == {nome for nome, _c, _ch, _a, _h in SCENARI}
    for nome in nomi_scenari():
        assert applica_scenario(nome)["coerente"] is True


def test_d5_figlio_trasferito():
    """D5 trasferisce il figlio `[35]` nel nuovo intervallo del destro."""
    assert verifica_d5()["coerente"] is True


def test_assente_conserva_stato():
    """Una chiave assente solleva `KeyError` e conserva lo stato."""
    albero = costruisci_d1()
    with pytest.raises(KeyError):
        albero.rimuovi(999)
    albero.controlla_invarianti()
    assert len(albero) == 8


def test_ritorno_al_vuoto():
    """La rimozione di tutte le chiavi riporta al vuoto con altezza -1."""
    albero = costruisci_d2_finale()
    for chiave in range(1, 11):
        albero.rimuovi(chiave)
        albero.controlla_invarianti()
    assert len(albero) == 0
    assert albero.altezza() == -1


def test_sequenze_riproducibili():
    """Trenta sequenze di inserimento e rimozione conservano gli invarianti."""
    generatore = random.Random(19)
    for _prova in range(30):
        albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
        chiavi = list(range(1, 46))
        generatore.shuffle(chiavi)
        presenti = set()
        for chiave in chiavi:
            if chiave % 3:
                albero.inserisci(chiave, f"dato-{chiave}")
                presenti.add(chiave)
            albero.controlla_invarianti()
        for chiave in sorted(presenti):
            albero.rimuovi(chiave)
            albero.controlla_invarianti()
        assert len(albero) == 0
