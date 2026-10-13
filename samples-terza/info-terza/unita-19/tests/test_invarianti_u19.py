"""Prove degli invarianti e del controllo — Unità 19."""

import pytest

from btree_modello_u19 import BTreeDidattico, NodoBTree
from dati_btree_u19 import costruisci_d1


def test_vuoto_e_radice_singola():
    """Vuoto con altezza -1 e radice foglia con altezza 0 superano il controllo."""
    vuoto = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    vuoto.controlla_invarianti()
    assert vuoto.altezza() == -1
    singolo = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    singolo.inserisci(7, "dato-7")
    singolo.controlla_invarianti()
    assert singolo.altezza() == 0


def test_grado_minimo_terzo():
    """Stati con `t = 3` rispettano occupazione da due a cinque voci."""
    albero = BTreeDidattico(grado_minimo=3, tipo_chiave=int)
    for chiave in range(1, 13):
        albero.inserisci(chiave, f"dato-{chiave}")
    albero.controlla_invarianti()
    assert [chiave for chiave, _dato in albero.voci_ordinate()] == list(range(1, 13))


def test_liste_indipendenti():
    """Nodi diversi non condividono le liste di voci e figli."""
    primo = NodoBTree([(1, "a")], [])
    secondo = NodoBTree([(1, "a")], [])
    primo.voci.append((2, "b"))
    assert secondo.chiavi() == [1]


def test_figli_diversi_da_k_piu_uno():
    """Un nodo interno senza `k + 1` figli viola il controllo."""
    albero = costruisci_d1()
    albero.radice.figli.pop()
    with pytest.raises(AssertionError, match="figli"):
        albero.controlla_invarianti()


def test_occupazione_minima_sulla_radice():
    """La regola minima non si applica alla radice con una sola voce."""
    albero = BTreeDidattico(grado_minimo=3, tipo_chiave=int)
    albero.inserisci(5, "dato-5")
    albero.controlla_invarianti()


def test_riferimento_condiviso():
    """Lo stesso nodo raggiunto due volte viene diagnosticato."""
    albero = costruisci_d1()
    albero.radice.figli[1] = albero.radice.figli[0]
    with pytest.raises(AssertionError, match="due volte"):
        albero.controlla_invarianti()


def test_ciclo_intenzionale():
    """Un ciclo nelle fixture corrotte termina con una diagnosi."""
    albero = costruisci_d1()
    albero.radice.figli[0].figli = [albero.radice]
    with pytest.raises(AssertionError):
        albero.controlla_invarianti()
