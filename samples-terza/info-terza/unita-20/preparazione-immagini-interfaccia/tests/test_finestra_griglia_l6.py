"""Verifica del coordinatore cooperativo a blocchi — Unità 20 (L6).

La suite verifica il coordinatore puro di `finestra_griglia.py` senza aprire
finestre grafiche:

- l'importazione del modulo non importa `tkinter` (nessuna interazione
  grafica involontaria; la GUI si avvia soltanto da `avvia_dimostrazione`);
- fotografica della configurazione, stati e avanzamento a blocchi;
- invalidazione delle callback con identificatore precedente, annullamento,
  nuovo lavoro e risultato parziale etichettato;
- registrazione degli errori di calcolo con messaggio conservato;
- conversione e validazione dei campi con messaggi su campo, dominio e
  correzione;
- conversione dalla posizione nel widget alla cella con offset, scala e
  bordi.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from finestra_griglia import (
    STATI_LAVORO,
    LavoroGriglia,
    annulla_lavoro,
    avvia_lavoro,
    converti_campo_intero,
    esegui_blocco,
    esito_artificiale,
    etichetta_progresso,
    etichetta_risultato,
    frazione_completata,
    nuova_configurazione,
    nuovo_lavoro,
    posizione_widget_a_cella,
    riepilogo_configurazione,
    risultato_completo,
)


def calcola_riga_artificiale(larghezza: int, limite: int):
    """Restituisce la funzione di riga dimostrativa per i test."""

    def calcola(q: int) -> tuple[int | None, ...]:
        return tuple(esito_artificiale(p, q, limite) for p in range(larghezza))

    return calcola


def esegui_fino_a_fine(lavoro: LavoroGriglia, calcola_riga, limite_passi: int = 1000) -> int:
    """Esegue blocchi con l'identificatore corrente fino a uscita da `in_calcolo`."""
    passi = 0
    while lavoro.stato == "in_calcolo" and passi < limite_passi:
        assert esegui_blocco(lavoro, lavoro.id_lavoro, calcola_riga) is True
        passi += 1
    return passi


def test_import_senza_tkinter_nel_processo_fresco() -> None:
    processo = subprocess.run(
        [
            sys.executable,
            "-c",
            "import finestra_griglia, sys; "
            "assert not hasattr(finestra_griglia, 'Tk'), 'Tk esposto dal modulo'; "
            "print('tkinter' in sys.modules)",
        ],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert processo.returncode == 0, processo.stderr
    assert processo.stdout.strip() == "False"


def test_nuovo_lavoro_pronto_con_fotografia() -> None:
    configurazione = nuova_configurazione(4, 2, 1, 7)
    lavoro = nuovo_lavoro(configurazione, 1)
    assert lavoro.stato == "pronto"
    assert lavoro.righe_completate == 0
    assert lavoro.righe == []
    assert frazione_completata(lavoro) == 0.0
    assert risultato_completo(lavoro) is False
    assert "non avviato" in etichetta_risultato(lavoro)
    assert "4x2" in riepilogo_configurazione(configurazione)


def test_blocchi_ordinati_fino_al_completamento() -> None:
    configurazione = nuova_configurazione(4, 2, 1, 7)
    lavoro = nuovo_lavoro(configurazione, 1)
    avvia_lavoro(lavoro)
    assert lavoro.stato == "in_calcolo"
    assert esegui_blocco(lavoro, 1, calcola_riga_artificiale(4, 7)) is True
    assert lavoro.righe_completate == 1
    assert lavoro.stato == "in_calcolo"
    assert frazione_completata(lavoro) == 0.5
    assert "parziale" in etichetta_risultato(lavoro)
    assert esegui_blocco(lavoro, 1, calcola_riga_artificiale(4, 7)) is True
    assert lavoro.stato == "completato"
    assert risultato_completo(lavoro) is True
    assert "completo" in etichetta_risultato(lavoro)
    assert "2 di 2" in etichetta_progresso(lavoro)
    # A lavoro completato le callback non producono più righe
    assert esegui_blocco(lavoro, 1, calcola_riga_artificiale(4, 7)) is False
    assert len(lavoro.righe) == 2


def test_blocco_piu_righe_e_contenuto_verificato() -> None:
    lavoro = nuovo_lavoro(nuova_configurazione(4, 2, 5, 7), 3)
    avvia_lavoro(lavoro)
    assert esegui_blocco(lavoro, 3, calcola_riga_artificiale(4, 7)) is True
    assert lavoro.stato == "completato"
    attese = tuple(tuple(esito_artificiale(p, q, 7) for p in range(4)) for q in range(2))
    assert tuple(lavoro.righe) == attese


def test_identificatore_precedente_senza_effetti() -> None:
    lavoro = nuovo_lavoro(nuova_configurazione(4, 2, 1, 7), 2)
    avvia_lavoro(lavoro)
    assert esegui_blocco(lavoro, 1, calcola_riga_artificiale(4, 7)) is False
    assert esegui_blocco(lavoro, 99, calcola_riga_artificiale(4, 7)) is False
    with pytest.raises(TypeError, match="id_lavoro"):
        esegui_blocco(lavoro, True, calcola_riga_artificiale(4, 7))
    assert lavoro.righe_completate == 0
    assert lavoro.stato == "in_calcolo"


def test_annullamento_conserva_parziale_e_invalida_callback() -> None:
    lavoro = nuovo_lavoro(nuova_configurazione(4, 4, 1, 7), 1)
    avvia_lavoro(lavoro)
    assert esegui_blocco(lavoro, 1, calcola_riga_artificiale(4, 7)) is True
    assert annulla_lavoro(lavoro) is True
    assert lavoro.stato == "annullato"
    assert len(lavoro.righe) == 1
    assert "parziale" in etichetta_risultato(lavoro) and "annullato" in etichetta_risultato(lavoro)
    assert risultato_completo(lavoro) is False
    # Le callback successive, anche con identificatore corretto, non avanzano
    assert esegui_blocco(lavoro, 1, calcola_riga_artificiale(4, 7)) is False
    assert annulla_lavoro(lavoro) is False


def test_nuovo_lavoro_dopo_annullamento_con_vecchio_id_inerte() -> None:
    configurazione = nuova_configurazione(4, 2, 1, 7)
    primo = nuovo_lavoro(configurazione, 1)
    avvia_lavoro(primo)
    esegui_blocco(primo, 1, calcola_riga_artificiale(4, 7))
    annulla_lavoro(primo)
    secondo = nuovo_lavoro(configurazione, 2)
    avvia_lavoro(secondo)
    # La callback del lavoro precedente non tocca il nuovo lavoro
    assert esegui_blocco(secondo, 1, calcola_riga_artificiale(4, 7)) is False
    assert secondo.righe_completate == 0
    passi = esegui_fino_a_fine(secondo, calcola_riga_artificiale(4, 7))
    assert passi == 2 and secondo.stato == "completato"


def test_errore_di_calcolo_registrato_con_messaggio() -> None:
    lavoro = nuovo_lavoro(nuova_configurazione(4, 2, 1, 7), 1)
    avvia_lavoro(lavoro)

    def riga_guasto(q: int) -> tuple[int | None, ...]:
        if q == 1:
            raise RuntimeError("sensore non disponibile")
        return (None, None, None, None)

    assert esegui_blocco(lavoro, 1, riga_guasto) is True
    assert esegui_blocco(lavoro, 1, riga_guasto) is False
    assert lavoro.stato == "errore"
    assert lavoro.errore == "sensore non disponibile"
    assert "errore" in etichetta_risultato(lavoro)
    assert risultato_completo(lavoro) is False


def test_esito_artificiale_deterministico_con_none_e_zero() -> None:
    assert esito_artificiale(0, 0, 7) is None
    assert esito_artificiale(3, 4, 7) is None
    valori = {esito_artificiale(p, q, 7) for p in range(7) for q in range(7)}
    assert None in valori and 0 in valori
    assert all(v is None or 0 <= v <= 7 for v in valori)
    assert esito_artificiale(1, 0, 7) == esito_artificiale(1, 0, 7)


def test_converti_campo_intero_con_messaggi() -> None:
    assert converti_campo_intero("80", "larghezza", 1, 800) == 80
    assert converti_campo_intero("  60 ", "altezza", 1, 600) == 60
    with pytest.raises(ValueError, match="larghezza.*1.*800.*abc"):
        converti_campo_intero("abc", "larghezza", 1, 800)
    with pytest.raises(ValueError, match="larghezza.*1.*800"):
        converti_campo_intero("1000", "larghezza", 1, 800)
    with pytest.raises(ValueError, match="righe per blocco"):
        converti_campo_intero("0", "righe per blocco", 1, 600)
    with pytest.raises(TypeError, match="larghezza"):
        converti_campo_intero(None, "larghezza", 1, 800)


def test_posizione_widget_a_cella_con_offset_scala_bordi() -> None:
    assert posizione_widget_a_cella(8, 8, 8, 8, 1, 4, 2) == (0, 0)
    assert posizione_widget_a_cella(11, 9, 8, 8, 1, 4, 2) == (3, 1)
    assert posizione_widget_a_cella(8 + 2 * 3, 8, 8, 8, 2, 4, 2) == (3, 0)
    assert posizione_widget_a_cella(8 + 2 * 3, 8 + 2 * 1, 8, 8, 2, 4, 2) == (3, 1)
    assert posizione_widget_a_cella(7, 8, 8, 8, 1, 4, 2) is None
    assert posizione_widget_a_cella(12, 8, 8, 8, 1, 4, 2) is None
    assert posizione_widget_a_cella(8, 10, 8, 8, 1, 4, 2) is None


def test_stati_previsti_e_rifiuto_input_invalidi() -> None:
    assert STATI_LAVORO == ("pronto", "in_calcolo", "annullato", "completato", "errore")
    with pytest.raises(ValueError, match="larghezza"):
        nuova_configurazione(0, 2, 1, 7)
    with pytest.raises(ValueError, match="righe_per_blocco"):
        nuova_configurazione(4, 2, 0, 7)
    with pytest.raises(TypeError):
        nuova_configurazione(True, 2, 1, 7)
    with pytest.raises(TypeError):
        nuovo_lavoro("non-configurazione", 1)
    with pytest.raises(TypeError):
        nuovo_lavoro(nuova_configurazione(4, 2, 1, 7), True)
    lavoro = nuovo_lavoro(nuova_configurazione(4, 2, 1, 7), 1)
    avvia_lavoro(lavoro)
    with pytest.raises(TypeError):
        esegui_blocco(lavoro, 1, "non-chiamabile")
    with pytest.raises(TypeError):
        avvia_lavoro("non-lavoro")
