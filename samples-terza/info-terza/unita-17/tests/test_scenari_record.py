"""Prove su record, indice e costi in funzione dell'altezza — Unità 17.

Casi semantici del piano §15.1: associazioni fra chiavi e record, ordine
della vista, conservazione del successore, e confronto deterministico
degli ordini di inserimento del dataset D2 con i conteggi dichiarati.
"""

import dataclasses

import pytest

from confronto_altezze_u17 import AlberoBSTContatore, misura_costruzione, misura_ricerca
from indice_schede_u17 import (
    Scheda,
    costruisci_indice,
    schede_canoniche,
    verifica_corrispondenza,
)

D1 = [40, 20, 60, 10, 30, 50, 70, 25, 35, 55]
D2_BILINEARE = [4, 2, 6, 1, 3, 5, 7]
D2_CATENA = [1, 2, 3, 4, 5, 6, 7]


def test_record_immutabili_e_indice_ordinato():
    indice = costruisci_indice(schede_canoniche())
    assert len(indice) == 10
    assert [chiave for chiave, _ in indice.voci_ordinate()] == [
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
    assert verifica_corrispondenza(indice) is True
    with pytest.raises(dataclasses.FrozenInstanceError):
        indice.cerca(30).titolo = "modificato"


def test_indice_ricerca_aggiornamento_e_cancellazione():
    indice = costruisci_indice(schede_canoniche())
    # Ricerca di 35.
    assert indice.cerca(35) == Scheda(35, "sottovoce di 30")
    # Aggiornamento del titolo di 30: la chiave resta, cambia il record.
    indice.aggiorna(30, Scheda(30, "voce aggiornata"))
    assert indice.cerca(30).titolo == "voce aggiornata"
    assert len(indice) == 10
    # Cancellazione della radice 40: il successore 50 conserva il proprio record.
    indice.rimuovi(40)
    assert len(indice) == 9
    assert indice.cerca(50) == Scheda(50, "successore della radice")
    assert indice.cerca(55) == Scheda(55, "sottovoce di 50")
    assert [chiave for chiave, _ in indice.voci_ordinate()] == [
        10,
        20,
        25,
        30,
        35,
        50,
        55,
        60,
        70,
    ]
    assert verifica_corrispondenza(indice) is True


def test_indice_intervallo_di_codici():
    indice = costruisci_indice(schede_canoniche())
    assert [chiave for chiave, _ in indice.intervallo(25, 55)] == [25, 30, 35, 40, 50, 55]
    assert indice.intervallo(36, 39) == []


def test_codice_ripetuto_rifiutato_prima_della_consegna():
    duplicati = [Scheda(30, "prima"), Scheda(30, "seconda")]
    with pytest.raises(ValueError):
        costruisci_indice(duplicati)


def test_d2_altezze_e_nodi_esaminati_nella_costruzione():
    albero_b, costruzione_b, altezza_b = misura_costruzione(D2_BILINEARE)
    albero_c, costruzione_c, altezza_c = misura_costruzione(D2_CATENA)
    assert altezza_b == 2
    assert altezza_c == 6
    assert costruzione_b == 10
    assert costruzione_c == 21
    assert albero_b.inordine() == albero_c.inordine() == sorted(D2_BILINEARE)
    assert misura_ricerca(albero_b, 7) == 3
    assert misura_ricerca(albero_b, 8) == 3
    assert misura_ricerca(albero_c, 7) == 7
    assert misura_ricerca(albero_c, 8) == 7


def test_traccia_della_ricerca_su_d1():
    albero = AlberoBSTContatore()
    for chiave in D1:
        albero.inserisci(chiave, chiave)
    trovato, percorso = albero.ricerca_con_traccia(35)
    assert trovato is True
    assert percorso == [40, 20, 30, 35]
    trovato, percorso = albero.ricerca_con_traccia(52)
    assert trovato is False
    assert percorso == [40, 60, 50, 55]


def test_l_inserimento_della_prima_radice_non_esamina_nodi():
    albero = AlberoBSTContatore()
    albero.azzera_contatore()
    albero.inserisci(40, 40)
    assert albero.nodi_esaminati == 0
    albero.inserisci(20, 20)
    assert albero.nodi_esaminati == 1
    albero.inserisci(60, 60)
    assert albero.nodi_esaminati == 2
