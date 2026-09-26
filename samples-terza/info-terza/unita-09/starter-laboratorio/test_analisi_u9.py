"""Suite del LAB-PY-U9 - versione di partenza, casi pubblici L01-L12.

La prima esecuzione della suite sullo starter **deve fallire**: i corpi da
completare sollevano `NotImplementedError` con il nome della fase del
laboratorio e i fallimenti attesi sono quelli, mai errori di import o di
sintassi. Se durante la raccolta compare un prompt interattivo, l'import non
è ancora pulito.

Fallimenti attesi della versione di partenza:
- `test_l01_lista_vuota`, `test_l02_quattro_valori_visite_4_e_8`,
  `test_l03_casi_di_confine`: `riepilogo_una_scansione` da completare (L1);
- `test_l04_conta_coppie` e `test_conta_coppie_esegue_i_cicli_del_modello`:
  `conta_coppie` da completare (L2);
- `test_l08_cinque_campioni_del_misuratore`,
  `test_l10_grafico_su_dati_esatti`,
  `test_l11_misura_e_grafico_da_durate_reali`: regione cronometrata e grafico
  da completare (L3);
- `test_l12_caso_dello_studente`: caso proprio non ancora progettato.

Superano già nella versione di partenza i casi sui materiali forniti: L05-L07
sulle funzioni complete di Fibonacci, L09 sulla sintesi dei campioni, più i
controlli di servizio. Nessun test impone che un algoritmo sia più veloce di
un altro: le prove del timer controllano il protocollo e la forma dei dati.

Il caso L12 è lasciato vuoto: è il caso progettato dallo studente.
"""

import inspect
import os

import matplotlib
import pytest

# Il test non apre finestre: si usa il backend senza schermo prima di importare
# il modulo del grafico, che importa `matplotlib.pyplot`.
matplotlib.use("Agg")

import grafici_u9 as grafici
import misure_u9 as misure
from analisi_u9 import (
    conta_coppie,
    fibonacci_diretto,
    fibonacci_diretto_osservato,
    fibonacci_iter,
    fibonacci_mem,
    fibonacci_mem_osservata,
    memoria_delle_basi,
    riepilogo_due_scansioni,
    riepilogo_una_scansione,
)


class ListaCheContaLeVisite(list):
    """Lista che annota quante volte un ciclo ne visita gli elementi.

    Strumento di verifica del test: nel modello di costo del capitolo una
    VISITA è una esecuzione del corpo del ciclo che attraversa la lista.
    Qui ogni valore consegnato a un ciclo viene contato, così il numero delle
    visite si osserva senza cambiare le funzioni misurate. L'uso dei metodi
    speciali anticipa un argomento trattato in una unità successiva e qui si
    limita a contare: per le classi si attenda la relativa trattazione.
    """

    def __init__(self, valori):
        super().__init__(valori)
        self.visite = 0

    def __iter__(self):
        for valore in super().__iter__():
            self.visite += 1
            yield valore


# --- L01 - L03: riepiloghi equivalenti --------------------------------------


def test_l01_lista_vuota():
    """L01 — `(0, 0)`, zero visite nel modello, chiamata comunque valida."""
    due = ListaCheContaLeVisite([])
    assert riepilogo_due_scansioni(due) == (0, 0)
    assert due.visite == 0
    una = ListaCheContaLeVisite([])
    assert riepilogo_una_scansione(una) == (0, 0)
    assert una.visite == 0
    # Zero visite nel modello non significa zero lavoro: la chiamata resta
    # valida e i suoi costi fissi non vengono cancellati dal conteggio.


def test_l02_quattro_valori_visite_4_e_8():
    """L02 — `[3, -2, 0, 5]`: `(6, 2)`, 8 visite contro 4, argomento invariato."""
    due = ListaCheContaLeVisite([3, -2, 0, 5])
    assert riepilogo_due_scansioni(due) == (6, 2)
    assert due.visite == 8

    una = ListaCheContaLeVisite([3, -2, 0, 5])
    assert riepilogo_una_scansione(una) == (6, 2)
    assert una.visite == 4

    # Nessuna mutazione: le due funzioni leggono la stessa lista.
    assert due == [3, -2, 0, 5]
    assert una == [3, -2, 0, 5]


def test_l03_casi_di_confine():
    """L03 — zero distinto da positivo: attesi del contratto comune."""
    casi = [([0], (0, 0)), ([-3, -1], (-4, 0)), ([2, 2], (4, 2))]
    for valori, atteso in casi:
        assert riepilogo_due_scansioni(list(valori)) == atteso
        assert riepilogo_una_scansione(list(valori)) == atteso


# --- L04: coppie i < j ------------------------------------------------------


def test_l04_conta_coppie():
    """L04 — 0, 0, 1, 6, 10 per n = 0, 1, 2, 4, 5, contatore indipendente."""
    assert [conta_coppie(n) for n in (0, 1, 2, 4, 5)] == [0, 0, 1, 6, 10]
    # Il contatore è locale a ogni chiamata: nessuno stato si accumula.
    assert conta_coppie(5) == 10
    assert conta_coppie(0) == 0
    assert conta_coppie(5) == 10


# --- L05 - L07: Fibonacci, valori e contatori -------------------------------


def test_l05_valori_di_fibonacci():
    """L05 — F(0), F(1), F(4), F(10) = 0, 1, 3, 55 per ogni variante."""
    attesi = {0: 0, 1: 1, 4: 3, 10: 55}
    for n, valore in attesi.items():
        assert fibonacci_diretto(n) == valore
        assert fibonacci_iter(n) == valore
        assert fibonacci_mem(n, memoria_delle_basi()) == valore


def test_l06_contatori_di_f4():
    """L06 — F(4): diretta C/D = 9/4; memoria nuova C/D/S = 7/4/3."""
    diretto = [0, 0]
    assert fibonacci_diretto_osservato(4, diretto) == 3
    assert diretto == [9, 4]

    statistiche = [0, 0, 0]
    assert fibonacci_mem_osservata(4, memoria_delle_basi(), statistiche) == 3
    assert statistiche == [7, 4, 3]


def test_l07_memoria_riutilizzata():
    """L07 — F(4) ripetuto 1/1/0 e F(5) dopo F(4) 3/2/1, etichette diverse."""
    memoria = memoria_delle_basi()
    statistiche = [0, 0, 0]
    fibonacci_mem_osservata(4, memoria, statistiche)
    assert statistiche == [7, 4, 3]

    esperimenti = {}
    statistiche = [0, 0, 0]
    assert fibonacci_mem_osservata(4, memoria, statistiche) == 3
    esperimenti["F(4) ripetuto — memoria già popolata"] = tuple(statistiche)

    statistiche = [0, 0, 0]
    assert fibonacci_mem_osservata(5, memoria, statistiche) == 5
    esperimenti["F(5) — aggiunta alla memoria fino a 4"] = tuple(statistiche)

    # Stati iniziali diversi della memoria: etichette diverse e nessuna
    # aggregazione in un'unica sintesi.
    assert esperimenti == {
        "F(4) ripetuto — memoria già popolata": (1, 1, 0),
        "F(5) — aggiunta alla memoria fino a 4": (3, 2, 1),
    }
    assert len(set(esperimenti)) == 2


# --- L08 - L09: campioni e sintesi ------------------------------------------


def test_l08_cinque_campioni_del_misuratore():
    """L08 — cinque campioni numerici non negativi, argomento invariato."""
    valori = [3, -2, 0, 5]
    campioni = misure.misura_scansione(riepilogo_due_scansioni, valori, 5, 2)
    assert len(campioni) == 5
    for campione in campioni:
        assert isinstance(campione, (int, float))
        assert campione >= 0
    assert valori == [3, -2, 0, 5]


def test_l09_mediana_artificiale():
    """L09 — mediana 3 sui campioni artificiali [5, 1, 4, 2, 3].

    Il dato è artificiale, in unità convenzionali, e serve soltanto a
    verificare la sintesi: non è una misura di tempo.
    """
    sintesi = misure.sintetizza_campioni([5, 1, 4, 2, 3])
    assert sintesi["mediana"] == 3
    assert sintesi["minimo"] == 1
    assert sintesi["massimo"] == 5


# --- L10 - L11: grafico esatto e grafico da misure reali --------------------


def test_l10_grafico_su_dati_esatti(tmp_path):
    """L10 — serie esatte n e 2n: titolo, assi, legenda, serie, tabella, file."""
    dimensioni, serie_a, serie_b = grafici.dati_visite_esatte()
    assert serie_a == [2, 4, 8, 16]
    assert serie_b == [4, 8, 16, 32]

    righe = grafici.tabella_equivalente(dimensioni, serie_a, serie_b)
    assert righe == [
        {"dimensione": 2, "serie_a": 2, "serie_b": 4},
        {"dimensione": 4, "serie_a": 4, "serie_b": 8},
        {"dimensione": 8, "serie_a": 8, "serie_b": 16},
        {"dimensione": 16, "serie_a": 16, "serie_b": 32},
    ]

    percorso = os.path.join(str(tmp_path), "confronto-scansioni.png")
    fig = grafici.grafico_scansioni(dimensioni, serie_a, serie_b, percorso)
    assert fig is not None

    asse = fig.get_axes()[0]
    assert asse.get_title() != ""
    assert asse.get_title() == grafici.ETICHETTE["titolo"]
    assert asse.get_xlabel() != ""
    assert asse.get_xlabel() == grafici.ETICHETTE["x"]
    assert asse.get_ylabel() != ""
    assert asse.get_ylabel() == grafici.ETICHETTE["y"]

    legenda = asse.get_legend()
    assert legenda is not None
    etichette_legenda = [testo.get_text() for testo in legenda.get_texts()]
    assert etichette_legenda == [
        grafici.ETICHETTE["serie_a"],
        grafici.ETICHETTE["serie_b"],
    ]
    assert all(etichetta != "" for etichetta in etichette_legenda)

    linee = asse.get_lines()
    assert len(linee) == 2
    assert list(linee[0].get_xdata()) == dimensioni
    assert list(linee[0].get_ydata()) == serie_a
    assert list(linee[1].get_ydata()) == serie_b
    # Marcatori diversi: la serie resta leggibile anche senza il colore.
    assert linee[0].get_marker() != linee[1].get_marker()

    assert os.path.getsize(percorso) > 0


def test_l11_misura_e_grafico_da_durate_reali(tmp_path):
    """L11 — campioni e metadati rintracciabili, salvataggio fuori dal timer."""
    sorgente_misura = inspect.getsource(misure.misura_scansione)
    assert sorgente_misura.count("perf_counter") == 2
    assert "savefig" not in sorgente_misura
    assert "print(" not in sorgente_misura

    sorgente_grafico = inspect.getsource(grafici.grafico_scansioni)
    assert "perf_counter" not in sorgente_grafico

    righe = misure.esperimento_scansioni(
        dimensioni=[10, 100], ripetizioni=5, chiamate_per_lotto=2
    )
    assert len(righe) == 2 * 2 * 5
    for riga in righe:
        assert set(riga) == set(misure.COLONNE_TABELLA)
        assert riga["esperimento"] != ""
        assert riga["algoritmo"] in (
            "riepilogo_una_scansione",
            "riepilogo_due_scansioni",
        )
        assert riga["significato_dimensione"] != ""
        assert riga["famiglia_input"] != ""
        assert riga["stato_memoria"] == "non applicabile"
        assert riga["ripetizione"] in (1, 2, 3, 4, 5)
        assert riga["chiamate_per_lotto"] == 2
        assert riga["durata_per_chiamata_s"] >= 0
        assert riga["durata_lotto_s"] == riga["durata_per_chiamata_s"] * riga["chiamate_per_lotto"]

    dimensioni = [10, 100]
    mediane_una = grafici.serie_mediane(righe, "riepilogo_una_scansione", dimensioni)
    mediane_due = grafici.serie_mediane(righe, "riepilogo_due_scansioni", dimensioni)
    percorso = os.path.join(str(tmp_path), "confronto-scansioni.png")
    fig = grafici.grafico_scansioni(dimensioni, mediane_una, mediane_due, percorso)
    assert fig is not None
    assert os.path.getsize(percorso) > 0
    asse = fig.get_axes()[0]
    dati_una = list(asse.get_lines()[0].get_ydata())
    assert len(dati_una) == len(mediane_una)
    for osservato, atteso in zip(dati_una, mediane_una):
        assert abs(osservato - atteso) < 1e-12


# --- L12: caso progettato dallo studente -----------------------------------


def test_l12_caso_dello_studente():
    """Caso progettato e motivato dallo studente: da completare.

    TODO dello studente:
    1. scegliere un caso nuovo su confini, campioni, timer o etichette;
    2. scrivere l'atteso **prima** di eseguire, motivandolo;
    3. dichiarare quale errore o conclusione impropria il caso deve
       distinguere;
    4. sostituire questo corpo con le asserzioni del caso.

    Il segnaposto qui sotto non è un test valido.
    """
    raise AssertionError("PY-U9-L12: caso proprio non ancora progettato")


# --- controlli di servizio --------------------------------------------------


def test_schema_della_tabella():
    """Lo schema della tabella copre tutti i campi del protocollo."""
    assert misure.COLONNE_TABELLA == (
        "esperimento",
        "algoritmo",
        "dimensione",
        "significato_dimensione",
        "famiglia_input",
        "stato_memoria",
        "ripetizione",
        "chiamate_per_lotto",
        "durata_lotto_s",
        "durata_per_chiamata_s",
    )


def test_misura_scansione_due_letture_del_timer():
    """La regione cronometrata si apre e si chiude con due sole letture."""
    sorgente = inspect.getsource(misure.misura_scansione)
    assert sorgente.count("perf_counter") == 2


def test_grafico_senza_finestra_e_senza_timer():
    """Il grafico non apre finestre e non contiene alcuna misura di tempo."""
    sorgente = inspect.getsource(grafici.grafico_scansioni)
    assert "plt.show" not in sorgente
    assert "perf_counter" not in sorgente
    assert "savefig" in sorgente


def test_misure_senza_file():
    """I dati vivono in liste e dizionari: nessun file, nessun modulo di file."""
    sorgente_misure = inspect.getsource(misure)
    assert "open(" not in sorgente_misure
    assert "import csv" not in sorgente_misure
    assert "import json" not in sorgente_misure
    assert "from pathlib" not in sorgente_misure
    assert "import pathlib" not in sorgente_misure
    sorgente_grafici = inspect.getsource(grafici)
    assert "from pathlib" not in sorgente_grafici
    assert "import pathlib" not in sorgente_grafici


def test_directory_mancante_messaggio_chiaro(tmp_path):
    """Directory assente: nessuna eccezione e messaggio chiaro disponibile."""
    percorso = os.path.join(str(tmp_path), "cartella_assente", "prova.png")
    assert grafici.grafico_scansioni([2, 4], [2, 4], [4, 8], percorso) is None
    messaggio = grafici.messaggio_directory_mancante(percorso)
    assert "cartella_assente" in messaggio
    assert "crearla" in messaggio


def test_conta_coppie_esegue_i_cicli_del_modello():
    """Il contratto nomina i due cicli del modello: il corpo va eseguito.

    La formula chiusa restituisce gli stessi numeri ma non esegue il corpo
    del ciclo: questo caso la distingue dal procedimento richiesto.
    """
    sorgente = inspect.getsource(conta_coppie)
    sorgente = sorgente.replace(" ", "").replace("\n", "").replace("\t", "")
    assert "foriinrange(n)" in sorgente
    assert "forjinrange(i+1,n)" in sorgente


def test_nessuna_lettura_nessuna_stampa_nelle_funzioni_verificate():
    """Le funzioni di analisi, misura e disegno non leggono né stampano."""
    funzioni = [
        riepilogo_due_scansioni,
        riepilogo_una_scansione,
        conta_coppie,
        misure.misura_scansione,
        grafici.grafico_scansioni,
        fibonacci_diretto,
        fibonacci_iter,
        fibonacci_mem,
        fibonacci_mem_osservata,
        fibonacci_diretto_osservato,
        memoria_delle_basi,
    ]
    for funzione in funzioni:
        sorgente = inspect.getsource(funzione)
        assert "input(" not in sorgente
        assert "print(" not in sorgente


def test_le_tre_varianti_di_fibonacci_concordano():
    """Le tre varianti restituiscono gli stessi valori da 0 a 10."""
    for n in range(11):
        assert fibonacci_diretto(n) == fibonacci_iter(n) == fibonacci_mem(n, memoria_delle_basi())


def test_funzioni_disponibili():
    assert callable(riepilogo_due_scansioni)
    assert callable(riepilogo_una_scansione)
    assert callable(conta_coppie)
    assert callable(misure.misura_scansione)
    assert callable(misure.sintetizza_campioni)
    assert callable(grafici.grafico_scansioni)
    assert callable(grafici.tabella_equivalente)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
