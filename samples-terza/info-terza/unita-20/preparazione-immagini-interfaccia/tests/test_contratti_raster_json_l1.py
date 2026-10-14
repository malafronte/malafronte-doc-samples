"""Verifica dei contratti canonici di campionamento, palette e schema JSON (L1).

Questa suite verifica in modo indipendente e senza aprire finestre grafiche le fixture e
gli oracoli di `contratti_raster_json.py`. I moduli applicativi di PY-40 (`coordinate_esempi.py`,
`palette_esempi.py`, `griglia_pillow.py`), PY-41 (`finestra_griglia.py`) e PY-42
(`configurazione_esempio.py`) verranno introdotti e testati nei lotti L5, L6 e L7.
"""

import copy
import math

import pytest

from contratti_raster_json import (
    CONFIGURAZIONI_JSON_CANONICHE,
    FAMIGLIE_FRATTALI_AMMESSE,
    GRIGLIA_CANONICA_1X1,
    GRIGLIA_CANONICA_4X2,
    PALETTE_AMMESSE,
    TOLLERANZA_COORDINATE,
    VISTA_CANONICA_1X1,
    VISTA_CANONICA_4X2,
    campiona_centro_pixel_riferimento,
    colora_esito_riferimento,
    costruisci_griglia_campioni_riferimento,
    deserializza_configurazione_json_riferimento,
    serializza_configurazione_json_riferimento,
    trasforma_punti_geometrici_in_pixel_riferimento,
    valida_dizionario_configurazione_riferimento,
)


def test_griglia_canonica_4x2_e_inversione_asse_verticale() -> None:
    assert math.isclose(VISTA_CANONICA_4X2.ampiezza_verticale, 2.0, abs_tol=TOLLERANZA_COORDINATE)
    griglia = costruisci_griglia_campioni_riferimento(VISTA_CANONICA_4X2)
    assert len(griglia) == 2
    assert len(griglia[0]) == 4

    for q in range(2):
        for p in range(4):
            assert abs(griglia[q][p] - GRIGLIA_CANONICA_4X2[q][p]) < TOLLERANZA_COORDINATE

    # Riga superiore q=0 ha y=+0.5 > riga inferiore q=1 con y=-0.5
    assert griglia[0][0].imag > griglia[1][0].imag
    # Passo orizzontale e verticale sono entrambi uguali a s_x / W = 1.0 (scala uniforme)
    passo_x = griglia[0][1].real - griglia[0][0].real
    passo_y = griglia[0][0].imag - griglia[1][0].imag
    assert math.isclose(passo_x, 1.0, abs_tol=TOLLERANZA_COORDINATE)
    assert math.isclose(passo_y, 1.0, abs_tol=TOLLERANZA_COORDINATE)


def test_griglia_canonica_1x1_campiona_esattamente_il_centro() -> None:
    griglia = costruisci_griglia_campioni_riferimento(VISTA_CANONICA_1X1)
    assert griglia == GRIGLIA_CANONICA_1X1
    punto = campiona_centro_pixel_riferimento(0, 0, 1, 1, -0.5, 0.25, 3.5)
    assert abs(punto - (-0.5 + 0.25j)) < TOLLERANZA_COORDINATE


def test_adattamento_geometrico_conserva_proporzioni_in_finestre_diverse() -> None:
    triangolo_equilatero = (
        (0.0, 0.0),
        (3.0, 0.0),
        (1.5, 1.5 * math.sqrt(3.0)),
    )
    for larghezza, altezza in ((320, 240), (800, 600), (240, 480)):
        punti_px = trasforma_punti_geometrici_in_pixel_riferimento(
            triangolo_equilatero,
            larghezza=larghezza,
            altezza=altezza,
        )
        lato_01 = math.hypot(punti_px[1][0] - punti_px[0][0], punti_px[1][1] - punti_px[0][1])
        lato_12 = math.hypot(punti_px[2][0] - punti_px[1][0], punti_px[2][1] - punti_px[1][1])
        lato_20 = math.hypot(punti_px[0][0] - punti_px[2][0], punti_px[0][1] - punti_px[2][1])
        assert math.isclose(lato_01, lato_12, rel_tol=1e-9)
        assert math.isclose(lato_12, lato_20, rel_tol=1e-9)
        # Il vertice superiore (y maggiore) ha coordinata q minore nel raster
        assert punti_px[2][1] < punti_px[0][1]


@pytest.mark.parametrize("nome_palette", PALETTE_AMMESSE)
def test_palette_deterministiche_distinguono_none_e_indice_zero(nome_palette: str) -> None:
    colore_none = colora_esito_riferimento(None, 100, nome_palette)
    colore_zero = colora_esito_riferimento(0, 100, nome_palette)
    colore_finale = colora_esito_riferimento(100, 100, nome_palette)

    for colore in (colore_none, colore_zero, colore_finale):
        assert len(colore) == 3
        assert all(isinstance(c, int) and 0 <= c <= 255 for c in colore)

    assert colore_zero != colore_none
    assert colore_finale != colore_none
    # Ripetibilità deterministica
    assert colora_esito_riferimento(0, 100, nome_palette) == colore_zero


@pytest.mark.parametrize("famiglia", FAMIGLIE_FRATTALI_AMMESSE)
def test_round_trip_json_delle_quattro_famiglie(famiglia: str) -> None:
    configurazione = copy.deepcopy(CONFIGURAZIONI_JSON_CANONICHE[famiglia])
    testo = serializza_configurazione_json_riferimento(configurazione)
    ricostruita = deserializza_configurazione_json_riferimento(testo)
    assert ricostruita == configurazione


def test_julia_ammette_parametro_diagnostico_c_meno_6() -> None:
    config = copy.deepcopy(CONFIGURAZIONI_JSON_CANONICHE["julia"])
    config["parametri"]["c"] = {"reale": -6.0, "immaginaria": 0.0}
    testo = serializza_configurazione_json_riferimento(config)
    ricostruita = deserializza_configurazione_json_riferimento(testo)
    assert ricostruita["parametri"]["c"]["reale"] == -6.0


def test_validazione_json_rifiuta_booleani_nan_inf_e_budget_eccessivo() -> None:
    # 1. Booleano al posto di intero (isinstance(True, int) == True in Python)
    config_bool = copy.deepcopy(CONFIGURAZIONI_JSON_CANONICHE["mandelbrot"])
    config_bool["parametri"]["limite_iterazioni"] = True
    with pytest.raises(TypeError):
        valida_dizionario_configurazione_riferimento(config_bool)

    # 2. Valore non finito (NaN / Inf) in memoria e nel testo JSON
    config_nan = copy.deepcopy(CONFIGURAZIONI_JSON_CANONICHE["julia"])
    config_nan["parametri"]["c"]["reale"] = float("nan")
    with pytest.raises(ValueError):
        serializza_configurazione_json_riferimento(config_nan)

    testo_con_nan = (
        '{"versione_schema": 1, "tipo_frattale": "mandelbrot", '
        '"vista": {"ampiezza_orizzontale": NaN}}'
    )
    with pytest.raises(ValueError):
        deserializza_configurazione_json_riferimento(testo_con_nan)

    # 3. Superamento del budget combinato W * H * N > 100_000_000
    # (800 x 600 e N=500 sono singolarmente nei massimi, ma 800*600*500 = 240_000_000 > 100_000_000)
    config_budget = copy.deepcopy(CONFIGURAZIONI_JSON_CANONICHE["mandelbrot"])
    config_budget["immagine"]["larghezza"] = 800
    config_budget["immagine"]["altezza"] = 600
    config_budget["parametri"]["limite_iterazioni"] = 500
    with pytest.raises(ValueError, match="budget stimato"):
        valida_dizionario_configurazione_riferimento(config_budget)

    # 4. Versione schema non supportata
    config_versione = copy.deepcopy(CONFIGURAZIONI_JSON_CANONICHE["koch"])
    config_versione["versione_schema"] = 2
    with pytest.raises(ValueError, match="Versione schema"):
        valida_dizionario_configurazione_riferimento(config_versione)
