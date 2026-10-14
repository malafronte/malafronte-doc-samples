"""Prove sui frattali geometrici di PY-37: livelli 0/1/2, conteggi e budget (L2)."""

import math

import pytest

from dati_canonici import (
    CONTEGGI_SEGMENTI_KOCH_CURVA,
    CONTEGGI_SEGMENTI_KOCH_FIOCCO,
    CONTEGGI_TRIANGOLI_SIERPINSKI,
    LATI_INIZIALI_FIOCCO_ORARIO,
    SEGMENTI_KOCH_LIVELLO_1,
    SEGMENTO_KOCH_BASE,
    TOLLERANZA_GEOMETRIA,
    TRIANGOLI_SIERPINSKI_LIVELLO_1,
    TRIANGOLO_CENTRALE_ESCLUSO_LIVELLO_1,
    TRIANGOLO_SIERPINSKI_BASE,
    VERTICI_FIOCCO_ORARIO,
    VERTICI_KOCH_LIVELLO_1,
)
from geometria_esempi import (
    curva_koch,
    fiocco_koch,
    livello_massimo_koch_curva,
    livello_massimo_koch_fiocco,
    livello_massimo_sierpinski,
    punto_medio,
    ruota_vettore_60_gradi,
    suddividi_segmento_koch,
    triangoli_sierpinski,
    vertici_sostituzione_koch,
    vettore_fra_punti,
)


def _quasi_uguale(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1]) < TOLLERANZA_GEOMETRIA


def test_punti_medi_vettori_e_rotazione_60_gradi():
    assert punto_medio((0.0, 0.0), (4.0, 0.0)) == (2.0, 0.0)
    assert punto_medio((0.0, 0.0), (4.0, 0.0)) != (2.0, 1.0)
    assert vettore_fra_punti((1.0, 2.0), (4.0, 6.0)) == (3.0, 4.0)
    ruotato = ruota_vettore_60_gradi((1.0, 0.0))
    assert math.isclose(ruotato[0], 0.5, abs_tol=TOLLERANZA_GEOMETRIA)
    assert math.isclose(ruotato[1], math.sqrt(3.0) / 2.0, abs_tol=TOLLERANZA_GEOMETRIA)


def test_curva_koch_livelli_0_1_2_e_conteggi():
    livello_0 = curva_koch(SEGMENTO_KOCH_BASE, 0)
    assert livello_0 == [SEGMENTO_KOCH_BASE]

    vertici = vertici_sostituzione_koch(SEGMENTO_KOCH_BASE)
    assert len(vertici) == 5
    for ottenuto, atteso in zip(vertici, VERTICI_KOCH_LIVELLO_1, strict=True):
        assert _quasi_uguale(ottenuto, atteso)

    livello_1 = curva_koch(SEGMENTO_KOCH_BASE, 1)
    assert len(livello_1) == 4
    for ottenuto, atteso in zip(livello_1, SEGMENTI_KOCH_LIVELLO_1, strict=True):
        assert _quasi_uguale(ottenuto[0], atteso[0])
        assert _quasi_uguale(ottenuto[1], atteso[1])

    # Continuità: ogni segmento inizia dove finisce il precedente.
    for primo, secondo in zip(livello_1, livello_1[1:], strict=False):
        assert _quasi_uguale(primo[1], secondo[0])

    livello_2 = curva_koch(SEGMENTO_KOCH_BASE, 2)
    assert len(livello_2) == 16
    assert livello_2[0][0] == SEGMENTO_KOCH_BASE[0]
    assert livello_2[-1][1] == SEGMENTO_KOCH_BASE[1]
    for primo, secondo in zip(livello_2, livello_2[1:], strict=False):
        assert _quasi_uguale(primo[1], secondo[0])

    for livello, atteso in CONTEGGI_SEGMENTI_KOCH_CURVA.items():
        assert len(curva_koch(SEGMENTO_KOCH_BASE, livello)) == atteso


def test_fiocco_koch_chiusura_continuita_orientamento_e_conteggi():
    livello_0 = fiocco_koch(VERTICI_FIOCCO_ORARIO, 0)
    assert len(livello_0) == 3
    assert tuple(livello_0) == LATI_INIZIALI_FIOCCO_ORARIO

    livello_1 = fiocco_koch(VERTICI_FIOCCO_ORARIO, 1)
    assert len(livello_1) == 12
    # Spezzata chiusa e continua: ultimo punto = primo punto.
    assert _quasi_uguale(livello_1[-1][1], livello_1[0][0])
    for primo, secondo in zip(livello_1, livello_1[1:], strict=False):
        assert _quasi_uguale(primo[1], secondo[0])

    # Le tre punte del livello 1 sono esterne: distano sqrt(3) dal baricentro.
    baricentro = (1.5, math.sqrt(3.0) / 2.0)
    punte = [livello_1[1][1], livello_1[5][1], livello_1[9][1]]
    for punta in punte:
        distanza = math.hypot(punta[0] - baricentro[0], punta[1] - baricentro[1])
        assert distanza > math.sqrt(3.0) / 2.0
        assert math.isclose(distanza, math.sqrt(3.0), abs_tol=TOLLERANZA_GEOMETRIA)

    livello_2 = fiocco_koch(VERTICI_FIOCCO_ORARIO, 2)
    assert len(livello_2) == 48
    assert _quasi_uguale(livello_2[-1][1], livello_2[0][0])

    for livello, atteso in CONTEGGI_SEGMENTI_KOCH_FIOCCO.items():
        assert len(fiocco_koch(VERTICI_FIOCCO_ORARIO, livello)) == atteso


def test_sierpinski_punti_medi_triangolo_centrale_escluso_e_conteggi():
    livello_0 = triangoli_sierpinski(TRIANGOLO_SIERPINSKI_BASE, 0)
    assert livello_0 == [TRIANGOLO_SIERPINSKI_BASE]

    livello_1 = triangoli_sierpinski(TRIANGOLO_SIERPINSKI_BASE, 1)
    assert len(livello_1) == 3
    for ottenuto, atteso in zip(livello_1, TRIANGOLI_SIERPINSKI_LIVELLO_1, strict=True):
        for p_ottenuto, p_atteso in zip(ottenuto, atteso, strict=True):
            assert _quasi_uguale(p_ottenuto, p_atteso)

    # Il triangolo centrale individuato dai punti medi resta escluso.
    for triangolo in livello_1:
        assert triangolo != TRIANGOLO_CENTRALE_ESCLUSO_LIVELLO_1

    # Ogni triangolo del livello 1 ha lato dimezzato (2.0 contro 4.0).
    for triangolo in livello_1:
        lato = math.hypot(triangolo[1][0] - triangolo[0][0], triangolo[1][1] - triangolo[0][1])
        assert math.isclose(lato, 2.0, abs_tol=TOLLERANZA_GEOMETRIA)

    livello_2 = triangoli_sierpinski(TRIANGOLO_SIERPINSKI_BASE, 2)
    assert len(livello_2) == 9

    for livello, atteso in CONTEGGI_TRIANGOLI_SIERPINSKI.items():
        assert len(triangoli_sierpinski(TRIANGOLO_SIERPINSKI_BASE, livello)) == atteso


def test_scelta_del_massimo_livello_entro_il_budget():
    # Curva: 4**d <= budget (uguaglianza accettata).
    assert livello_massimo_koch_curva(1) == 0
    assert livello_massimo_koch_curva(4) == 1
    assert livello_massimo_koch_curva(15) == 1
    assert livello_massimo_koch_curva(16) == 2
    assert livello_massimo_koch_curva(192) == 3  # 4**3 = 64, 4**4 = 256 > 192
    assert livello_massimo_koch_curva(64) == 3
    # Fiocco: 3 * 4**d <= budget.
    assert livello_massimo_koch_fiocco(3) == 0
    assert livello_massimo_koch_fiocco(12) == 1
    assert livello_massimo_koch_fiocco(192) == 3
    with pytest.raises(ValueError):
        livello_massimo_koch_fiocco(2)
    # Sierpinski: 3**d <= budget.
    assert livello_massimo_sierpinski(1) == 0
    assert livello_massimo_sierpinski(3) == 1
    assert livello_massimo_sierpinski(81) == 4
    assert livello_massimo_sierpinski(80) == 3


def test_errori_di_dominio_e_accumulatore_indipendente():
    with pytest.raises(TypeError):
        curva_koch(SEGMENTO_KOCH_BASE, True)
    with pytest.raises(ValueError):
        curva_koch(SEGMENTO_KOCH_BASE, -1)
    with pytest.raises(ValueError):
        fiocco_koch(((0.0, 0.0), (1.0, 1.0), (2.0, 2.0)), 1)
    with pytest.raises(ValueError):
        triangoli_sierpinski(TRIANGOLO_SIERPINSKI_BASE, 1, stile="tratteggio")
    with pytest.raises(ValueError):
        livello_massimo_koch_curva(0)
    # Due invocazioni pubbliche non condividono l'accumulatore.
    prima = curva_koch(SEGMENTO_KOCH_BASE, 1)
    seconda = curva_koch(SEGMENTO_KOCH_BASE, 1)
    assert prima == seconda
    assert prima is not seconda
    suddivisi = suddividi_segmento_koch(SEGMENTO_KOCH_BASE)
    assert len(suddivisi) == 4
