"""Prove sulle operazioni del BST — Unità 17, cap. PY-33.

Casi semantici del piano §15.1: ricerca presente/assente, estremi,
dominio e bool, dati falsi presenti, inserimento e aggiornamento,
duplicato conservativo, cancellazione con le fixture del §4.4.
"""

import pytest

from bst_u17 import AlberoBST, costruisci_da_inserimenti

D1 = [40, 20, 60, 10, 30, 50, 70, 25, 35, 55]


def albero_d1(dati=None):
    return costruisci_da_inserimenti(D1, dati)


def test_albero_vuoto_e_nodo_unico():
    albero = AlberoBST()
    assert len(albero) == 0
    assert albero.preordine() == []
    assert albero.inordine() == []
    assert albero.postordine() == []
    assert albero.voci_ordinate() == []
    assert albero.altezza() == -1
    assert albero.contiene(10) is False
    assert albero.intervallo(0, 100) == []

    albero.inserisci(40, "radice")
    assert len(albero) == 1
    assert albero.altezza() == 0
    assert albero.minimo() == 40
    assert albero.massimo() == 40
    assert albero.cerca(40) == "radice"

    assert albero.rimuovi(40) is True
    assert len(albero) == 0
    assert albero.altezza() == -1
    with pytest.raises(IndexError):
        albero.minimo()
    with pytest.raises(IndexError):
        albero.massimo()


def test_d1_costruzione_visite_ed_estremi():
    albero = albero_d1()
    assert len(albero) == 10
    assert albero.altezza() == 3
    assert albero.preordine() == [40, 20, 10, 30, 25, 35, 60, 50, 55, 70]
    assert albero.inordine() == [10, 20, 25, 30, 35, 40, 50, 55, 60, 70]
    assert albero.postordine() == [10, 25, 35, 30, 20, 55, 50, 70, 60, 40]
    assert albero.minimo() == 10
    assert albero.massimo() == 70


def test_ricerca_presente_e_assente():
    albero = albero_d1()
    assert albero.contiene(35) is True
    assert albero.cerca(35) == 35
    assert albero.contiene(52) is False
    with pytest.raises(KeyError):
        albero.cerca(52)


def test_dati_falsi_sono_dati_validi():
    albero = AlberoBST()
    albero.inserisci(1, None)
    albero.inserisci(2, 0)
    albero.inserisci(3, False)
    albero.inserisci(4, "")
    assert albero.cerca(1) is None
    assert albero.cerca(2) == 0
    assert albero.cerca(3) is False
    assert albero.cerca(4) == ""
    assert albero.contiene(1) is True
    assert albero.voci_ordinate() == [(1, None), (2, 0), (3, False), (4, "")]


def test_dominio_delle_chiavi():
    albero = AlberoBST()
    with pytest.raises(TypeError):
        albero.inserisci(True, "bool")
    with pytest.raises(TypeError):
        albero.inserisci(3.5, "float")
    with pytest.raises(TypeError):
        albero.inserisci("3", "stringa")
    with pytest.raises(TypeError):
        albero.contiene(False)
    # Il controllo degli argomenti è osservabile anche sull'albero vuoto.
    with pytest.raises(TypeError):
        albero.intervallo(0, "10")
    assert len(albero) == 0


def test_duplicato_rifiutato_e_stato_conservato():
    albero = albero_d1()
    forma_prima = albero.preordine()
    with pytest.raises(ValueError):
        albero.inserisci(30, "duplicato")
    assert len(albero) == 10
    assert albero.cerca(30) == 30
    assert albero.preordine() == forma_prima


def test_aggiornamento_modifica_il_dato_senza_crescere():
    albero = albero_d1()
    albero.aggiorna(30, "titolo nuovo")
    assert len(albero) == 10
    assert albero.cerca(30) == "titolo nuovo"
    assert albero.inordine() == [10, 20, 25, 30, 35, 40, 50, 55, 60, 70]
    with pytest.raises(KeyError):
        albero.aggiorna(52, "assente")
    assert len(albero) == 10


def test_cancellazione_foglia():
    albero = albero_d1()
    assert albero.rimuovi(10) is True
    assert len(albero) == 9
    assert albero.preordine() == [40, 20, 30, 25, 35, 60, 50, 55, 70]
    assert albero.contiene(10) is False
    assert albero.voci_ordinate()[0] == (20, 20)


def test_cancellazione_con_un_figlio():
    albero = albero_d1()
    assert albero.rimuovi(50) is True
    assert len(albero) == 9
    # Il figlio destro 55 resta raggiungibile al posto del padre.
    assert albero.preordine() == [40, 20, 10, 30, 25, 35, 60, 55, 70]
    assert albero.cerca(55) == 55


def test_cancellazione_con_due_figli_successore_profondo():
    albero = albero_d1()
    assert albero.rimuovi(40) is True
    assert len(albero) == 9
    # Il successore inordine di 40 è 50: chiave e dato sostituiscono la
    # radice, mentre 55 resta raggiungibile tramite 60.sinistro.
    assert albero.preordine() == [50, 20, 10, 30, 25, 35, 60, 55, 70]
    assert albero.inordine() == [10, 20, 25, 30, 35, 50, 55, 60, 70]
    assert albero.voci_ordinate() == [
        (10, 10),
        (20, 20),
        (25, 25),
        (30, 30),
        (35, 35),
        (50, 50),
        (55, 55),
        (60, 60),
        (70, 70),
    ]


def test_cancellazione_successore_immediato_con_figlio():
    albero = costruisci_da_inserimenti([40, 20, 60, 70])
    assert albero.rimuovi(40) is True
    assert len(albero) == 3
    assert albero.preordine() == [60, 20, 70]
    assert albero.inordine() == [20, 60, 70]


def test_cancellazione_radice_con_un_figlio():
    albero = costruisci_da_inserimenti([40, 20])
    assert albero.rimuovi(40) is True
    assert len(albero) == 1
    assert albero.preordine() == [20]
    assert albero.altezza() == 0


def test_cancellazione_nodo_unico_e_ritorno_al_vuoto():
    albero = costruisci_da_inserimenti([40])
    assert albero.rimuovi(40) is True
    assert albero._radice is None
    assert len(albero) == 0
    assert albero.altezza() == -1
    albero.inserisci(55, "nuovo")
    assert albero.inordine() == [55]


def test_cancellazione_assente_conserva_tutto():
    albero = albero_d1()
    stato_prima = albero.voci_ordinate()
    assert albero.rimuovi(52) is False
    assert len(albero) == 10
    assert albero.voci_ordinate() == stato_prima
    assert albero.preordine() == [40, 20, 10, 30, 25, 35, 60, 50, 55, 70]


def test_rimozioni_ripetute_fino_al_vuoto():
    albero = albero_d1()
    for chiave in sorted(D1, reverse=True):
        assert albero.rimuovi(chiave) is True
    assert len(albero) == 0
    assert albero._radice is None
    assert albero.inordine() == []
    albero.inserisci(30, "rinascita")
    assert albero.voci_ordinate() == [(30, "rinascita")]


def test_coppie_chiave_dato_preservate_nella_cancellazione():
    dati = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "l"]
    albero = costruisci_da_inserimenti(D1, dati)
    albero.rimuovi(40)
    assert albero.voci_ordinate() == [
        (10, "d"),
        (20, "b"),
        (25, "h"),
        (30, "e"),
        (35, "i"),
        (50, "f"),
        (55, "l"),
        (60, "c"),
        (70, "g"),
    ]
