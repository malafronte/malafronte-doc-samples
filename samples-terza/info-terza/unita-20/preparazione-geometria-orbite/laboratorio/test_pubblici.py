"""Casi pubblici del laboratorio LAB-PY-U20-A — Unità 20 (L4).

I casi LAB-A-01–LAB-A-04 usano i moduli verificati di geometria, complessi e
orbite e sono superati dallo starter fornito. I casi LAB-A-05–LAB-A-11
richiedono le funzioni `esito_fuga`, `esito_mandelbrot` ed `esito_julia` dello
starter, da completare nelle fasi 4–5: falliscono con `NotImplementedError`
finché il lavoro non è svolto. Eseguire dalla radice del progetto:

```powershell
uv run pytest -q laboratorio/test_pubblici.py
```
"""

import pytest

from complessi_esempi import quadrato_complesso
from dati_canonici import EsitoFugaCanonico
from geometria_esempi import curva_koch, triangoli_sierpinski
from laboratorio.fuga_lab_starter import (
    esito_fuga,
    esito_julia,
    esito_mandelbrot,
    riga_tabella_esito,
)
from orbite_esempi import traccia_orbita


def test_lab_a_01_vertici_koch_livello_1():
    assert curva_koch(((0.0, 0.0), (3.0, 0.0)), 1)[1] == ((1.0, 0.0), (1.5, 0.8660254037844386))


def test_lab_a_02_triangoli_sierpinski_livello_1():
    base = ((0.0, 0.0), (4.0, 0.0), (2.0, 3.4641016151377544))
    assert len(triangoli_sierpinski(base, 1)) == 3


def test_lab_a_03_quadrato_fondamentale():
    assert quadrato_complesso(1.0 + 2.0j) == -3.0 + 4.0j


def test_lab_a_04_traccia_con_c_uno():
    assert traccia_orbita(0.0j, 1.0 + 0.0j, 4)[3] == 5.0 + 0.0j


def test_lab_a_05_budget_finito_con_c_uno():
    assert esito_fuga(0.0j, 1.0 + 0.0j, 2, 2.0).indice_fuga is None
    assert esito_fuga(0.0j, 1.0 + 0.0j, 3, 2.0).indice_fuga == 3


def test_lab_a_06_confine_con_c_meno_due():
    esito = esito_fuga(0.0j, -2.0 + 0.0j, 10, 2.0)
    assert esito.indice_fuga is None
    assert esito.valore_finale == 2.0 + 0.0j


def test_lab_a_07_fuga_immediata_con_seme_esterno():
    esito = esito_fuga(3.0 + 0.0j, 0.0j, 10, 2.0)
    assert esito.indice_fuga == 0
    assert esito.aggiornamenti_eseguiti == 0


def test_lab_a_08_punto_fisso_con_c_meno_sei():
    esito = esito_fuga(3.0 + 0.0j, -6.0 + 0.0j, 10, 6.0)
    assert esito.indice_fuga is None
    assert esito.valore_finale == 3.0 + 0.0j


def test_lab_a_09_chiamata_mandelbrot():
    assert esito_mandelbrot(1.0 + 0.0j, 3).indice_fuga == 3
    assert esito_mandelbrot(-1.0 + 0.0j, 10).indice_fuga is None


def test_lab_a_10_chiamata_julia():
    assert esito_julia(1.0 + 0.0j, 0.0j, 10).valore_finale == 1.0 + 0.0j
    assert esito_julia(3.0 + 0.0j, -6.0 + 0.0j, 10).indice_fuga is None


def test_lab_a_11_formattazione_della_tabella():
    esito = EsitoFugaCanonico(indice_fuga=3, aggiornamenti_eseguiti=3, valore_finale=5.0 + 0.0j)
    riga = riga_tabella_esito("M-05", esito)
    assert "M-05" in riga and "3" in riga and "(5+0j)" in riga
    with pytest.raises(TypeError):
        riga_tabella_esito("M-05", "fuga")
