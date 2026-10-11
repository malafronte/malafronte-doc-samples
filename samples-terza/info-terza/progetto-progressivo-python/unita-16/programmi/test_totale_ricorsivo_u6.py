"""Suite di verifica del totale ricorsivo (tappa U6).

Casi pubblici PR01-PR07, casi discriminanti su ultimo elemento e duplicati,
e raccordo con il riepilogo U5 con la conversione euro -> centesimi eseguita
una sola volta.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_totale_ricorsivo_u6.py
"""
from spedizione_u5 import (
    anteprima_preventivo,
    registra_preventivo,
    riepilogo_preventivi,
    totale_preventivi_ric,
)


# --- Casi pubblici PR01-PR07 ---


def test_pr01_lista_vuota_e_quanti_zero():
    assert totale_preventivi_ric([], 0) == 0


def test_pr02_quanti_zero_su_lista_non_vuota():
    importi_cent = [250]
    assert totale_preventivi_ric(importi_cent, 0) == 0
    assert importi_cent == [250]


def test_pr03_un_solo_elemento():
    importi_cent = [250]
    assert totale_preventivi_ric(importi_cent, 1) == 250
    assert importi_cent == [250]


def test_pr04_prefisso_che_esclude_l_ultimo():
    importi_cent = [250, 0, 750]
    assert totale_preventivi_ric(importi_cent, 2) == 250
    assert importi_cent == [250, 0, 750]


def test_pr05_lista_intera_con_elemento_nullo_in_mezzo():
    importi_cent = [250, 0, 750]
    assert totale_preventivi_ric(importi_cent, 3) == 1000
    assert importi_cent == [250, 0, 750]


def test_pr06_duplicati_contati_entrambi():
    importi_cent = [125, 125, 0]
    assert totale_preventivi_ric(importi_cent, 3) == 250
    assert importi_cent == [125, 125, 0]


def test_pr07_due_chiamate_sulla_stessa_lista():
    importi_cent = [100, 200, 300, 400]
    prima = totale_preventivi_ric(importi_cent, 4)
    seconda = totale_preventivi_ric(importi_cent, 4)
    assert prima == 1000
    assert seconda == prima
    assert importi_cent == [100, 200, 300, 400]


# --- Casi discriminanti ---


def test_discriminante_ultimo_elemento_escluso_e_incluso():
    """Il confine fra quanti = n-1 e quanti = n decide sull'ultimo importo."""
    importi_cent = [10, 20, 30]
    assert totale_preventivi_ric(importi_cent, 2) == 30
    assert totale_preventivi_ric(importi_cent, 3) == 60


def test_discriminante_duplicati_e_zero_finale():
    """Due importi uguali sono due elementi distinti; lo zero finale conta."""
    importi_cent = [7, 7, 0]
    assert totale_preventivi_ric(importi_cent, 3) == 14
    assert totale_preventivi_ric(importi_cent, 2) == 14
    assert totale_preventivi_ric(importi_cent, 1) == 7


def test_discriminante_importo_zero_in_testa():
    """Uno zero in testa non produce la somma degli elementi successivi."""
    importi_cent = [0, 400, 900]
    assert totale_preventivi_ric(importi_cent, 1) == 0
    assert totale_preventivi_ric(importi_cent, 2) == 400


# --- Raccordo con il riepilogo U5 (M26-M27) ---


def test_raccordo_u5_u6_conversione_unica():
    """Il riepilogo U5 lavora in euro, la lista U6 in centesimi.

    La conversione euro -> centesimi avviene una sola volta, quando la lista
    in centesimi viene costruita; la somma U6 confrontata col riepilogo U5 è
    somma_euro * 100.
    """
    preventivi_euro = []
    registra_preventivo(preventivi_euro, 3)
    registra_preventivo(preventivi_euro, 9)
    registra_preventivo(preventivi_euro, 5)
    numero, somma_euro = riepilogo_preventivi(preventivi_euro)

    importi_cent = []
    for importo_euro in preventivi_euro:
        importi_cent.append(importo_euro * 100)

    assert numero == 3
    assert somma_euro == 17
    assert importi_cent == [300, 900, 500]
    assert totale_preventivi_ric(importi_cent, len(importi_cent)) == somma_euro * 100
    assert preventivi_euro == [3, 9, 5]


def test_raccordo_anteprima_non_contamina_la_lista_di_lavoro():
    """L'anteprima U5 non entra nel confronto U6: resta una lista a parte."""
    preventivi_euro = [3, 9, 5]
    provvisoria = anteprima_preventivo(preventivi_euro, 7)
    assert provvisoria == [3, 9, 5, 7]
    assert preventivi_euro == [3, 9, 5]
    importi_cent = []
    for importo_euro in preventivi_euro:
        importi_cent.append(importo_euro * 100)
    assert totale_preventivi_ric(importi_cent, 3) == 1700
