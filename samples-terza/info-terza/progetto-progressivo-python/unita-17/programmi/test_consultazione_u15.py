"""Suite dei criteri di consultazione intercambiabili (tappa U15).

Casi pubblici PU15-01-PU15-08 verificabili sul dominio, tre casi propri
motivati — un confine, un difetto plausibile e una prova di conservazione
dello stato — e la variante breve PU15-08. I test non usano file né CLI: il
dominio è provabile senza interazione (PU15-10) e la regressione U5-U14 si
verifica con la suite cumulativa (PU15-09). Dati soltanto sintetici.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_consultazione_u15.py
"""
import pytest

from registro_consultazione_u15 import (
    ErroreConfigurazione,
    PoliticaDestinazione,
    PoliticaSoglia,
    PoliticaSogliaEsclusiva,
    seleziona_codici,
)
from registro_modello_u14 import RegistroPreventivi

CRITERI_PRINCIPALI = [
    pytest.param(PoliticaDestinazione("locale"), id="destinazione-locale"),
    pytest.param(PoliticaSoglia(500), id="soglia-500"),
]


def raccolta_canonica():
    """Raccolta di riferimento U15: 007/450, 012/0, 003/1200 nell'ordine noto."""
    raccolta = RegistroPreventivi()
    raccolta.inserisci("007", "locale", 450)
    raccolta.inserisci("012", "nazionale", 0)
    raccolta.inserisci("003", "locale", 1200)
    return raccolta


class MaiChiamata:
    """Criterio di sonda: solleva se il client lo chiama con raccolta vuota."""

    def ammette(self, preventivo):
        raise AssertionError("il criterio non doveva essere chiamato")


class EsitoTestuale:
    """Difetto plausibile: decisione giusta, risultato del tipo sbagliato."""

    def __init__(self, minimo_cent):
        self._minimo_cent = minimo_cent

    def ammette(self, preventivo):
        if preventivo.totale_cent >= self._minimo_cent:
            return "sì"
        return "no"


class EsitoNumerico:
    """Difetto plausibile: booleani espressi come interi 1 e 0."""

    def __init__(self, minimo_cent):
        self._minimo_cent = minimo_cent

    def ammette(self, preventivo):
        return int(preventivo.totale_cent >= self._minimo_cent)


class GuastoInLettura:
    """Criterio difettoso: solleva durante la scansione, dopo il primo sì."""

    def __init__(self, minimo_cent):
        self._minimo_cent = minimo_cent
        self._chiamate = 0

    def ammette(self, preventivo):
        self._chiamate = self._chiamate + 1
        if self._chiamate == 1:
            return True
        raise OSError("guasto simulato del collaboratore")


# --- Promesse comuni, verificate su entrambe le implementazioni ---


@pytest.mark.parametrize("criterio", CRITERI_PRINCIPALI)
def test_promise_comuni(criterio):
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    risultato = seleziona_codici(raccolta, criterio)
    assert isinstance(risultato, list)
    assert raccolta.per_lista() == prima
    assert [p.codice for p in raccolta.preventivi()] == ["007", "012", "003"]
    secondo = seleziona_codici(raccolta, criterio)
    assert risultato == secondo
    assert risultato is not secondo


@pytest.mark.parametrize("criterio", CRITERI_PRINCIPALI)
def test_pu15_01_vuoto_valido(criterio):
    vuota = RegistroPreventivi()
    assert seleziona_codici(vuota, criterio) == []
    assert vuota.numero == 0
    assert seleziona_codici(vuota, MaiChiamata()) == []


# --- PU15-03: la stessa chiamata usa le due implementazioni ---


def test_pu15_03_sostituzione():
    raccolta = raccolta_canonica()
    per_destinazione = PoliticaDestinazione("locale")
    per_soglia = PoliticaSoglia(500)
    assert type(per_destinazione) is not type(per_soglia)
    primi = seleziona_codici(raccolta, per_destinazione)
    secondi = seleziona_codici(raccolta, per_soglia)
    assert primi == ["007", "003"]
    assert secondi == ["003"]


# --- PU15-04: risultati specifici dei due criteri scelti ---


def test_pu15_04_risultati_specifici():
    raccolta = raccolta_canonica()
    assert seleziona_codici(raccolta, PoliticaDestinazione("locale")) == [
        "007",
        "003",
    ]
    assert seleziona_codici(raccolta, PoliticaDestinazione("nazionale")) == ["012"]
    assert seleziona_codici(raccolta, PoliticaSoglia(500)) == ["003"]
    assert seleziona_codici(raccolta, PoliticaSoglia(0)) == ["007", "012", "003"]
    assert seleziona_codici(raccolta, PoliticaSoglia(2000)) == []


# --- PU15-02 e PU15-05: zeri, ordine, identità di dominio, risultato protetto ---


def test_pu15_02_e_05_invarianti():
    raccolta = RegistroPreventivi()
    raccolta.inserisci("007", "locale", 450)
    raccolta.inserisci("7", "nazionale", 0)
    prima = raccolta.per_lista()
    risultato = seleziona_codici(raccolta, PoliticaSoglia(0))
    assert risultato == ["007", "7"]
    assert risultato[0] == "007"
    assert raccolta.per_lista() == prima
    risultato.append("999")
    assert raccolta.per_lista() == prima
    assert seleziona_codici(raccolta, PoliticaSoglia(0)) == ["007", "7"]


# --- PU15-06: configurazione invalida, errore prima di ogni effetto ---


def test_pu15_06_configurazione_invalida():
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    with pytest.raises(ErroreConfigurazione):
        PoliticaDestinazione("estera")
    with pytest.raises(ErroreConfigurazione):
        PoliticaSoglia(-1)
    with pytest.raises(ErroreConfigurazione):
        PoliticaSoglia(True)
    with pytest.raises(ErroreConfigurazione):
        PoliticaSoglia("500")
    assert raccolta.per_lista() == prima


# --- PU15-07: guasto del collaboratore, stato conservato, nessun parziale ---


def test_pu15_07_guasto_senza_successo():
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    with pytest.raises(OSError):
        seleziona_codici(raccolta, GuastoInLettura(0))
    assert raccolta.per_lista() == prima


# --- PU15-08: nuova implementazione integrata dallo stesso client ---


def test_pu15_08_nuova_implementazione():
    raccolta = raccolta_canonica()
    variante = PoliticaSogliaEsclusiva(450)
    assert seleziona_codici(raccolta, variante) == ["003"]
    assert variante.descrizione() == "soglia > 450 centesimi"
    # Il client non cambia: la stessa funzione serve le tre implementazioni.
    assert seleziona_codici(raccolta, PoliticaSoglia(450)) == ["007", "003"]


# --- Casi propri: confine, difetto plausibile, conservazione dello stato ---


def test_proprio_confine_della_soglia():
    raccolta = raccolta_canonica()
    assert seleziona_codici(raccolta, PoliticaSoglia(450)) == ["007", "003"]
    assert seleziona_codici(raccolta, PoliticaSogliaEsclusiva(450)) == ["003"]
    assert seleziona_codici(raccolta, PoliticaSoglia(1200)) == ["003"]


@pytest.mark.parametrize(
    "difettoso", [EsitoTestuale(500), EsitoNumerico(500)], ids=["testo", "interi"]
)
def test_proprio_difetti_plausibili(difettoso):
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    with pytest.raises(TypeError):
        seleziona_codici(raccolta, difettoso)
    assert raccolta.per_lista() == prima


def test_proprio_ripetibilita_e_stato():
    raccolta = raccolta_canonica()
    prima = raccolta.per_lista()
    criterio = PoliticaDestinazione("locale")
    primo = seleziona_codici(raccolta, criterio)
    secondo = seleziona_codici(raccolta, criterio)
    assert primo == secondo == ["007", "003"]
    assert raccolta.per_lista() == prima
    assert raccolta.numero == 3
