"""Prove delle applicazioni - Unità 16 (PY-23 C e PY-24 E-F).

Il modulo verifica il modello a raddoppio dell'array dinamico, il servizio di
annullamento e l'elaborazione FIFO delle richieste, con i dataset canonici dei
problemi svolti e i casi di errore che devono conservare lo stato.
"""

from __future__ import annotations

import pytest

from annullamenti_u16 import ContatoreAnnullabile
from array_dinamico_modello_u16 import ArrayDinamicoModello, traccia_accodamenti
from pile_code_u16 import CodaConcatenata, CodaDeque
from richieste_u16 import Richiesta, ServizioRichieste


def test_modello_raddoppio_su_dieci_accodamenti():
    traccia = traccia_accodamenti(10)
    copie = sum(riga["copiate"] for riga in traccia)
    scritture = sum(riga["scritture"] for riga in traccia)
    assert copie == 14  # 2 + 4 + 8 riferimenti copiati
    assert scritture == 10
    assert copie + scritture == 24
    assert [riga["operazione"] for riga in traccia if riga["copiate"] > 0] == [3, 5, 9]
    assert traccia[-1]["lunghezza_dopo"] == 10
    assert traccia[-1]["capacita_dopo"] == 16


def test_modello_separa_lunghezza_e_capacita():
    array = ArrayDinamicoModello(capacita_iniziale=2)
    array.appendi(12)
    assert array.dimensione == 1
    assert array.posti_riservati() == 2


def test_annullamenti_canonici_e_cronologia_vuota():
    contatore = ContatoreAnnullabile(5)
    contatore.aggiorna(3)
    contatore.aggiorna(4)
    assert contatore.valore == 12
    assert contatore.annulla() is True
    assert contatore.valore == 8
    assert contatore.annulla() is True
    assert contatore.valore == 5
    assert contatore.annulla() is False  # politica del vuoto dichiarata
    assert contatore.valore == 5
    assert len(contatore) == 0


def test_aggiornamento_invalido_conserva_stato_e_cronologia():
    contatore = ContatoreAnnullabile(5)
    contatore.aggiorna(3)
    with pytest.raises(TypeError):
        contatore.aggiorna(True)  # bool non è un delta ammesso
    with pytest.raises(ValueError):
        contatore.aggiorna(-100)  # il risultato sarebbe negativo
    assert contatore.valore == 8
    assert len(contatore) == 1
    assert contatore.annulla() is True
    assert contatore.valore == 5


def test_richieste_canoniche_tempi_cumulativi():
    servizio = ServizioRichieste(CodaDeque())
    for codice, durata in [("R01", 2), ("R02", 1), ("R03", 3)]:
        servizio.accoda_richiesta(Richiesta(codice, durata))
    esiti = servizio.elabora_tutte()
    assert [esito.codice for esito in esiti] == ["R01", "R02", "R03"]
    assert [esito.completata_a for esito in esiti] == [2, 3, 6]
    assert servizio.tempo_trascorso == 6
    assert servizio.elabora_prossima() is None  # vuoto: nessun esito, stato conservato


@pytest.mark.parametrize("fabbrica", [CodaDeque, CodaConcatenata])
def test_stesso_client_con_le_due_rappresentazioni(fabbrica):
    servizio = ServizioRichieste(fabbrica())
    for codice, durata in [("R01", 2), ("R02", 1), ("R03", 3)]:
        servizio.accoda_richiesta(Richiesta(codice, durata))
    assert servizio.pendenti() == ["R01", "R02", "R03"]
    assert servizio.elabora_prossima().codice == "R01"
    servizio.accoda_richiesta(Richiesta("R04", 1))
    assert servizio.pendenti() == ["R02", "R03", "R04"]  # ordine residuo FIFO
    esiti = servizio.elabora_tutte()
    assert [esito.codice for esito in esiti] == ["R02", "R03", "R04"]
    assert [esito.completata_a for esito in esiti] == [3, 6, 7]


def test_richiesta_invalida_prima_dell_accodamento():
    servizio = ServizioRichieste(CodaDeque())
    servizio.accoda_richiesta(Richiesta("R01", 2))
    with pytest.raises(ValueError):
        servizio.accoda_richiesta(Richiesta("", 1))
    with pytest.raises(ValueError):
        servizio.accoda_richiesta(Richiesta("R02", 0))
    with pytest.raises(TypeError):
        servizio.accoda_richiesta(Richiesta("R03", True))
    with pytest.raises(TypeError):
        servizio.accoda_richiesta("R04")
    assert servizio.pendenti() == ["R01"]  # coda e dimensione conservate
    assert len(servizio) == 1


def test_registro_vuoto_e_passaggio_al_vuoto_con_reinserimento():
    servizio = ServizioRichieste(CodaConcatenata())
    assert servizio.elabora_tutte() == []
    servizio.accoda_richiesta(Richiesta("R01", 2))
    assert servizio.elabora_prossima().codice == "R01"
    assert servizio.elabora_prossima() is None
    servizio.accoda_richiesta(Richiesta("R02", 1))  # reinserimento dopo il vuoto
    assert servizio.elabora_prossima().codice == "R02"
    assert servizio.tempo_trascorso == 3
