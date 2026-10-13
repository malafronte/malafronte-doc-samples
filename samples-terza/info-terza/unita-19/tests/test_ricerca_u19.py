"""Prove di ricerca e conteggi — Unità 19."""

import pytest

from btree_modello_u19 import BTreeDidattico
from dati_btree_u19 import costruisci_d1, costruisci_d2_finale


def test_prima_ultima_voce_locale():
    """La ricerca trova prima e ultima voce di un nodo foglia."""
    albero = costruisci_d1()
    assert albero.cerca(5) == "dato-5"
    assert albero.cerca(30) == "dato-30"


def test_voce_interna_senza_discesa():
    """La voce interna `20` si risolve con un solo nodo visitato."""
    esito = costruisci_d1().ricerca_con_conteggi(20)
    assert (esito.trovato, esito.dato, esito.nodi) == (True, "dato-20", 1)


def test_regioni_di_assenza():
    """Assenze sotto il minimo, sopra il massimo e intermedie su D1."""
    albero = costruisci_d1()
    for query in (4, 40, 15):
        with pytest.raises(KeyError):
            albero.cerca(query)
        assert albero.ricerca_con_conteggi(query).trovato is False
    assert albero.ricerca_con_conteggi(4).nodi == 2


def test_dati_falsy():
    """Dati `None`, `0` e `""` legittimi, distinti dall'assenza."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    for chiave, dato in ((1, None), (2, 0), (3, "")):
        albero.inserisci(chiave, dato)
    assert albero.cerca(1) is None and albero.contiene(1) is True
    assert albero.cerca(2) == 0 and albero.cerca(3) == ""


def test_tipo_errato():
    """Chiave di tipo fuori dominio solleva `TypeError`."""
    albero = costruisci_d1()
    with pytest.raises(TypeError):
        albero.cerca("10")
    with pytest.raises(TypeError):
        albero.contiene(10.0)


@pytest.mark.parametrize(
    ("query", "nodi", "confronti"),
    [(4, 1, 2), (10, 3, 6), (0, 3, 6), (11, 3, 5)],
)
def test_conteggi_d2(query, nodi, confronti):
    """I conteggi su D2 seguono la convenzione del capitolo."""
    esito = costruisci_d2_finale().ricerca_con_conteggi(query)
    assert (esito.nodi, esito.confronti) == (nodi, confronti)


def test_ricerca_pura():
    """La ricerca conserva lo stato: voci e dimensione invariati."""
    albero = costruisci_d2_finale()
    prima = albero.voci_ordinate()
    for query in (4, 10, 0, 11):
        try:
            albero.cerca(query)
        except KeyError:
            pass
    assert albero.voci_ordinate() == prima
    assert len(albero) == 10
