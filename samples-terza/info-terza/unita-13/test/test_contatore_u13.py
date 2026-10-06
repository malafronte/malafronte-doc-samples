"""Prove del contatore con capacità: casi OGG-01…OGG-12.

Ogni prova deriva l'atteso dal **contratto** del capitolo: costruzione,
successo, rifiuto, errore di input, indipendenza delle istanze, alias e
proiezione dello stato.
"""

import pytest
from contatore_capacita_u13 import (
    SEQUENZA_CANONICA,
    ContatoreCapacita,
    esegui_sequenza_classe,
    esegui_sequenza_procedurale,
)
from istanze_alias_self_u13 import ContatoreConSelfRiassegnato

# --- OGG-01 ---------------------------------------------------------------


def test_ogg_01_costruzioni_valide():
    """OGG-01: capacità 5 con quantità 0 e 5, capacità 0 con quantità 0."""
    assert ContatoreCapacita(5, 0).stato() == {"capacita": 5, "quantita": 0}
    assert ContatoreCapacita(5, 5).stato() == {"capacita": 5, "quantita": 5}
    assert ContatoreCapacita(0, 0).stato() == {"capacita": 0, "quantita": 0}
    assert ContatoreCapacita(5).stato() == {"capacita": 5, "quantita": 0}


# --- OGG-02 ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("capacita", "quantita"),
    [(-1, 0), (5, -1), (5, 6), (0, 1)],
)
def test_ogg_02_costruzioni_fuori_contratto(capacita, quantita):
    """OGG-02: capacità negativa o quantità fuori intervallo producono ValueError."""
    with pytest.raises(ValueError):
        ContatoreCapacita(capacita, quantita)


def test_ogg_02_chiamata_fallita_non_restituisce_un_istanza():
    """OGG-02: la costruzione fallita non ha un risultato `False` né un'istanza."""
    with pytest.raises(ValueError):
        ContatoreCapacita(5, 6)


# --- OGG-03 ---------------------------------------------------------------


@pytest.mark.parametrize("unita", [1.5, "3", True, False])
def test_ogg_03_tipi_non_ammessi(unita):
    """OGG-03: float, testo e booleani sono rifiutati, senza conversione silenziosa."""
    contatore = ContatoreCapacita(5, 0)
    with pytest.raises(ValueError):
        contatore.aggiungi(unita)
    with pytest.raises(ValueError):
        contatore.preleva(unita)
    assert contatore.stato() == {"capacita": 5, "quantita": 0}


# --- OGG-04 ---------------------------------------------------------------


def test_ogg_04_sequenza_canonica():
    """OGG-04: esiti e ogni stato intermedio coincidono con la tabella."""
    passi = esegui_sequenza_classe(5, 0, SEQUENZA_CANONICA)
    assert [p[2] for p in passi] == [True, False, True, False, True, True]
    assert [p[3] for p in passi] == [p[3] for p in SEQUENZA_CANONICA]


def test_ogg_04_equivalenza_con_la_versione_procedurale():
    """OGG-04: le due versioni coincidono passo per passo."""
    assert esegui_sequenza_classe(5, 0, SEQUENZA_CANONICA) == esegui_sequenza_procedurale(
        5, 0, SEQUENZA_CANONICA
    )


# --- OGG-05 ---------------------------------------------------------------


def test_ogg_05_operazione_zero():
    """OGG-05: la quantità zero è valida, restituisce True e non cambia lo stato."""
    contatore = ContatoreCapacita(5, 3)
    assert contatore.aggiungi(0) is True
    assert contatore.preleva(0) is True
    assert contatore.stato() == {"capacita": 5, "quantita": 3}


def test_ogg_05_zero_distinto_dal_negativo():
    """OGG-05: il negativo è un errore di input, non un rifiuto."""
    contatore = ContatoreCapacita(5, 3)
    with pytest.raises(ValueError):
        contatore.aggiungi(-1)


# --- OGG-06 ---------------------------------------------------------------


def test_ogg_06_due_istanze_intercalate():
    """OGG-06: quantità e capacità restano indipendenti."""
    primo = ContatoreCapacita(5, 0)
    secondo = ContatoreCapacita(8, 2)
    assert primo.aggiungi(4) is True
    assert secondo.preleva(1) is True
    assert secondo.aggiungi(8) is False
    assert primo.stato() == {"capacita": 5, "quantita": 4}
    assert secondo.stato() == {"capacita": 8, "quantita": 1}


# --- OGG-07 ---------------------------------------------------------------


def test_ogg_07_alias_della_prima_istanza():
    """OGG-07: la mutazione è visibile da entrambi i nomi, la seconda è invariata."""
    primo = ContatoreCapacita(5, 0)
    secondo = ContatoreCapacita(5, 0)
    alias = primo
    alias.aggiungi(3)
    assert primo is alias
    assert primo.stato() == {"capacita": 5, "quantita": 3}
    assert secondo.stato() == {"capacita": 5, "quantita": 0}


# --- OGG-08 ---------------------------------------------------------------


def test_ogg_08_riassegnamento_locale_di_self():
    """OGG-08: il nome del chiamante resta associato all'istanza originaria."""
    c = ContatoreConSelfRiassegnato(4)
    risultato = c.incrementa_su_altro(9)
    assert risultato == 9
    assert c.valore == 4


# --- OGG-09 ---------------------------------------------------------------


def test_ogg_09_lista_copiata_superficialmente():
    """OGG-09: contenitori distinti, elementi condivisi; la nuova costruzione è diversa."""
    primo = ContatoreCapacita(5, 1)
    ricostruito = ContatoreCapacita(5, 1)
    assert ricostruito is not primo
    assert ricostruito.stato() == primo.stato()
    lista = [primo, ContatoreCapacita(5, 2)]
    copia = lista.copy()
    assert copia is not lista
    assert copia[0] is lista[0]
    copia[0].aggiungi(3)
    assert lista[0].stato() == {"capacita": 5, "quantita": 4}
    # La nuova costruzione non ha partecipato alla mutazione.
    assert ricostruito.stato() == {"capacita": 5, "quantita": 1}


# --- OGG-10 ---------------------------------------------------------------


def test_ogg_10_snapshot_modificato_non_incide():
    """OGG-10: modificare il risultato di stato() non modifica l'istanza."""
    contatore = ContatoreCapacita(5, 2)
    snapshot = contatore.stato()
    snapshot["quantita"] = 99
    snapshot["capacita"] = 0
    assert contatore.stato() == {"capacita": 5, "quantita": 2}
    assert contatore.spazio_libero() == 3


# --- OGG-11 ---------------------------------------------------------------


def test_ogg_11_chiamata_legata_ed_esplicita():
    """OGG-11: stessi risultati e stati su istanze equivalenti."""
    legata = ContatoreCapacita(5, 0)
    esplicita = ContatoreCapacita(5, 0)
    assert legata.aggiungi(3) is True
    assert ContatoreCapacita.aggiungi(esplicita, 3) is True
    assert legata.stato() == esplicita.stato() == {"capacita": 5, "quantita": 3}


# --- OGG-12 ---------------------------------------------------------------


# Frammenti deliberatamente difettosi: producono i sintomi spiegati nel
# capitolo e non fanno parte dei programmi validi del corso.
class _InizializzatoreConRisultato:
    """Difetto: `__init__` cerca di restituire un valore."""

    def __init__(self, valore):
        self.valore = valore
        return valore


class _MetodoSenzaIstanza:
    """Difetto: il metodo non dichiara il parametro dell'istanza."""

    def __init__(self, valore):
        self.valore = valore

    def incrementa(quantita):
        return quantita


def test_ogg_12_return_da_inizializzatore():
    """OGG-12: un valore restituito da `__init__` è un errore di linguaggio."""
    with pytest.raises(TypeError):
        _InizializzatoreConRisultato(3)


def test_ogg_12_self_omesso():
    """OGG-12: senza il parametro dell'istanza la chiamata legata non associa gli argomenti."""
    difettoso = _MetodoSenzaIstanza(2)
    with pytest.raises(TypeError):
        difettoso.incrementa(3)


def test_ogg_12_locale_al_posto_dell_attributo():
    """OGG-12: il metodo termina e lo stato resta invariato."""
    from istanze_alias_self_u13 import ContatoreConLocale

    difettoso = ContatoreConLocale(2)
    assert difettoso.incrementa(3) == 5
    assert difettoso.valore == 2
