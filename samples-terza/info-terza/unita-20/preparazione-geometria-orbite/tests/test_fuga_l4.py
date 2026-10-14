"""Prove sul kernel di fuga di PY-39: contratto, 12 casi e wrappers (L4)."""

import math

import pytest

from dati_canonici import (
    CASI_FUGA_CANONICI,
    TOLLERANZA_COMPLESSI,
    oracolo_fuga_componenti_reali,
)
from fuga_esempi import (
    RAGGIO_FUGA_MANDELBROT,
    EsitoFuga,
    esito_fuga,
    esito_fuga_reali,
    esito_julia,
    esito_mandelbrot,
    fuga_rilevata,
    raggio_fuga_julia,
)


def _concorda_valore(ottenuto: complex, atteso: complex) -> bool:
    return abs(ottenuto - atteso) < TOLLERANZA_COMPLESSI


def test_dodici_casi_canonici_con_indice_aggiornamenti_e_valore():
    assert len(CASI_FUGA_CANONICI) == 12
    for caso in CASI_FUGA_CANONICI:
        esito = esito_fuga(caso.z_iniziale, caso.c, caso.limite_iterazioni, caso.raggio_fuga)
        assert esito.indice_fuga == caso.indice_fuga_atteso, caso.codice
        assert esito.aggiornamenti_eseguiti == caso.aggiornamenti_attesi, caso.codice
        assert _concorda_valore(esito.valore_finale, caso.valore_finale_atteso), caso.codice


def test_kernel_su_reali_e_oracolo_l1_concordano_con_complex():
    for caso in CASI_FUGA_CANONICI:
        gemello = esito_fuga_reali(
            caso.z_iniziale.real,
            caso.z_iniziale.imag,
            caso.c.real,
            caso.c.imag,
            caso.limite_iterazioni,
            caso.raggio_fuga,
        )
        riferimento = esito_fuga(caso.z_iniziale, caso.c, caso.limite_iterazioni, caso.raggio_fuga)
        assert gemello.indice_fuga == riferimento.indice_fuga, caso.codice
        assert gemello.aggiornamenti_eseguiti == riferimento.aggiornamenti_eseguiti
        assert _concorda_valore(gemello.valore_finale, riferimento.valore_finale)
        oracolo = oracolo_fuga_componenti_reali(
            caso.z_iniziale.real,
            caso.z_iniziale.imag,
            caso.c.real,
            caso.c.imag,
            caso.limite_iterazioni,
            caso.raggio_fuga,
        )
        assert oracolo.indice_fuga == riferimento.indice_fuga, caso.codice

    # Caso non esatto con entrambe le componenti non nulle: tolleranza motivata.
    complesso = esito_fuga(0.1 - 0.2j, -0.8 + 0.156j, 50, raggio_fuga_julia(-0.8 + 0.156j))
    reali = esito_fuga_reali(0.1, -0.2, -0.8, 0.156, 50, raggio_fuga_julia(-0.8 + 0.156j))
    assert complesso.indice_fuga == reali.indice_fuga
    assert _concorda_valore(complesso.valore_finale, reali.valore_finale)


def test_confronto_stretto_budget_e_indice_zero():
    # M-03: |z| = 2 sul confine non è fuga; il confronto usa > stretto, non >=.
    confine = esito_fuga(0.0j, -2.0 + 0.0j, 10, 2.0)
    assert confine.indice_fuga is None
    assert confine.valore_finale == 2.0 + 0.0j

    # M-04 contro M-05: stesso parametro, budget diverso (None contro fuga a N=3).
    assert esito_fuga(0.0j, 1.0 + 0.0j, 2, 2.0).indice_fuga is None
    ultimo_passo = esito_fuga(0.0j, 1.0 + 0.0j, 3, 2.0)
    assert ultimo_passo.indice_fuga == 3
    assert ultimo_passo.valore_finale == 5.0 + 0.0j

    # J-04: fuga già su z_0 con indice 0 e zero aggiornamenti.
    immediata = esito_fuga(3.0 + 0.0j, 0.0j, 10, 2.0)
    assert immediata.indice_fuga == 0
    assert immediata.aggiornamenti_eseguiti == 0
    assert immediata.valore_finale == 3.0 + 0.0j

    # J-03: al passo 0 vale |z_0| = 2 <= 2; la fuga arriva al passo 1.
    assert esito_fuga(2.0 + 0.0j, 0.0j, 10, 2.0).indice_fuga == 1


def test_raggio_julia_e_punto_fisso_con_c_meno_sei():
    assert RAGGIO_FUGA_MANDELBROT == 2.0
    assert raggio_fuga_julia(0.0j) == 2.0
    assert raggio_fuga_julia(-6.0 + 0.0j) == 6.0
    assert raggio_fuga_julia(-0.8 + 0.156j) == 2.0
    assert math.isclose(raggio_fuga_julia(3.0 + 4.0j), 5.0)

    # J-05: con R = 6 il punto z_0 = 3 resta fisso (3^2 - 6 = 3).
    preservato = esito_fuga(3.0 + 0.0j, -6.0 + 0.0j, 10, 6.0)
    assert preservato.indice_fuga is None
    assert preservato.valore_finale == 3.0 + 0.0j

    # Errore PY-U20-E04: con il raggio universale 2 lo stesso punto fugge al passo 0.
    errato = esito_fuga(3.0 + 0.0j, -6.0 + 0.0j, 10, 2.0)
    assert errato.indice_fuga == 0


def test_chiamate_mandelbrot_e_julia_con_dati_fissi_e_variabili():
    assert esito_mandelbrot(0.0j, 10) == esito_fuga(0.0j, 0.0j, 10, 2.0)
    assert esito_mandelbrot(1.0 + 0.0j, 3) == esito_fuga(0.0j, 1.0 + 0.0j, 3, 2.0)
    assert esito_julia(1.0j, 0.0j, 10) == esito_fuga(1.0j, 0.0j, 10, 2.0)
    assert esito_julia(3.0 + 0.0j, -6.0 + 0.0j, 10) == esito_fuga(3.0 + 0.0j, -6.0 + 0.0j, 10, 6.0)
    # Mandelbrot fissa il seme a zero; Julia fissa il parametro per l'immagine.
    assert esito_mandelbrot(-1.0 + 0.0j, 10).indice_fuga is None
    assert esito_julia(1.0 + 0.0j, 0.0j, 10).valore_finale == 1.0 + 0.0j


def test_fuga_rilevata_distigue_none_da_zero():
    assert fuga_rilevata(esito_fuga(0.0j, 1.0 + 0.0j, 3, 2.0)) is True
    assert fuga_rilevata(esito_fuga(3.0 + 0.0j, 0.0j, 10, 2.0)) is True
    assert fuga_rilevata(esito_fuga(0.0j, 1.0 + 0.0j, 2, 2.0)) is False
    # L'indice 0 è una fuga valida: il controllo usa `is None`, mai la falsità.
    assert esito_fuga(3.0 + 0.0j, 0.0j, 10, 2.0).indice_fuga == 0
    with pytest.raises(TypeError):
        fuga_rilevata("fuga")


def test_confronto_sul_modulo_quadro_conserva_il_criterio_stretto():
    # Lo stesso criterio con R^2: |z|^2 > R^2 equivale a |z| > R per R > 0.
    for caso in CASI_FUGA_CANONICI:
        esito = esito_fuga(caso.z_iniziale, caso.c, caso.limite_iterazioni, caso.raggio_fuga)
        z, c, n_max = caso.z_iniziale, caso.c, caso.limite_iterazioni
        soglia = caso.raggio_fuga * caso.raggio_fuga
        if z.real * z.real + z.imag * z.imag > soglia:
            assert esito.indice_fuga == 0
            continue
        indice = None
        for passo in range(1, n_max + 1):
            z = z * z + c
            if z.real * z.real + z.imag * z.imag > soglia:
                indice = passo
                break
        assert esito.indice_fuga == indice, caso.codice


def test_costo_limitato_dal_budget_e_arresto_immediato():
    # Un punto usa al massimo N aggiornamenti; la fuga immediata ne usa zero.
    assert esito_fuga(0.0j, 0.0j, 10, 2.0).aggiornamenti_eseguiti == 10
    assert esito_fuga(0.0j, 2.0 + 0.0j, 10, 2.0).aggiornamenti_eseguiti == 2
    assert esito_fuga(0.0j, 2.0 + 0.0j, 500, 2.0).aggiornamenti_eseguiti == 2
    assert isinstance(esito_fuga(0.0j, 0.0j, 10, 2.0), EsitoFuga)


def test_errori_di_dominio_del_kernel():
    with pytest.raises(ValueError):
        esito_fuga(0.0j, 1.0 + 0.0j, 0, 2.0)
    with pytest.raises(TypeError):
        esito_fuga(0.0j, 1.0 + 0.0j, True, 2.0)
    with pytest.raises(ValueError):
        esito_fuga(0.0j, 1.0 + 0.0j, 10, 0.0)
    with pytest.raises(ValueError):
        esito_fuga(0.0j, 1.0 + 0.0j, 10, float("nan"))
    with pytest.raises(ValueError):
        esito_fuga(complex(float("inf"), 0.0), 0.0j, 10, 2.0)
    with pytest.raises(TypeError):
        esito_fuga(0.0j, 1.0 + 0.0j, 10, True)
    with pytest.raises(TypeError):
        esito_mandelbrot("1", 10)
    with pytest.raises(ValueError):
        esito_julia(0.0j, 0.0j, -3)
    with pytest.raises(TypeError):
        esito_fuga_reali(0.0, 0.0, 1.0, "0.0", 10, 2.0)
