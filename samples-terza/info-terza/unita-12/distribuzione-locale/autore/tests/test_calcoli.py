"""Test del package `utilita_magazzino_u12`.

Almeno tre casi discriminanti per funzione: il limite dello zero, un caso
ordinario con i valori canonici del corso e una violazione del dominio con la
diagnosi attesa. I test distinguono anche le due classi di errore del contratto
- `TypeError` per l'argomento di tipo sbagliato, `ValueError` per il dato fuori
dominio - e verificano che l'argomento non venga modificato dove il contratto
lo promette.

Esecuzione dalla cartella `autore/`:

    uv run pytest tests/ -q
"""

import pytest

from utilita_magazzino_u12 import formatta_centesimi, normalizza_codice, valore_magazzino

RECORD_CANONICI = [
    {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
    {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
]


def test_valore_magazzino_sul_dataset_canonico():
    assert valore_magazzino(RECORD_CANONICI) == 800


def test_valore_magazzino_sulla_lista_vuota_e_zero():
    assert valore_magazzino([]) == 0


def test_valore_magazzino_non_modifica_la_lista():
    articoli = [dict(record) for record in RECORD_CANONICI]
    prima = [dict(record) for record in articoli]
    valore_magazzino(articoli)
    assert articoli == prima


def test_valore_magazzino_rifiuta_i_dati_fuori_dominio():
    with pytest.raises(ValueError, match="quantita"):
        valore_magazzino([dict(RECORD_CANONICI[0], quantita=-1)])
    with pytest.raises(ValueError, match="atteso un intero"):
        valore_magazzino([dict(RECORD_CANONICI[0], quantita=True)])
    with pytest.raises(ValueError, match="mancante"):
        valore_magazzino([{"quantita": 1}])


def test_valore_magazzino_con_argomento_non_lista_e_un_uso_sbagliato():
    with pytest.raises(TypeError, match="attesa una lista"):
        valore_magazzino(5)


def test_formatta_centesimi_zero_e_resti_piccoli():
    assert formatta_centesimi(0) == "0,00 €"
    assert formatta_centesimi(5) == "0,05 €"
    assert formatta_centesimi(800) == "8,00 €"
    assert formatta_centesimi(1234) == "12,34 €"


def test_formatta_centesimi_distingue_tipo_e_dominio():
    with pytest.raises(ValueError, match="non negativo"):
        formatta_centesimi(-1)
    for valore in (True, 1.0, "8"):
        with pytest.raises(TypeError, match="atteso un intero"):
            formatta_centesimi(valore)


def test_normalizza_codice_elimina_solo_gli_spazi_esterni():
    assert normalizza_codice(" 007 ") == "007"
    assert normalizza_codice("00A") == "00A"
    assert normalizza_codice("0 07") == "0 07"


def test_normalizza_codice_distingue_tipo_e_dominio():
    for valore in ("", "   "):
        with pytest.raises(ValueError, match="vuoto"):
            normalizza_codice(valore)
    for valore in (7, None):
        with pytest.raises(TypeError, match="atteso testo"):
            normalizza_codice(valore)
