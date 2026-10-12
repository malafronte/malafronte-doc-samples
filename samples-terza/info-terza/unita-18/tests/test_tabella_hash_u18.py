"""Prove sulla tabella concatenata — Unità 18, cap. PY-34.

Casi semantici del piano §18.1: tabella vuota, catena concentrata e bucket
distinti, valori falsy presenti, inserimenti e aggiornamenti ripetuti,
rimozioni di testa, interno, coda, unico nodo e assente, reinserimento dopo
rimozione, crescite successive con conservazione, validazione di chiavi e
capacità, invarianti dopo sequenze di modifiche ed equivalenza con `dict`.
"""

import pytest

from tabella_hash_u18 import TabellaHashConcatenata


def tabella_base():
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(12, "A")
    tabella.assegna(7, "B")
    tabella.assegna(22, "C")
    tabella.assegna(17, "D")
    return tabella


def test_tabella_vuota():
    tabella = TabellaHashConcatenata(5)
    assert len(tabella) == 0
    assert tabella.capacita == 5
    assert tabella.fattore_carico == 0
    assert tabella.contiene(12) is False
    with pytest.raises(KeyError):
        tabella.cerca(12)
    with pytest.raises(KeyError):
        tabella.rimuovi(12)
    assert tabella.coppie() == []
    tabella.controlla_invarianti()


def test_capacita_non_valida():
    with pytest.raises(ValueError):
        TabellaHashConcatenata(0)
    with pytest.raises(TypeError):
        TabellaHashConcatenata("5")
    with pytest.raises(TypeError):
        TabellaHashConcatenata(True)
    with pytest.raises(TypeError):
        TabellaHashConcatenata(5.0)


def test_chiavi_fuori_dominio():
    tabella = TabellaHashConcatenata(5)
    for chiave in (True, 1.5, None, (1, 2), ["a"], b"a"):
        with pytest.raises(TypeError):
            tabella.assegna(chiave, "x")
        with pytest.raises(TypeError):
            tabella.cerca(chiave)
        with pytest.raises(TypeError):
            tabella.contiene(chiave)
        with pytest.raises(TypeError):
            tabella.rimuovi(chiave)


def test_sequenza_base_e_catena():
    tabella = tabella_base()
    assert len(tabella) == 4
    assert tabella.fattore_carico == pytest.approx(0.8)
    assert tabella.lunghezze_bucket() == [0, 0, 4, 0, 0]
    assert [chiave for chiave, _v in tabella.coppie()] == [17, 22, 7, 12]
    tabella.controlla_invarianti()


def test_ricerche_con_conteggi():
    tabella = tabella_base()
    tabella.assegna(7, "B2")
    assert tabella.cerca(17) == "D" and tabella.confronti_per(17) == 1
    assert tabella.cerca(7) == "B2" and tabella.confronti_per(7) == 3
    assert tabella.cerca(12) == "A" and tabella.confronti_per(12) == 4
    with pytest.raises(KeyError):
        tabella.cerca(27)
    assert tabella.confronti_per(27) == 4
    with pytest.raises(KeyError):
        tabella.cerca(4)
    assert tabella.confronti_per(4) == 0


def test_valori_falsy_distinti_dall_assenza():
    tabella = TabellaHashConcatenata(5)
    for chiave, valore in [(1, 0), (2, False), (3, None), ("x", "")]:
        tabella.assegna(chiave, valore)
    assert tabella.cerca(1) == 0
    assert tabella.cerca(2) is False
    assert tabella.cerca(3) is None
    assert tabella.cerca("x") == ""
    assert tabella.contiene(1) is True
    assert len(tabella) == 4
    tabella.controlla_invarianti()


def test_intero_e_stringa_come_chiavi_distinte():
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(7, "intero")
    tabella.assegna("7", "stringa")
    tabella.assegna("007", "codice")
    assert tabella.cerca(7) == "intero"
    assert tabella.cerca("7") == "stringa"
    assert tabella.cerca("007") == "codice"
    assert len(tabella) == 3


def test_aggiornamento_conserva_posizione_e_dimensione():
    tabella = tabella_base()
    tabella.assegna(7, "B2")
    assert len(tabella) == 4
    assert tabella.capacita == 5
    assert tabella.cerca(7) == "B2"
    assert tabella.cerca(12) == "A"
    tabella.controlla_invarianti()


def test_rimozione_testa():
    tabella = tabella_base()
    assert tabella.rimuovi(17) == "D"
    assert len(tabella) == 3
    assert [c for c, _v in tabella.coppie()] == [22, 7, 12]
    with pytest.raises(KeyError):
        tabella.cerca(17)
    tabella.controlla_invarianti()


def test_rimozione_nodo_interno():
    tabella = tabella_base()
    assert tabella.rimuovi(22) == "C"
    assert [c for c, _v in tabella.coppie()] == [17, 7, 12]
    assert tabella.cerca(7) == "B"
    tabella.controlla_invarianti()


def test_rimozione_coda():
    tabella = tabella_base()
    assert tabella.rimuovi(12) == "A"
    assert [c for c, _v in tabella.coppie()] == [17, 22, 7]
    tabella.controlla_invarianti()


def test_rimozione_assente_conserva_stato():
    tabella = tabella_base()
    with pytest.raises(KeyError):
        tabella.rimuovi(27)
    assert len(tabella) == 4
    assert tabella.capacita == 5
    assert [c for c, _v in tabella.coppie()] == [17, 22, 7, 12]
    tabella.controlla_invarianti()


def test_rimozione_unico_nodo():
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(3, "solo")
    assert tabella.rimuovi(3) == "solo"
    assert len(tabella) == 0
    assert tabella.lunghezze_bucket() == [0, 0, 0, 0, 0]
    tabella.controlla_invarianti()


def test_reinserimento_dopo_rimozione():
    tabella = tabella_base()
    tabella.rimuovi(22)
    tabella.assegna(22, "C2")
    assert tabella.cerca(22) == "C2"
    assert len(tabella) == 4
    tabella.controlla_invarianti()


def test_crescita_da_cinque_a_dieci():
    tabella = TabellaHashConcatenata(5)
    for chiave in (12, 7, 22, 17, 3):
        tabella.assegna(chiave, f"V{chiave}")
    assert (len(tabella), tabella.capacita) == (5, 5)
    assert tabella.fattore_carico == pytest.approx(1.0)
    tabella.assegna(8, "V8")
    assert (len(tabella), tabella.capacita) == (6, 10)
    assert tabella.fattore_carico == pytest.approx(0.6)
    for chiave in (12, 7, 22, 17, 3, 8):
        assert tabella.cerca(chiave) == f"V{chiave}"
    attesi = {12: 2, 7: 7, 22: 2, 17: 7, 3: 3, 8: 8}
    for chiave, indice in attesi.items():
        assert tabella._indice(chiave) == indice
    tabella.controlla_invarianti()


def test_crescite_successive_conservano_associazioni():
    tabella = TabellaHashConcatenata(2)
    riferimento = {}
    for chiave in range(30):
        tabella.assegna(chiave, chiave * 10)
        riferimento[chiave] = chiave * 10
    assert len(tabella) == 30
    assert tabella.capacita == 32
    for chiave, valore in riferimento.items():
        assert tabella.cerca(chiave) == valore
    tabella.controlla_invarianti()


def test_coppie_fotografia_superficiale():
    tabella = tabella_base()
    fotografia = tabella.coppie()
    fotografia.append((99, "X"))
    assert len(tabella) == 4
    with pytest.raises(KeyError):
        tabella.cerca(99)


def test_equivalenza_con_dict():
    tabella = TabellaHashConcatenata(5)
    riferimento = {}
    operazioni = [(12, "A"), (7, "B"), (22, "C"), (17, "D"), (7, "B2"), ("007", "Z")]
    for chiave, valore in operazioni:
        tabella.assegna(chiave, valore)
        riferimento[chiave] = valore
    assert len(tabella) == len(riferimento)
    for chiave, valore in riferimento.items():
        assert tabella.cerca(chiave) == valore
    tabella.rimuovi(22)
    del riferimento[22]
    assert sorted(map(repr, tabella.coppie())) == sorted(map(repr, riferimento.items()))
    tabella.controlla_invarianti()


def test_sequenza_mista_con_invarianti():
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(12, "A")
    tabella.assegna(7, "B")
    tabella.rimuovi(12)
    tabella.assegna(22, "C")
    tabella.assegna(7, "B2")
    tabella.assegna(17, "D")
    tabella.assegna(3, "E")
    assert len(tabella) == 4
    assert tabella.cerca(7) == "B2"
    tabella.controlla_invarianti()
