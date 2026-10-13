"""Prove delle soluzioni di riferimento — Unità 19."""

from esercizi_base_u19 import (
    verifica_confronto_carico,
    verifica_indice_record,
    verifica_ricerche_d1,
    verifica_sequenza_d2,
)
from problemi_btree_u19 import (
    btree_riferimento,
    capienza_nodo_blocco,
    conta_accessi_blocchi,
    dossier_consultazioni,
    query_intervallo_record,
    sequenza_aumento_altezza,
    traccia_speculare_d5,
    verifica_indici_equivalenti,
    verifica_limiti_ereditati,
)


def test_soluzioni_base():
    """Le verifiche di base confermano D1, D2, record e confronto."""
    assert verifica_ricerche_d1() == {
        20: (True, 1),
        17: (True, 2),
        15: (False, 2),
        4: (False, 2),
        40: (False, 2),
    }
    d2 = verifica_sequenza_d2()
    assert (d2["radice"], d2["altezza"], d2["dimensione"]) == ([4], 2, 10)
    assert d2["conteggi"] == {4: (1, 2), 10: (3, 6), 0: (3, 6), 11: (3, 5)}
    record = verifica_indice_record()
    assert record["chiavi"] == ["003", "007", "012", "017", "021", "034", "042", "7"]
    assert record["intervallo"] == ["007", "012", "017", "021"]
    assert verifica_confronto_carico()["coerente"] is True


def test_soluzioni_problemi():
    """Le soluzioni algoritmiche confermano altezza, intervalli e scelta."""
    assert sequenza_aumento_altezza()["altezza_finale"] == 1
    assert [c for c, _d in query_intervallo_record("007", "021")] == ["007", "012", "017", "021"]
    assert dossier_consultazioni()["coerente"] is True
    assert verifica_indici_equivalenti() is True
    assert traccia_speculare_d5()["coerente"] is True
    assert verifica_limiti_ereditati(btree_riferimento([(1, "a"), (2, "b")])) is True


def test_blocchi_e_capienza():
    """Blocchi distinti dalle visite e capienza `t = 85` nel modello."""
    accessi = conta_accessi_blocchi([10, 4], radice_residente=False)
    assert accessi == {10: (3, 3), 4: (1, 1)}
    residenti = conta_accessi_blocchi([10], radice_residente=True)
    assert residenti == {10: (3, 2)}
    capienza = capienza_nodo_blocco()
    assert capienza["t_massimo"] == 85
    assert capienza["occupazione"] <= 4096
