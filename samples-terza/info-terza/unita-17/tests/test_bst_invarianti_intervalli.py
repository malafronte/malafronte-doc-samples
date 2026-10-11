"""Prove su intervalli, invarianti e operazioni miste — Unità 17, cap. PY-33.

Casi semantici del piano §15.1: estremi presenti/assenti, uguaglianza,
inclusione, sotto/sopra, nessun risultato, vuoto, invertito, tipo
invalido; violazione globale, duplicato interno e dimensione errata;
sequenza deterministica confrontata con un oracolo `dict`.
"""

import pytest

from bst_u17 import AlberoBST, _Nodo, costruisci_da_inserimenti

D1 = [40, 20, 60, 10, 30, 50, 70, 25, 35, 55]


def albero_d1(dati=None):
    return costruisci_da_inserimenti(D1, dati)


def test_intervallo_inclusivo_su_d1():
    albero = albero_d1()
    assert albero.intervallo(25, 55) == [
        (25, 25),
        (30, 30),
        (35, 35),
        (40, 40),
        (50, 50),
        (55, 55),
    ]


def test_intervallo_estremi_e_confini():
    albero = albero_d1()
    # Estremi presenti: l'intervallo chiuso li include.
    assert [chiave for chiave, _ in albero.intervallo(10, 70)] == [
        10,
        20,
        25,
        30,
        35,
        40,
        50,
        55,
        60,
        70,
    ]
    # Uguaglianza degli estremi: soltanto la chiave corrispondente.
    assert albero.intervallo(35, 35) == [(35, 35)]
    # Estremo singolo assente ma intervallo con risultati.
    assert [chiave for chiave, _ in albero.intervallo(26, 34)] == [30]
    # Nessuna corrispondenza: intervallo compreso fra due chiavi vicine.
    assert albero.intervallo(36, 39) == []
    # Estremi sotto e sopra l'intero dominio.
    assert albero.intervallo(-100, 5) == []
    assert albero.intervallo(1000, 2000) == []


def test_intervallo_su_vuoto_e_estremi_invertiti():
    albero = AlberoBST()
    assert albero.intervallo(0, 100) == []
    with pytest.raises(ValueError):
        albero.intervallo(55, 25)
    con_dati = albero_d1()
    with pytest.raises(ValueError):
        con_dati.intervallo(55, 25)
    with pytest.raises(TypeError):
        con_dati.intervallo(25, "55")
    with pytest.raises(TypeError):
        con_dati.intervallo(True, 55)


def test_intervallo_restituisce_coppie_con_dati():
    dati = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "l"]
    albero = costruisci_da_inserimenti(D1, dati)
    assert albero.intervallo(25, 55) == [
        (25, "h"),
        (30, "e"),
        (35, "i"),
        (40, "a"),
        (50, "f"),
        (55, "l"),
    ]


def test_invarianti_su_struttura_valida():
    albero = albero_d1()
    albero.controlla_invarianti()
    albero.rimuovi(40)
    albero.controlla_invarianti()
    vuoto = AlberoBST()
    vuoto.controlla_invarianti()


def test_invarianti_rilevano_violazione_globale_d_ordine():
    # 45 nel sottoalbero sinistro di 40 viola il vincolo imposto dalla
    # radice: il controllo limitato al padre non lo rileverebbe.
    albero = AlberoBST()
    albero._radice = _Nodo(40, 40, sinistro=_Nodo(20, 20, destro=_Nodo(45, 45)))
    albero._dimensione = 3
    with pytest.raises(AssertionError):
        albero.controlla_invarianti()


def test_invarianti_rilevano_dimensione_errata_e_nodo_ripetuto():
    albero = AlberoBST()
    albero._radice = _Nodo(20, 20)
    albero._dimensione = 5
    with pytest.raises(AssertionError):
        albero.controlla_invarianti()

    condiviso = _Nodo(30, 30)
    albero = AlberoBST()
    albero._radice = _Nodo(20, 20, destro=condiviso, sinistro=condiviso)
    albero._dimensione = 3
    with pytest.raises(AssertionError):
        albero.controlla_invarianti()


def test_operazioni_miste_confrontate_con_oracolo_dict():
    # Sequenza deterministica nota da U8: dopo ogni modifica si
    # confrontano dimensione, coppie ordinate e risultati delle query.
    oracolo = {}
    albero = AlberoBST()
    operazioni = [
        ("inserisci", 40, "a"),
        ("inserisci", 20, "b"),
        ("inserisci", 60, "c"),
        ("inserisci", 10, "d"),
        ("inserisci", 30, "e"),
        ("aggiorna", 30, "e2"),
        ("inserisci", 50, "f"),
        ("inserisci", 70, "g"),
        ("inserisci", 25, "h"),
        ("rimuovi", 10, None),
        ("rimuovi", 40, None),
        ("inserisci", 35, "i"),
        ("rimuovi", 999, None),
        ("aggiorna", 70, "g2"),
    ]
    for operazione, chiave, dato in operazioni:
        if operazione == "inserisci":
            if chiave in oracolo:
                with pytest.raises(ValueError):
                    albero.inserisci(chiave, dato)
            else:
                albero.inserisci(chiave, dato)
                oracolo[chiave] = dato
        elif operazione == "aggiorna":
            if chiave not in oracolo:
                with pytest.raises(KeyError):
                    albero.aggiorna(chiave, dato)
            else:
                albero.aggiorna(chiave, dato)
                oracolo[chiave] = dato
        else:
            atteso = chiave in oracolo
            assert albero.rimuovi(chiave) is atteso
            oracolo.pop(chiave, None)

        assert len(albero) == len(oracolo)
        assert albero.voci_ordinate() == sorted(oracolo.items())
        assert albero.inordine() == sorted(oracolo)
        assert albero.intervallo(25, 60) == [
            voce for voce in sorted(oracolo.items()) if 25 <= voce[0] <= 60
        ]
        albero.controlla_invarianti()
