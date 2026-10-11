"""Prove sugli alberi binari rappresentati con oggetti — Unità 17, cap. PY-32.

Casi semantici del piano §15.1: vuoto, nodo unico, un figlio, D1 e un
albero binario generico con valori fuori ordine; tre visite, conteggi e
altezza.
"""

from alberi_binari_u17 import (
    Nodo,
    altezza,
    conta_foglie,
    conta_nodi,
    costruisci_albero_d1,
    inordine,
    postordine,
    preordine,
    profondita_valore,
)

VUOTO = None
NODO_UNICO = Nodo(40)
UN_FIGLIO = Nodo(40, Nodo(20))
D1 = [40, 20, 60, 10, 30, 50, 70, 25, 35, 55]


def albero_generico():
    """Albero binario non ordinato, per distinguere struttura e ordine."""
    return Nodo("m", Nodo("z", Nodo("a")), Nodo("q", None, Nodo("b")))


def test_vuoto_e_nodo_unico():
    assert conta_nodi(VUOTO) == 0
    assert conta_foglie(VUOTO) == 0
    assert altezza(VUOTO) == -1
    assert preordine(VUOTO) == []
    assert inordine(VUOTO) == []
    assert postordine(VUOTO) == []

    assert conta_nodi(NODO_UNICO) == 1
    assert conta_foglie(NODO_UNICO) == 1
    assert altezza(NODO_UNICO) == 0
    assert preordine(NODO_UNICO) == [40]
    assert inordine(NODO_UNICO) == [40]
    assert postordine(NODO_UNICO) == [40]


def test_nodo_con_un_solo_figlio_non_e_foglia():
    assert conta_nodi(UN_FIGLIO) == 2
    assert conta_foglie(UN_FIGLIO) == 1
    assert altezza(UN_FIGLIO) == 1
    assert preordine(UN_FIGLIO) == [40, 20]


def test_altezza_della_catena_di_tre_nodi():
    catena = Nodo(1, Nodo(2, Nodo(3)))
    assert altezza(catena) == 2
    assert conta_foglie(catena) == 1
    assert inordine(catena) == [3, 2, 1]


def test_d1_visite_conteggi_e_altezza():
    albero = costruisci_albero_d1()
    assert conta_nodi(albero) == 10
    assert conta_foglie(albero) == 5
    assert altezza(albero) == 3
    assert preordine(albero) == [40, 20, 10, 30, 25, 35, 60, 50, 55, 70]
    assert inordine(albero) == [10, 20, 25, 30, 35, 40, 50, 55, 60, 70]
    assert postordine(albero) == [10, 25, 35, 30, 20, 55, 50, 70, 60, 40]


def test_d1_profondita_dei_nodi_foglia():
    albero = costruisci_albero_d1()
    assert profondita_valore(albero, 40) == 0
    assert profondita_valore(albero, 20) == 1
    assert profondita_valore(albero, 35) == 3
    assert profondita_valore(albero, 55) == 3
    assert profondita_valore(albero, 999) is None


def test_albero_generico_visite_indipendenti_dall_ordine():
    albero = albero_generico()
    assert preordine(albero) == ["m", "z", "a", "q", "b"]
    assert inordine(albero) == ["a", "z", "m", "q", "b"]
    assert postordine(albero) == ["a", "z", "b", "q", "m"]
    assert altezza(albero) == 2
    # Le foglie sono "a" e "b": "z" e "q" hanno un solo figlio e non sono foglie.
    assert conta_foglie(albero) == 2


def test_visite_restituiscono_liste_indipendenti():
    albero = costruisci_albero_d1()
    prima = inordine(albero)
    prima.append(999)
    assert inordine(albero) == [10, 20, 25, 30, 35, 40, 50, 55, 60, 70]
