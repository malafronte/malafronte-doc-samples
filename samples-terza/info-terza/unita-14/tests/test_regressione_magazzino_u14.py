"""Regressione funzionale del magazzino U14 rispetto ai valori U12/U13 (U14).

I moduli U13 vivono in `unita-13/` e non vengono importati: la regressione
esegue le **stesse sequenze pubblicate** nella sezione J di OOP-02 e nel
cap. PY-20 sul nuovo `Magazzino` e confronta proiezioni, esiti e stati con
gli attesi storici (dataset 007/012, riepilogo 2/6/800, politiche CSV e
JSON, alias dell'istanza aggiornata).

La rappresentazione `repr` non è un oracolo di correttezza: si confrontano
dati, esiti e effetti.
"""

from articolo_proprieta_u14 import Articolo, DatiArticolo
from magazzino_composto_u14 import Magazzino


def magazzino_canonico():
    magazzino = Magazzino()
    magazzino.inserisci("007", "Vite, lunga", 4, 25)
    magazzino.inserisci("012", 'Caffè "A"', 2, 350)
    return magazzino


def test_riepilogo_canonico_storico():
    # OOP-02 J: {'articoli': 2, 'quantita_totale': 6, 'valore_centesimi': 800}
    assert magazzino_canonico().riepilogo() == {
        "articoli": 2,
        "quantita_totale": 6,
        "valore_centesimi": 800,
    }


def test_riepilogo_sul_vuoto_tre_zeri():
    assert Magazzino().riepilogo() == {
        "articoli": 0,
        "quantita_totale": 0,
        "valore_centesimi": 0,
    }


def test_ricerca_esatta_con_zeri_significativi():
    magazzino = magazzino_canonico()
    assert magazzino.cerca("007") is not None
    assert magazzino.cerca("7") is None
    assert magazzino.cerca("012").descrizione == 'Caffè "A"'


def test_inserimento_duplicato_rifiutato_stato_invariato():
    magazzino = magazzino_canonico()
    try:
        magazzino.inserisci("007", "duplicato", 1, 1)
        raise AssertionError("duplicato accettato")
    except ValueError:
        pass
    assert magazzino.riepilogo()["articoli"] == 2
    assert magazzino.cerca("007").descrizione == "Vite, lunga"


def test_prima_posizione_non_confusa_con_assenza():
    magazzino = Magazzino()
    magazzino.inserisci("000", "primo", 1, 1)
    assert magazzino.cerca("000") is not None
    assert magazzino.modifica("000", "primo", 2, 1) is True
    assert magazzino.elimina("000") is True


def test_modifica_conserva_identita_e_aggiorna_insieme():
    magazzino = Magazzino()
    magazzino.inserisci("007", "Vite, lunga", 4, 25)
    articolo = Articolo("007", "Vite, lunga", 4, 25)
    alias = articolo
    articolo.aggiorna("Vite, lunga", 6, 25)
    assert alias.quantita == 6  # l'alias osserva la mutazione (contratto U13)


def test_modifica_invalida_ultimo_campo_stato_intatto():
    magazzino = magazzino_canonico()
    prima = magazzino.cerca("012")
    try:
        magazzino.modifica("012", 'Caffè "A"', 2, -350)
        raise AssertionError("candidato invalido accettato")
    except ValueError:
        pass
    dopo = magazzino.cerca("012")
    assert dopo == prima
    assert magazzino.riepilogo()["valore_centesimi"] == 800


def test_modifica_assente_false():
    magazzino = magazzino_canonico()
    assert magazzino.modifica("999", "x", 1, 1) is False


def test_eliminazione_esiti():
    magazzino = magazzino_canonico()
    assert magazzino.elimina("012") is True
    assert magazzino.elimina("012") is False
    assert magazzino.riepilogo() == {"articoli": 1, "quantita_totale": 4, "valore_centesimi": 100}


def test_snapshot_frozen_non_e_l_articolo():
    magazzino = magazzino_canonico()
    snapshot = magazzino.cerca("007")
    assert isinstance(snapshot, DatiArticolo)
    assert snapshot == DatiArticolo("007", "Vite, lunga", 4, 25)
    assert (snapshot == magazzino.cerca("007")) is True


def test_proiezioni_protette_dalla_mutazione_esterna():
    magazzino = magazzino_canonico()
    proiezioni = magazzino.articoli()
    try:
        proiezioni.append("intruso")
        raise AssertionError("append riuscita sulla tupla")
    except AttributeError:
        pass
    assert magazzino.riepilogo()["articoli"] == 2


def test_due_magazzini_indipendenti():
    primo = magazzino_canonico()
    secondo = Magazzino()
    secondo.inserisci("100", "Isolato", 1, 1)
    secondo.inserisci("007", "Altro sette", 9, 9)
    assert primo.riepilogo()["articoli"] == 2
    assert secondo.riepilogo()["articoli"] == 2
    assert primo.cerca("007").descrizione == "Vite, lunga"


def test_valore_derivato_delega_all_articolo():
    magazzino = Magazzino()
    magazzino.inserisci("007", "Vite, lunga", 4, 25)
    articolo = Articolo("007", "Vite, lunga", 4, 25)
    assert magazzino.riepilogo()["valore_centesimi"] == articolo.valore_centesimi == 100
