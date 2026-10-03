"""Suite di verifica dell'analisi del costo (tappa U9).

Casi pubblici PU9-01-PU9-08. I conteggi verificano il modello dichiarato nel
dossier: visite per il riepilogo, confronti fra codici per la consultazione.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_analisi_u9.py
"""
from analisi_costi_u9 import (
    cerca_preventivo_conteggi,
    genera_registro,
    mediana,
    riepilogo_per_destinazione_conteggi,
)
from spedizione_u5 import (
    cerca_preventivo,
    crea_registro,
)


def registro_canonico():
    """Dataset di riferimento U8-U9: codici 007, 008, 009."""
    codici = ["007", "008", "009"]
    preventivi = [("locale", 300), ("nazionale", 900), ("locale", 500)]
    return crea_registro(codici, preventivi)


# --- PU9-01 e PU9-02: riepilogo e costo fisso ---


def test_pu9_01_riepilogo_di_tre_record():
    registro = registro_canonico()
    riepilogo, visite, aggiornamenti = riepilogo_per_destinazione_conteggi(registro)
    assert riepilogo["locale"] == {"conteggio": 2, "totale_cent": 800}
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 900}
    assert visite == 3
    assert aggiornamenti == 6
    assert registro[0]["totale_cent"] == 300
    assert len(registro) == 3


def test_pu9_02_registro_vuoto_costo_fisso_separato():
    riepilogo, visite, aggiornamenti = riepilogo_per_destinazione_conteggi([])
    assert riepilogo == {
        "locale": {"conteggio": 0, "totale_cent": 0},
        "nazionale": {"conteggio": 0, "totale_cent": 0},
    }
    # Zero record visitati: la costruzione dei due gruppi è costo fisso
    # della chiamata e non compare nei contatori.
    assert visite == 0
    assert aggiornamenti == 0


# --- PU9-03 e PU9-04: consultazioni e lunghezza dei codici ---


def test_pu9_03_confronti_della_scansione_con_arresto():
    registro = registro_canonico()
    record, confronti = cerca_preventivo_conteggi(registro, "007")
    assert record == registro[0]
    assert confronti == 1

    record, confronti = cerca_preventivo_conteggi(registro, "009")
    assert record == registro[2]
    assert confronti == 3

    record, confronti = cerca_preventivo_conteggi(registro, "010")
    assert record is None
    assert confronti == 3


def test_pu9_04_codice_7_distinto_da_007():
    registro = registro_canonico()
    record, confronti = cerca_preventivo_conteggi(registro, "7")
    assert record is None
    assert confronti == 3
    assert cerca_preventivo(registro, "007") == registro[0]


# --- PU9-05: due input della stessa lunghezza ---


def test_pu9_05_stessa_lunghezza_posizioni_diverse():
    primo = genera_registro(3)
    secondo = genera_registro(3)
    assert len(primo) == len(secondo)

    record, confronti_prima = cerca_preventivo_conteggi(primo, "000000")
    assert record == primo[0]
    assert confronti_prima == 1

    record, confronti_ultima = cerca_preventivo_conteggi(secondo, "000002")
    assert record == secondo[2]
    assert confronti_ultima == 3


# --- PU9-06 e PU9-07: dimensioni crescenti e ripetizioni ---


def test_pu9_06_correttezza_prima_dei_tempi():
    for n in (10, 100, 1000):
        registro = genera_registro(n)
        riepilogo, visite, aggiornamenti = riepilogo_per_destinazione_conteggi(registro)
        totale_atteso = 0
        for record in registro:
            totale_atteso = totale_atteso + record["totale_cent"]
        totale_osservato = (
            riepilogo["locale"]["totale_cent"] + riepilogo["nazionale"]["totale_cent"]
        )
        assert len(registro) == n
        assert totale_osservato == totale_atteso
        assert visite == n
        assert aggiornamenti == 2 * n


def test_pu9_07_ripetizioni_su_stesso_dataset():
    registro = genera_registro(50)
    prima = riepilogo_per_destinazione_conteggi(registro)
    seconda = riepilogo_per_destinazione_conteggi(registro)
    assert prima == seconda
    assert len(registro) == 50
    assert registro[0]["codice"] == "000000"
    assert registro[49]["codice"] == "000049"


# --- PU9-08: il modello di costo, non i tempi, è ciò che è provato ---


def test_pu9_08_formule_del_modello_su_input_piccoli():
    """Le formule del modello valgono su ogni n: i tempi no.

    Visite = n, aggiornamenti = 2n, confronti = n per assente e ultima
    posizione, 1 per il primo record. Il dato 1/3/3 del caso PU9-03 è un caso
    particolare di queste formule.
    """
    for n in (1, 2, 5, 10):
        registro = genera_registro(n)
        riepilogo, visite, aggiornamenti = riepilogo_per_destinazione_conteggi(registro)
        assert visite == n
        assert aggiornamenti == 2 * n
        record, confronti = cerca_preventivo_conteggi(registro, registro[0]["codice"])
        assert confronti == 1
        record, confronti = cerca_preventivo_conteggi(registro, "999999")
        assert confronti == n


def test_mediana_descrive_i_campioni_senza_inventarli():
    """La mediana è un campione ordinato, non una previsione teorica."""
    assert mediana([0.3, 0.1, 0.2]) == 0.2
    assert mediana([0.4, 0.1, 0.2, 0.3]) == 0.25
    assert mediana([0.7]) == 0.7
