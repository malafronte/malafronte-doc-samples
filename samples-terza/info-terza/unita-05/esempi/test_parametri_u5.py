"""Test degli effetti e dell'indipendenza (cap. PY-09, sez. J).

Collocare il file in `programmi/test_parametri_u5.py`, vicino a
`parametri_u5.py`. Eseguire con: uv run pytest -q programmi/test_parametri_u5.py
Ogni test prepara i propri dati: nessuna lista condivisa fra test.
"""

from parametri_u5 import (
    aggiungi_in_posto,
    con_aggiunta,
    raccogli,
    riepilogo,
    sostituisci_locale,
)


def test_riassegnamento_locale_non_cambia_il_chiamante() -> None:
    dati = [4, 7]
    esito = sostituisci_locale(dati)
    assert dati == [4, 7]
    assert esito is None


def test_aggiungi_in_posto_modifica_la_lista_ricevuta() -> None:
    dati = [4, 7]
    esito = aggiungi_in_posto(dati, 3)
    assert dati == [4, 7, 3]
    assert esito is None


def test_aggiungi_in_posto_accetta_la_lista_vuota() -> None:
    dati = []
    esito = aggiungi_in_posto(dati, 3)
    assert dati == [3]
    assert esito is None


def test_con_aggiunta_restituisce_una_lista_nuova() -> None:
    dati = [4, 7]
    risultato = con_aggiunta(dati, 3)
    assert risultato == [4, 7, 3]
    assert dati == [4, 7]
    assert risultato is not dati


def test_con_aggiunta_sulla_lista_vuota() -> None:
    dati = []
    risultato = con_aggiunta(dati, 3)
    assert risultato == [3]
    assert dati == []
    assert risultato is not dati


def test_riepilogo_non_vuoto() -> None:
    dati = [4, 7, 3]
    risultato = riepilogo(dati)
    assert risultato == (3, 14)
    assert dati == [4, 7, 3]


def test_riepilogo_con_interi_negativi() -> None:
    dati = [-2, 0, 5]
    risultato = riepilogo(dati)
    assert risultato == (3, 3)
    assert dati == [-2, 0, 5]


def test_riepilogo_lista_vuota() -> None:
    assert riepilogo([]) == (0, 0)


def test_due_chiamate_senza_argomento_sono_indipendenti() -> None:
    primo = raccogli(3)
    secondo = raccogli(7)
    assert primo == [3]
    assert secondo == [7]
    assert secondo is not primo


def test_argomento_esplicito_none_crea_una_lista_nuova() -> None:
    risultato = raccogli(3, None)
    assert risultato == [3]


def test_lista_vuota_fornita_viene_modificata() -> None:
    dati = []
    risultato = raccogli(3, dati)
    assert dati == [3]
    assert risultato is dati


def test_lista_fornita_non_vuota_viene_modificata() -> None:
    dati = [4]
    risultato = raccogli(7, dati)
    assert dati == [4, 7]
    assert risultato is dati


def test_falsa_copia_viene_smascherata_dallo_stato_dell_input() -> None:
    """Test discriminante: un'implementazione che restituisce il contenuto
    atteso ma muta indebitamente l'input fallisce sull'asserzione finale."""
    dati = [4, 7]
    risultato = con_aggiunta(dati, 3)
    assert risultato == [4, 7, 3]
    assert dati == [4, 7]
