"""Prove sull'indice di record e sulle chiavi native — Unità 18.

Casi del piano §§L e C/J: costruzione con unicità, zeri significativi,
duplicati rifiutati senza consegna parziale, query assenti, fotografia
ordinata, sostituzione di un record, equivalenza numerica di `dict` ed
esempi hashable.
"""

import pytest

from chiavi_native_u18 import (
    associazione_con_chiave_valore,
    diagnosi_chiave_mutata,
    equivalenza_numerica,
    tupla_con_elemento_mutabile,
)
from indice_record_u18 import (
    RecordMateriale,
    consulta,
    costruisci_indice,
    fotografia,
    record_canonici,
    sostituisci_record,
    valida_codice,
)


def test_record_canonici_e_collisioni():
    record = record_canonici()
    assert [voce.codice for voce in record] == ["007", "012", "003", "017"]
    indice = costruisci_indice(record, 5)
    assert len(indice) == 4
    for voce in record:
        assert consulta(indice, voce.codice) == voce
    assert indice.lunghezze_bucket() == [0, 1, 3, 0, 0]


def test_zeri_significativi_e_chiavi_distinte():
    indice = costruisci_indice(
        [RecordMateriale("007", "cavetto", 1), RecordMateriale("7", "etichetta", 2)], 5
    )
    assert consulta(indice, "007").descrizione == "cavetto"
    assert consulta(indice, "7").descrizione == "etichetta"


def test_duplicato_rifiutato_senza_consegna():
    record = record_canonici() + [RecordMateriale("007", "doppio", 9)]
    with pytest.raises(ValueError):
        costruisci_indice(record, 5)


def test_costruzione_vuota():
    indice = costruisci_indice([], 5)
    assert len(indice) == 0
    with pytest.raises(KeyError):
        consulta(indice, "007")


def test_query_assente_distinta_dal_valore():
    indice = costruisci_indice(record_canonici(), 5)
    with pytest.raises(KeyError):
        consulta(indice, "999")
    with pytest.raises(ValueError):
        consulta(indice, "")
    with pytest.raises(TypeError):
        consulta(indice, 7)


def test_fotografia_ordinata_e_sorgente_conservata():
    record = record_canonici()
    indice = costruisci_indice(record, 5)
    foto = fotografia(indice)
    assert [codice for codice, _voce in foto] == ["003", "007", "012", "017"]
    assert [voce.codice for voce in record] == ["007", "012", "003", "017"]


def test_sostituisci_record():
    indice = costruisci_indice(record_canonici(), 5)
    foto = sostituisci_record(indice, "007", RecordMateriale("007", "cavetto nuovo", 5))
    assert consulta(indice, "007").quantita == 5
    assert [codice for codice, _voce in foto] == ["003", "007", "012", "017"]
    with pytest.raises(ValueError):
        sostituisci_record(indice, "007", RecordMateriale("012", "altro", 1))


def test_validazione_record():
    with pytest.raises(ValueError):
        RecordMateriale("", "vuoto", 1)
    with pytest.raises(TypeError):
        RecordMateriale(7, "intero", 1)
    with pytest.raises(ValueError):
        RecordMateriale("007", "negativo", -1)
    with pytest.raises(TypeError):
        RecordMateriale("007", "bool", True)
    with pytest.raises(TypeError):
        valida_codice(7)


def test_confronto_con_dict():
    record = record_canonici()
    indice = costruisci_indice(record, 5)
    riferimento = {voce.codice: voce for voce in record}
    assert len(indice) == len(riferimento)
    for codice, voce in riferimento.items():
        assert consulta(indice, codice) == voce


def test_chiave_valore_frozen():
    esito = associazione_con_chiave_valore()
    assert esito["istanze_uguali"] is True
    assert esito["hash_coerenti"] is True
    assert esito["valore_ritrovato"] == "laboratorio"


def test_equivalenza_numerica_dict():
    esito = equivalenza_numerica()
    assert esito["associazioni"] == 1
    assert esito["valore"] == "reale"


def test_tupla_con_lista_non_hashable():
    esito = tupla_con_elemento_mutabile()
    assert esito["tupla_con_lista_non_hashable"] is True
    assert esito["tupla_hashable"] is True


def test_diagnosi_chiave_mutata():
    esito = diagnosi_chiave_mutata()
    assert esito["trovato_prima"] == "primo"
    assert esito["equivalente_prima"] == "primo"
    assert esito["equivalente_dopo"] is None
    assert esito["trovato_dopo"] in (None, "primo")
