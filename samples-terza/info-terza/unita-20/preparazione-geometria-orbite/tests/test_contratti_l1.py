"""Verifica dei contratti e degli oracoli canonici di geometria, complessi e fuga (L1).

Questa suite verifica in modo autonomo le fixture e gli oracoli indipendenti definiti
in `dati_canonici.py`. I test dei moduli applicativi dei capitoli successivi
(`geometria_esempi.py` in L2, `complessi_esempi.py` e `orbite_esempi.py` in L3,
`fuga_esempi.py` in L4) verranno aggiunti nei rispettivi lotti usando questi stessi
dati canonici.
"""

import math

import pytest

from dati_canonici import (
    APOTEMA_FIOCCO_BASE,
    BARICENTRO_FIOCCO_BASE,
    CASI_FUGA_CANONICI,
    CASI_FUGA_PER_CODICE,
    CASI_OPERAZIONI_COMPLESSE,
    CONTEGGI_SEGMENTI_KOCH_CURVA,
    CONTEGGI_SEGMENTI_KOCH_FIOCCO,
    CONTEGGI_TRIANGOLI_SIERPINSKI,
    LATI_INIZIALI_FIOCCO_ORARIO,
    LATO_KOCH_CANONICO,
    LATO_SIERPINSKI_CANONICO,
    PUNTE_ESTERNE_FIOCCO_LIVELLO_1,
    RAGGIO_CIRCOSCRITTO_FIOCCO_BASE,
    RAGGIO_FUGA_MANDELBROT,
    SEGMENTI_KOCH_LIVELLO_1,
    SEGMENTO_KOCH_BASE,
    TOLLERANZA_COMPLESSI,
    TOLLERANZA_GEOMETRIA,
    TRACCE_ORBITE_CANONICHE,
    TRIANGOLI_SIERPINSKI_LIVELLO_1,
    TRIANGOLO_CENTRALE_ESCLUSO_LIVELLO_1,
    TRIANGOLO_SIERPINSKI_BASE,
    VERTICI_KOCH_LIVELLO_1,
    area_totale_sierpinski,
    lato_triangolo_sierpinski,
    lunghezza_segmento_koch,
    lunghezza_totale_koch_curva,
    numero_segmenti_koch_curva,
    numero_segmenti_koch_fiocco,
    numero_triangoli_sierpinski,
    oracolo_fuga_componenti_reali,
    raggio_fuga_julia,
    suddividi_segmento_koch_riferimento,
)


def _distanza(p_1: tuple[float, float], p_2: tuple[float, float]) -> float:
    return math.hypot(p_2[0] - p_1[0], p_2[1] - p_1[1])


def test_vertici_e_segmenti_koch_livello_1() -> None:
    segmenti = suddividi_segmento_koch_riferimento(SEGMENTO_KOCH_BASE)
    assert len(segmenti) == 4
    for ottenuto, atteso in zip(segmenti, SEGMENTI_KOCH_LIVELLO_1, strict=True):
        assert _distanza(ottenuto[0], atteso[0]) < TOLLERANZA_GEOMETRIA
        assert _distanza(ottenuto[1], atteso[1]) < TOLLERANZA_GEOMETRIA
        assert math.isclose(_distanza(ottenuto[0], ottenuto[1]), 1.0, abs_tol=TOLLERANZA_GEOMETRIA)

    # Verifica continuità della spezzata e triangolo equilatero centrale (lato 1.0).
    for indice in range(len(segmenti) - 1):
        assert _distanza(segmenti[indice][1], segmenti[indice + 1][0]) < TOLLERANZA_GEOMETRIA
    assert math.isclose(
        _distanza(VERTICI_KOCH_LIVELLO_1[1], VERTICI_KOCH_LIVELLO_1[3]),
        1.0,
        abs_tol=TOLLERANZA_GEOMETRIA,
    )


def test_orientamento_orario_fiocco_produce_punte_esterne() -> None:
    punte_ottenute = []
    for lato in LATI_INIZIALI_FIOCCO_ORARIO:
        sottosegmenti = suddividi_segmento_koch_riferimento(lato)
        punta = sottosegmenti[1][1]
        punte_ottenute.append(punta)
        distanza_dal_baricentro = _distanza(punta, BARICENTRO_FIOCCO_BASE)
        assert distanza_dal_baricentro > APOTEMA_FIOCCO_BASE
        assert math.isclose(
            distanza_dal_baricentro,
            RAGGIO_CIRCOSCRITTO_FIOCCO_BASE,
            abs_tol=TOLLERANZA_GEOMETRIA,
        )

    for ottenuta, attesa in zip(punte_ottenute, PUNTE_ESTERNE_FIOCCO_LIVELLO_1, strict=True):
        assert _distanza(ottenuta, attesa) < TOLLERANZA_GEOMETRIA

    # Controverifica didattica: invertendo il lato di base da (0, 0) -> (3, 0),
    # la punta cadrebbe esattamente sul baricentro interno del triangolo.
    sottosegmenti_antiorari = suddividi_segmento_koch_riferimento(((0.0, 0.0), (3.0, 0.0)))
    punta_interna = sottosegmenti_antiorari[1][1]
    assert _distanza(punta_interna, BARICENTRO_FIOCCO_BASE) < TOLLERANZA_GEOMETRIA


def test_conteggi_e_misure_koch_e_sierpinski() -> None:
    for livello, atteso in CONTEGGI_SEGMENTI_KOCH_CURVA.items():
        assert numero_segmenti_koch_curva(livello) == atteso
        assert numero_segmenti_koch_fiocco(livello) == CONTEGGI_SEGMENTI_KOCH_FIOCCO[livello]
        lunghezza_singola = lunghezza_segmento_koch(LATO_KOCH_CANONICO, livello)
        lunghezza_totale = lunghezza_totale_koch_curva(LATO_KOCH_CANONICO, livello)
        assert math.isclose(
            lunghezza_singola * atteso,
            lunghezza_totale,
            rel_tol=TOLLERANZA_GEOMETRIA,
        )

    area_base = (math.sqrt(3.0) / 4.0) * (LATO_SIERPINSKI_CANONICO**2)
    for livello, atteso in CONTEGGI_TRIANGOLI_SIERPINSKI.items():
        assert numero_triangoli_sierpinski(livello) == atteso
        lato_livello = lato_triangolo_sierpinski(LATO_SIERPINSKI_CANONICO, livello)
        area_singola = (math.sqrt(3.0) / 4.0) * (lato_livello**2)
        assert math.isclose(
            area_singola * atteso,
            area_totale_sierpinski(area_base, livello),
            rel_tol=TOLLERANZA_GEOMETRIA,
        )

    assert len(TRIANGOLI_SIERPINSKI_LIVELLO_1) == 3
    assert TRIANGOLO_CENTRALE_ESCLUSO_LIVELLO_1 not in TRIANGOLI_SIERPINSKI_LIVELLO_1
    assert TRIANGOLO_SIERPINSKI_BASE[0] == TRIANGOLI_SIERPINSKI_LIVELLO_1[0][0]


def test_operazioni_complesse_e_tracce_orbite_canonicizzate() -> None:
    for caso in CASI_OPERAZIONI_COMPLESSE:
        atteso_c = complex(caso.risultato_atteso)
        if caso.nome.startswith("modulo"):
            assert math.isclose(
                abs(caso.z_1), float(caso.risultato_atteso), abs_tol=TOLLERANZA_COMPLESSI
            )
        elif caso.nome.startswith("somma"):
            assert caso.z_2 is not None
            assert abs((caso.z_1 + caso.z_2) - atteso_c) < TOLLERANZA_COMPLESSI
        elif caso.nome.startswith("sottrazione"):
            assert caso.z_2 is not None
            assert abs((caso.z_1 - caso.z_2) - atteso_c) < TOLLERANZA_COMPLESSI
        elif caso.nome.startswith("prodotto"):
            assert caso.z_2 is not None
            assert abs((caso.z_1 * caso.z_2) - atteso_c) < TOLLERANZA_COMPLESSI
        elif caso.nome.startswith("quadrato"):
            assert abs((caso.z_1**2) - atteso_c) < TOLLERANZA_COMPLESSI

    parametri_tracce = {
        "c_zero_da_zero": 0.0j,
        "c_meno_uno_da_zero": -1.0 + 0.0j,
        "c_uno_da_zero": 1.0 + 0.0j,
        "c_i_da_zero": 1.0j,
    }
    for nome_traccia, c in parametri_tracce.items():
        attesa = TRACCE_ORBITE_CANONICHE[nome_traccia]
        z = 0.0j
        prodotta = [z]
        for _ in range(len(attesa) - 1):
            z = z * z + c
            prodotta.append(z)
        assert tuple(prodotta) == attesa


@pytest.mark.parametrize("caso", CASI_FUGA_CANONICI, ids=[c.codice for c in CASI_FUGA_CANONICI])
def test_dodici_casi_canonici_mandelbrot_e_julia(caso) -> None:
    esito = oracolo_fuga_componenti_reali(
        x_iniziale=caso.z_iniziale.real,
        y_iniziale=caso.z_iniziale.imag,
        c_reale=caso.c.real,
        c_immaginaria=caso.c.imag,
        limite_iterazioni=caso.limite_iterazioni,
        raggio_fuga=caso.raggio_fuga,
    )
    assert esito.indice_fuga == caso.indice_fuga_atteso
    assert esito.aggiornamenti_eseguiti == caso.aggiornamenti_attesi
    assert abs(esito.valore_finale - caso.valore_finale_atteso) < TOLLERANZA_COMPLESSI

    if caso.famiglia == "mandelbrot":
        assert caso.z_iniziale == 0.0j
        assert caso.raggio_fuga == RAGGIO_FUGA_MANDELBROT
    else:
        assert caso.raggio_fuga == raggio_fuga_julia(caso.c)


def test_distinzione_fuga_passo_zero_passo_finale_e_budget_esaurito() -> None:
    # J-04: fuga già al passo 0 con zero aggiornamenti
    j04 = CASI_FUGA_PER_CODICE["J-04"]
    esito_j04 = oracolo_fuga_componenti_reali(
        j04.z_iniziale.real,
        j04.z_iniziale.imag,
        j04.c.real,
        j04.c.imag,
        j04.limite_iterazioni,
        j04.raggio_fuga,
    )
    assert esito_j04.indice_fuga == 0
    assert esito_j04.indice_fuga is not None
    assert esito_j04.aggiornamenti_eseguiti == 0

    # M-04 vs M-05: stesso punto c=1, ma budget N=2 (non fugge) vs N=3 (fugge sull'ultimo passo)
    m04 = CASI_FUGA_PER_CODICE["M-04"]
    m05 = CASI_FUGA_PER_CODICE["M-05"]
    esito_m04 = oracolo_fuga_componenti_reali(0.0, 0.0, 1.0, 0.0, m04.limite_iterazioni, 2.0)
    esito_m05 = oracolo_fuga_componenti_reali(0.0, 0.0, 1.0, 0.0, m05.limite_iterazioni, 2.0)
    assert esito_m04.indice_fuga is None
    assert esito_m04.aggiornamenti_eseguiti == 2
    assert esito_m05.indice_fuga == 3
    assert esito_m05.aggiornamenti_eseguiti == 3


def test_caso_discriminante_julia_c_meno_6_z0_3() -> None:
    j05 = CASI_FUGA_PER_CODICE["J-05"]
    raggio_corretto = raggio_fuga_julia(j05.c)
    assert raggio_corretto == 6.0

    esito_corretto = oracolo_fuga_componenti_reali(
        j05.z_iniziale.real,
        j05.z_iniziale.imag,
        j05.c.real,
        j05.c.imag,
        j05.limite_iterazioni,
        raggio_corretto,
    )
    assert esito_corretto.indice_fuga is None
    assert esito_corretto.valore_finale == 3.0 + 0.0j

    # Con il raggio fisso errato R=2.0 il punto fisso z_0=3 verrebbe espulso al passo 0.
    esito_raggio_errato = oracolo_fuga_componenti_reali(
        j05.z_iniziale.real,
        j05.z_iniziale.imag,
        j05.c.real,
        j05.c.imag,
        j05.limite_iterazioni,
        2.0,
    )
    assert esito_raggio_errato.indice_fuga == 0


def test_rifiuto_valori_booleani_e_non_finiti() -> None:
    with pytest.raises(TypeError):
        numero_segmenti_koch_curva(True)
    with pytest.raises(ValueError):
        numero_segmenti_koch_curva(-1)
    with pytest.raises(ValueError):
        raggio_fuga_julia(complex(float("nan"), 0.0))
    with pytest.raises(ValueError):
        oracolo_fuga_componenti_reali(0.0, 0.0, float("inf"), 0.0, 10, 2.0)
    with pytest.raises(TypeError):
        oracolo_fuga_componenti_reali(0.0, 0.0, 0.0, 0.0, True, 2.0)
