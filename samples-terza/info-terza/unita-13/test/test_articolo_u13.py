"""Prove della classe Articolo: casi ART-01…ART-05.

Le prove verificano lo schema, le diagnosi sul campo, la conservazione dello
stato dopo un rifiuto e la differenza fra proiezione dei dati e attributi
interni.
"""

import pytest
from articolo_u13 import Articolo, valida_dati_articolo

CANONICI = (
    ("007", "Vite, lunga", 4, 25),
    ("012", 'Caffè "A"', 2, 350),
)


# --- ART-01 ---------------------------------------------------------------


def test_art_01_articoli_canonici():
    """ART-01: campi preservati, valori 100 e 700 centesimi."""
    primo = Articolo(*CANONICI[0])
    secondo = Articolo(*CANONICI[1])
    assert primo.dati() == {
        "codice": "007",
        "descrizione": "Vite, lunga",
        "quantita": 4,
        "prezzo_centesimi": 25,
    }
    assert secondo.dati() == {
        "codice": "012",
        "descrizione": 'Caffè "A"',
        "quantita": 2,
        "prezzo_centesimi": 350,
    }
    assert primo.valore_centesimi() == 100
    assert secondo.valore_centesimi() == 700


def test_art_01_codice_esatto():
    """ART-01: `007` e `7` sono codici diversi, con confronto sensibile alle maiuscole."""
    articolo = Articolo("007", "Vite, lunga", 4, 25)
    assert articolo.ha_codice("007") is True
    assert articolo.ha_codice("7") is False
    assert articolo.ha_codice("007 ") is False
    assert Articolo("ab", "x", 0, 0).ha_codice("AB") is False


# --- ART-02 ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("codice", "descrizione", "quantita", "prezzo", "campo"),
    [
        ("", "Vite", 4, 25, "codice"),
        (" 007", "Vite", 4, 25, "codice"),
        ("007 ", "Vite", 4, 25, "codice"),
        ("007", "   ", 4, 25, "descrizione"),
        ("007", "", 4, 25, "descrizione"),
        ("007", "Vite", -1, 25, "quantita"),
        ("007", "Vite", 4, -1, "prezzo_centesimi"),
        ("007", "Vite", 1.5, 25, "quantita"),
        ("007", "Vite", 4, "25", "prezzo_centesimi"),
    ],
)
def test_art_02_diagnosi_sul_campo(codice, descrizione, quantita, prezzo, campo):
    """ART-02: la costruzione rifiutata nomina il campo responsabile."""
    with pytest.raises(ValueError, match=campo):
        Articolo(codice, descrizione, quantita, prezzo)


@pytest.mark.parametrize("quantita", [True, False])
def test_art_02_booleano_non_ammesso(quantita):
    """ART-02: un booleano non è un intero ammesso dallo schema."""
    with pytest.raises(ValueError, match="atteso un intero"):
        Articolo("007", "Vite", quantita, 25)


def test_art_02_validazione_condivisa():
    """ART-02: la funzione pura rifiuta senza costruire istanze."""
    assert valida_dati_articolo("007", "Vite", 4, 25) is None
    with pytest.raises(ValueError):
        valida_dati_articolo("007", 12, 4, 25)


# --- ART-03 ---------------------------------------------------------------


def test_art_03_aggiornamento_paziale_rifiutato():
    """ART-03: primo campo valido e secondo invalido, tutto invariato."""
    articolo = Articolo(*CANONICI[0])
    with pytest.raises(ValueError):
        articolo.aggiorna("Nuova descrizione", -1, 30)
    assert articolo.dati() == {
        "codice": "007",
        "descrizione": "Vite, lunga",
        "quantita": 4,
        "prezzo_centesimi": 25,
    }


def test_art_03_identita_preservata():
    """ART-03: dopo il rifiuto l'istanza è la stessa, con lo stesso codice."""
    articolo = Articolo(*CANONICI[0])
    identita = id(articolo)
    with pytest.raises(ValueError):
        articolo.aggiorna("Nuova descrizione", 2, -30)
    assert id(articolo) == identita
    assert articolo.ha_codice("007") is True


# --- ART-04 ---------------------------------------------------------------


def test_art_04_aggiornamento_valido_con_alias():
    """ART-04: l'alias osserva i nuovi dati e il codice resta stabile."""
    articolo = Articolo(*CANONICI[0])
    alias = articolo
    assert articolo.aggiorna("Vite, corta", 6, 30) is None
    assert alias.dati() == {
        "codice": "007",
        "descrizione": "Vite, corta",
        "quantita": 6,
        "prezzo_centesimi": 30,
    }
    assert alias is articolo
    assert alias.ha_codice("007") is True


def test_art_04_differenza_da_sostituzione():
    """ART-04: l'istanza esistente non viene rimpiazzata, come accadeva in U12."""
    articolo = Articolo(*CANONICI[0])
    riferimenti = [articolo]
    articolo.aggiorna("Vite, corta", 6, 30)
    assert riferimenti[0].dati()["descrizione"] == "Vite, corta"


# --- ART-05 ---------------------------------------------------------------


def test_art_05_proiezione_indipendente():
    """ART-05: modificare il record di `dati()` non modifica l'articolo."""
    articolo = Articolo(*CANONICI[0])
    record = articolo.dati()
    record["descrizione"] = "cambiato"
    record["quantita"] = 999
    assert articolo.dati() == {
        "codice": "007",
        "descrizione": "Vite, lunga",
        "quantita": 4,
        "prezzo_centesimi": 25,
    }


def test_art_05_due_proiezioni_distinte():
    """ART-05: ogni chiamata a `dati()` produce un dizionario nuovo."""
    articolo = Articolo(*CANONICI[0])
    prima = articolo.dati()
    seconda = articolo.dati()
    assert prima is not seconda
    assert prima == seconda
