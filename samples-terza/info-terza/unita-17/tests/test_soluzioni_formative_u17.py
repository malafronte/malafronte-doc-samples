"""Prove sulle soluzioni formative — Unità 17.

Il modulo richiama le funzioni di verifica dei due moduli di soluzioni e
controlla che i risultati coincidano con i valori canonici dei capitoli.
"""

from bst_u17 import AlberoBST, costruisci_da_inserimenti
from esercizi_base_u17 import (
    conta_nodi_a_profondita,
    costruisci_d1_nodi,
    elementi_di_un_albero,
    inserisci_o_aggiorna,
    preordine_iterativo,
    profondita_e_altezza,
    ricerca_con_contratti,
    verifica_soluzioni_base,
    visita_con_accumulatore,
)
from problemi_algoritmici_u17 import (
    intervallo_con_esclusione,
    intervallo_con_visita_completa,
    profilo_di_un_ordine,
    prova_completa,
    rimuovi_con_due_figli,
    rimuovi_con_zero_o_un_figlio,
    verifica_ordine_e_dimensione,
)

D1 = [40, 20, 60, 10, 30, 50, 70, 25, 35, 55]


def test_verifica_soluzioni_base():
    assert verifica_soluzioni_base()["inordine"] == [10, 20, 25, 30, 35, 40, 50, 55, 60, 70]


def test_verifica_soluzioni_algoritmiche():
    assert prova_completa() is True


def test_funzioni_base_sui_casi_del_capitolo():
    d1 = costruisci_d1_nodi()
    assert elementi_di_un_albero(d1) == {"nodi": 10, "archi": 9, "foglie": 5}
    assert profondita_e_altezza(d1, 20) == (1, 2)
    assert profondita_e_altezza(d1, 40) == (0, 3)
    assert profondita_e_altezza(d1, 25) == (3, 0)
    assert conta_nodi_a_profondita(d1, 3) == 3
    assert conta_nodi_a_profondita(d1, 9) == 0
    assert visita_con_accumulatore(d1, "preordine") == [
        40,
        20,
        10,
        30,
        25,
        35,
        60,
        50,
        55,
        70,
    ]
    assert preordine_iterativo(d1) == visita_con_accumulatore(d1, "preordine")


def test_contratti_di_ricerca_e_aggiornamento():
    albero = costruisci_da_inserimenti(D1)
    assert ricerca_con_contratti(albero, 35) == (True, 35)
    assert ricerca_con_contratti(albero, 52) == (False, None)
    albero.inserisci(31, None)
    assert ricerca_con_contratti(albero, 31) == (True, None)
    assert inserisci_o_aggiorna(albero, 30, "aggiornato") == "aggiornato"
    assert inserisci_o_aggiorna(albero, 12, "nuovo") == "inserito"
    assert len(albero) == 12


def test_controllo_d_ordine_difettoso_e_corretto():
    albero = costruisci_da_inserimenti(D1)
    assert verifica_ordine_e_dimensione(albero) is True
    # Il discendente 45 nel sottoalbero sinistro di 40 sfugge al controllo
    # limitato al padre, mentre il validatore a limiti ereditati lo rileva.
    from bst_u17 import _Nodo

    difettoso = AlberoBST()
    difettoso._radice = _Nodo(40, 40, sinistro=_Nodo(20, 20, destro=_Nodo(45, 45)))
    difettoso._dimensione = 3
    try:
        verifica_ordine_e_dimensione(difettoso)
    except AssertionError:
        pass
    else:
        raise AssertionError("il controllo a limiti ereditati avrebbe dovuto rilevare 45")


def test_intervalli_equivalenti_e_profili():
    albero = costruisci_da_inserimenti(D1)
    contatore = {}
    assert intervallo_con_esclusione(albero, 25, 55, contatore) == intervallo_con_visita_completa(
        albero, 25, 55
    )
    assert [chiave for chiave, _ in intervallo_con_esclusione(albero, 25, 55)] == [
        25,
        30,
        35,
        40,
        50,
        55,
    ]
    assert contatore["nodi_esaminati"] < len(albero)
    assert profilo_di_un_ordine([4, 2, 6, 1, 3, 5, 7]) == {
        "n": 7,
        "altezza": 2,
        "nodi_costruzione": 10,
        "ricerca_massimo": 3,
        "ricerca_assente": 3,
    }
    assert profilo_di_un_ordine([1, 2, 3, 4, 5, 6, 7]) == {
        "n": 7,
        "altezza": 6,
        "nodi_costruzione": 21,
        "ricerca_massimo": 7,
        "ricerca_assente": 7,
    }


def test_cancellazioni_guidate():
    radice, rimosso = rimuovi_con_zero_o_un_figlio(None, 10)
    assert (radice, rimosso) == (None, False)
    albero = costruisci_da_inserimenti(D1)
    albero._radice, rimosso = rimuovi_con_zero_o_un_figlio(albero._radice, 10)
    assert rimosso is True
    albero._dimensione -= 1
    assert albero.inordine() == [20, 25, 30, 35, 40, 50, 55, 60, 70]

    due_figli = costruisci_da_inserimenti(D1)
    due_figli._radice, rimosso = rimuovi_con_due_figli(due_figli._radice, 40)
    assert rimosso is True
    assert due_figli._radice.chiave == 50
    assert due_figli.inordine() == [10, 20, 25, 30, 35, 50, 55, 60, 70]
