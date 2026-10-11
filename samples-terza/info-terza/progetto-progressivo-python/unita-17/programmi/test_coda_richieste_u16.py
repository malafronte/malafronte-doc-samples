"""Suite della coda di richieste di consultazione (tappa U16).

Casi pubblici PU16-01-PU16-09 verificabili sul dominio, tre casi propri
motivati - un confine, un difetto plausibile e una richiesta ripetuta - e la
politica di errore fronte, calcolo, estrazione. I test non usano file né CLI:
il dominio è provabile senza interazione e la regressione PU16-10 si verifica
con la suite cumulativa U5-U16. Dati soltanto sintetici.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_coda_richieste_u16.py
"""
import pytest

from coda_richieste_u16 import (
    CodaConcatenataU16,
    CodaDequeU16,
    RichiestaConsultazione,
    ServizioConsultazione,
)
from registro_consultazione_u15 import PoliticaDestinazione, PoliticaSoglia
from registro_modello_u14 import RegistroPreventivi

REPRESENTAZIONI = [
    pytest.param(CodaDequeU16, id="coda-deque"),
    pytest.param(CodaConcatenataU16, id="coda-concatenata"),
]


def raccolta_canonica():
    """Registro di riferimento U16: 007/locale/450, 012/nazionale/0, 003/locale/1200."""
    registro = RegistroPreventivi()
    registro.inserisci("007", "locale", 450)
    registro.inserisci("012", "nazionale", 0)
    registro.inserisci("003", "locale", 1200)
    return registro


def servizio_con_richieste(fabbrica, specifiche):
    """Costruisce un servizio e accoda le richieste `(codice, criterio)` indicate."""
    servizio = ServizioConsultazione(fabbrica())
    for codice, criterio in specifiche:
        servizio.accoda_richiesta(RichiestaConsultazione(codice, criterio))
    return servizio


RICHIESTE_CANONICHE = [
    ("R01", PoliticaDestinazione("locale")),
    ("R02", PoliticaSoglia(500)),
    ("R03", PoliticaSoglia(0)),
]


@pytest.mark.parametrize("fabbrica", REPRESENTAZIONI)
def test_pu16_01_nessuna_richiesta(fabbrica):
    registro = raccolta_canonica()
    prima = registro.per_lista()
    servizio = ServizioConsultazione(fabbrica())
    assert servizio.elabora_prossima(registro) is None
    assert servizio.elabora_tutte(registro) == []
    assert len(servizio) == 0
    assert registro.per_lista() == prima  # registro conservato


@pytest.mark.parametrize("fabbrica", REPRESENTAZIONI)
def test_pu16_02_ordine_di_arrivo(fabbrica):
    servizio = servizio_con_richieste(fabbrica, RICHIESTE_CANONICHE)
    esiti = servizio.elabora_tutte(raccolta_canonica())
    assert [e.codice for e in esiti] == ["R01", "R02", "R03"]
    assert [e.codici_ammessi for e in esiti] == [
        ("007", "003"),
        ("003",),
        ("007", "012", "003"),
    ]
    assert servizio.elaborate == 3


@pytest.mark.parametrize("fabbrica", REPRESENTAZIONI)
def test_pu16_03_inserimenti_intercalati(fabbrica):
    servizio = servizio_con_richieste(fabbrica, RICHIESTE_CANONICHE[:2])
    primo = servizio.elabora_prossima(raccolta_canonica())
    assert primo.codice == "R01"
    servizio.accoda_richiesta(RichiestaConsultazione("R03", PoliticaSoglia(0)))
    assert servizio.pendenti() == ["R02", "R03"]  # ordine residuo FIFO
    esiti = servizio.elabora_tutte(raccolta_canonica())
    assert [e.codice for e in esiti] == ["R02", "R03"]


def test_pu16_04_codici_con_zeri_e_importo_zero():
    servizio = servizio_con_richieste(CodaDequeU16, [("R03", PoliticaSoglia(0))])
    esito = servizio.elabora_prossima(raccolta_canonica())
    assert esito.codici_ammessi == ("007", "012", "003")  # zeri significativi conservati
    assert all(isinstance(codice, str) for codice in esito.codici_ammessi)


def test_pu16_05_sostituzione_della_rappresentazione():
    attesi = None
    for fabbrica in (CodaDequeU16, CodaConcatenataU16):
        servizio = servizio_con_richieste(fabbrica, RICHIESTE_CANONICHE)
        esiti = servizio.elabora_tutte(raccolta_canonica())
        osservati = [(e.codice, e.criterio, e.codici_ammessi) for e in esiti]
        if attesi is None:
            attesi = osservati
        else:
            assert osservati == attesi  # stesso client, stessi esiti
    for fabbrica in (CodaDequeU16, CodaConcatenataU16):
        with pytest.raises(IndexError):
            fabbrica().estrai()  # stesso comportamento sul vuoto
        with pytest.raises(IndexError):
            fabbrica().fronte()


@pytest.mark.parametrize("fabbrica", REPRESENTAZIONI)
def test_pu16_06_richiesta_invalida_prima_dell_accodamento(fabbrica):
    servizio = servizio_con_richieste(fabbrica, [("R01", PoliticaSoglia(0))])
    with pytest.raises(TypeError):
        servizio.accoda_richiesta("R02")
    with pytest.raises(ValueError):
        servizio.accoda_richiesta(RichiestaConsultazione("", PoliticaSoglia(0)))
    with pytest.raises(TypeError):
        servizio.accoda_richiesta(RichiestaConsultazione("R03", object()))
    assert servizio.pendenti() == ["R01"]  # contenuto e dimensione conservati
    assert len(servizio) == 1


@pytest.mark.parametrize("fabbrica", REPRESENTAZIONI)
def test_pu16_07_registro_vuoto(fabbrica):
    servizio = servizio_con_richieste(fabbrica, RICHIESTE_CANONICHE)
    registro = RegistroPreventivi()
    esiti = servizio.elabora_tutte(registro)
    assert [e.codice for e in esiti] == ["R01", "R02", "R03"]  # si completano in ordine
    assert [e.codici_ammessi for e in esiti] == [(), (), ()]


@pytest.mark.parametrize("fabbrica", REPRESENTAZIONI)
def test_pu16_08_uno_vuoto_reinserimento(fabbrica):
    servizio = servizio_con_richieste(fabbrica, [("R01", PoliticaSoglia(0))])
    assert servizio.elabora_prossima(raccolta_canonica()).codice == "R01"
    assert servizio.elabora_prossima(raccolta_canonica()) is None  # vuoto
    servizio.accoda_richiesta(RichiestaConsultazione("R02", PoliticaSoglia(500)))
    assert servizio.elabora_prossima(raccolta_canonica()).codici_ammessi == ("003",)


def test_pu16_09_conservazione_del_registro():
    registro = raccolta_canonica()
    prima = registro.per_lista()
    servizio = servizio_con_richieste(CodaDequeU16, RICHIESTE_CANONICHE)
    servizio.elabora_tutte(registro)
    assert registro.per_lista() == prima  # dati e ordine dell'archivio conservati
    assert len(prima) == 3


def test_caso_proprio_confine_della_soglia():
    """Caso proprio 1: la soglia uguale al totale ammette il preventivo."""
    servizio = servizio_con_richieste(CodaDequeU16, [("R01", PoliticaSoglia(450))])
    esito = servizio.elabora_prossima(raccolta_canonica())
    assert esito.codici_ammessi == ("007", "003")


class EsitoTestuale:
    """Difetto plausibile: decisione giusta, risultato del tipo sbagliato."""

    def __init__(self, minimo_cent):
        self._minimo_cent = minimo_cent

    def descrizione(self):
        return f"soglia >= {self._minimo_cent} centesimi"

    def ammette(self, preventivo):
        return "sì" if preventivo.totale_cent >= self._minimo_cent else "no"


def test_caso_proprio_difetto_plausibile_conserva_la_richiesta():
    """Caso proprio 2: esito non booleano; la richiesta resta al fronte."""
    servizio = servizio_con_richieste(
        CodaConcatenataU16, [("R01", EsitoTestuale(500)), ("R02", PoliticaSoglia(0))]
    )
    with pytest.raises(TypeError):
        servizio.elabora_prossima(raccolta_canonica())
    assert servizio.pendenti() == ["R01", "R02"]  # fronte, calcolo, estrazione
    assert len(servizio) == 2


def test_caso_proprio_richiesta_ripetuta():
    """Caso proprio 3: lo stesso codice su due richieste distinte, entrambe elaborate."""
    servizio = servizio_con_richieste(
        CodaDequeU16, [("R01", PoliticaSoglia(0)), ("R01", PoliticaSoglia(500))]
    )
    esiti = servizio.elabora_tutte(raccolta_canonica())
    assert [e.codice for e in esiti] == ["R01", "R01"]
    assert [e.codici_ammessi for e in esiti] == [("007", "012", "003"), ("003",)]
