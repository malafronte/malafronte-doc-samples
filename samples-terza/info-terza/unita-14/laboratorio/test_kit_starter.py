"""Test pubblici iniziali dello starter del LAB-PY-U14.

Pochi test di feedback, **non** una suite completa: lo studente ne aggiunge
almeno due motivati e uno che fallisce sulla versione difettosa. Questi
test non fanno parte della suite del progetto (`tests/`): si eseguono dalla
cartella `laboratorio/` con `uv run pytest test_kit_starter.py -q` e
falliscono finché le fasi non sono completate: è il comportamento atteso.
"""

import pytest
from kit_starter import GestorePrestiti, catalogo_pubblico, crea_kit


def test_kit_con_campi_validi():
    kit = crea_kit("K01", "Kit misure", 3)
    assert kit.codice == "K01"


def test_kit_rifiuta_dotazione_negativa():
    with pytest.raises(ValueError):
        crea_kit("K01", "Kit misure", -1)


def test_due_gestori_sul_catalogo_pubblico():
    primo = GestorePrestiti(catalogo_pubblico())
    secondo = GestorePrestiti(catalogo_pubblico())
    assert primo.disponibile("K01") == 3
    assert secondo.disponibile("K01") == 3
