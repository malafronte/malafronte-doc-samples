"""Prove sulle soluzioni formative — Unità 18.

La suite verifica i moduli in `soluzioni/`: stati delle tracce, diagnosi dei
difetti, suite discriminante di esempio, fotografia di riferimento e gli otto
problemi canonici della famiglia Hashing, collisioni e indici.
"""

import pytest

from esercizi_base_u18 import (
    chiavi_stesso_indice_riferimento,
    diagnosi_crescita_con_indici_vecchi,
    diagnosi_dimensione_su_aggiornamento,
    diagnosi_marcatore_mancante,
    diagnosi_scansione_interrotta,
    diagnosi_sovrascrittura,
    fotografia_riferimento,
    suite_discriminante,
    verifica_crescita,
    verifica_sequenza_base,
)
from indice_record_u18 import RecordMateriale
from problemi_hash_u18 import (
    aggrega_quantita,
    chiavi_stesso_indice,
    deduplica_codici,
    distribuzione_associazioni,
    indice_con_univita,
    interpreta_conteggi,
    scegli_indice,
    sequenza_verifica_modifiche,
)


def test_verifica_sequenza_base():
    esito = verifica_sequenza_base()
    assert esito["indici"] == {12: 2, 7: 2, 22: 2, 17: 2}
    assert [c for c, _v in esito["catena_bucket_2"]] == [17, 22, 7, 12]
    assert esito["dimensione"] == 4
    assert esito["carico"] == pytest.approx(0.8)
    assert esito["ricerche"][7] == ("B2", 3)
    assert esito["ricerche"][27] == ("KeyError", 4)
    assert esito["ricerche"][4] == ("KeyError", 0)


def test_verifica_crescita():
    esito = verifica_crescita()
    assert (esito["dimensione"], esito["capacita"]) == (6, 10)
    assert esito["carico"] == pytest.approx(0.6)
    assert esito["indici"] == {12: 2, 7: 7, 22: 2, 17: 7, 3: 3, 8: 8}


def test_diagnosi_verificate():
    for diagnosi in (
        diagnosi_sovrascrittura(),
        diagnosi_dimensione_su_aggiornamento(),
        diagnosi_scansione_interrotta(),
        diagnosi_crescita_con_indici_vecchi(),
        diagnosi_marcatore_mancante(),
    ):
        assert diagnosi["verificato"] is True


def test_suite_discriminante():
    suite = suite_discriminante()
    assert len(suite) == 3
    coperti = {d for caso in suite for d in caso["difetti_rivelati"]}
    assert len(coperti) >= 3


def test_fotografia_e_famiglia_riferimento():
    assert [c for c, _v in fotografia_riferimento()] == ["003", "007", "012", "017"]
    assert chiavi_stesso_indice_riferimento() == [2, 7, 12, 17]


def test_t09_chiavi_stesso_indice():
    assert chiavi_stesso_indice(5, 2, 4) == [2, 7, 12, 17]
    assert chiavi_stesso_indice(5, 0, 0) == []


def test_t10_distribuzione():
    riepilogo = distribuzione_associazioni([0, 0, 4, 0, 0])
    assert (riepilogo["n"], riepilogo["lunghezza_massima"]) == (4, 4)
    assert riepilogo["indici_massimo"] == [2]


def test_t11_deduplica():
    assert deduplica_codici(["007", "012", "007", "003", "012"]) == ["007", "012", "003"]
    assert deduplica_codici([]) == []
    assert deduplica_codici(["007", "7"]) == ["007", "7"]


def test_t12_aggrega():
    totali, ordine = aggrega_quantita([("007", 4), ("012", 2), ("007", -4)])
    assert totali == {"007": 0, "012": 2}
    assert ordine == ["007", "012"]
    assert "007" in totali


def test_t13_indice_e_query():
    record = [
        RecordMateriale("007", "cavetto USB", 4),
        RecordMateriale("012", "tastiera", 2),
    ]
    foto, risposte = indice_con_univita(record, ["007", "999"], 5)
    assert [c for c, _v in foto] == ["007", "012"]
    assert risposte[0][1].descrizione == "cavetto USB"
    assert risposte[1] == ("999", "assente")
    with pytest.raises(ValueError):
        indice_con_univita(record + [RecordMateriale("007", "doppio", 1)], ["007"], 5)


def test_t14_sequenza_coerente():
    passi = sequenza_verifica_modifiche()
    assert len(passi) == 9
    assert all(p["coerente_con_dict"] for p in passi)
    assert passi[-1]["capacita"] == 10


def test_x05_scelte_motivate():
    assert scegli_indice(1000, 1, 0, 0)[0] == "scansione"
    assert scegli_indice(1000, 500, 0, 10)[0] == "hash"
    assert scegli_indice(1000, 50, 5, 10)[0] == "BST"


def test_x06_conteggi():
    distribuite = [(i, f"V{i}") for i in (1, 2, 3, 4)]
    concentrate = [(2 + 5 * j, f"V{j}") for j in range(4)]
    esito = interpreta_conteggi(distribuite, concentrate, [2, 99], 5)
    assert esito["capacita"] == 5
    for famiglia in ("distribuite", "concentrate"):
        assert [r["trovato"] for r in esito[famiglia]] == [True, False]
    peggiore_conc = max(r["confronti"] for r in esito["concentrate"])
    peggiore_dist = max(r["confronti"] for r in esito["distribuite"])
    assert (peggiore_dist, peggiore_conc) == (1, 4)
