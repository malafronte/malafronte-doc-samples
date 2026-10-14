"""Prove su complessi e orbite di PY-38: operazioni, tracce e tabella (L3)."""

import math

import pytest

from complessi_esempi import (
    concorda_con_complex,
    costruisci_complesso,
    differenza_complessi,
    differenza_coppie,
    modulo_complesso,
    modulo_coppia,
    modulo_quadro_complesso,
    parti,
    prodotto_complessi,
    prodotto_coppie,
    quadrato_complesso,
    quadrato_coppia,
    somma_complessi,
    somma_coppie,
)
from dati_canonici import (
    CASI_OPERAZIONI_COMPLESSE,
    TOLLERANZA_COMPLESSI,
    TRACCE_ORBITE_CANONICHE,
)
from orbite_esempi import (
    modulo_massimo_traccia,
    passo_quadratico,
    passo_quadratico_coppia,
    tabella_orbita,
    traccia_orbita,
    traccia_orbita_coppia,
)


def test_casi_canonici_su_complex_e_su_coppie_di_reali():
    attesi = {caso.nome: caso for caso in CASI_OPERAZIONI_COMPLESSE}
    assert modulo_complesso(attesi["modulo_3_piu_4j"].z_1) == 5.0
    assert modulo_quadro_complesso(3.0 + 4.0j) == 25.0
    assert modulo_coppia((3.0, 4.0)) == 5.0

    somma = somma_complessi(1.0 + 2.0j, 3.0 - 1.0j)
    assert abs(somma - (4.0 + 1.0j)) < TOLLERANZA_COMPLESSI
    assert somma_coppie((1.0, 2.0), (3.0, -1.0)) == (4.0, 1.0)

    differenza = differenza_complessi(3.0 - 1.0j, 1.0 + 2.0j)
    assert abs(differenza - (2.0 - 3.0j)) < TOLLERANZA_COMPLESSI
    assert differenza_coppie((3.0, -1.0), (1.0, 2.0)) == (2.0, -3.0)

    prodotto = prodotto_complessi(1.0 + 2.0j, 3.0 - 1.0j)
    assert abs(prodotto - (5.0 + 5.0j)) < TOLLERANZA_COMPLESSI
    assert prodotto_coppie((1.0, 2.0), (3.0, -1.0)) == (5.0, 5.0)

    quadrato = quadrato_complesso(1.0 + 2.0j)
    assert abs(quadrato - (-3.0 + 4.0j)) < TOLLERANZA_COMPLESSI
    assert quadrato_coppia((1.0, 2.0)) == (-3.0, 4.0)


def test_confronto_complex_contro_coppie_con_tolleranza_motivata():
    # Lo stesso aggiornamento su due strade diverse concorda entro 1e-12.
    assert concorda_con_complex(quadrato_coppia((1.0, 2.0)), quadrato_complesso(1.0 + 2.0j))
    assert concorda_con_complex(
        prodotto_coppie((0.1, 0.2), (0.3, -0.4)),
        prodotto_complessi(complex(0.1, 0.2), complex(0.3, -0.4)),
    )
    assert not concorda_con_complex((5.0, 5.0), 5.0 + 6.0j)


def test_aggiornamento_non_simultaneo_cambia_il_risultato():
    # Variante errata PY-U20-E02: riusa il valore di `a` già aggiornato.
    a, b = 1.0, 2.0
    a_nuovo = a * a - b * b
    b_errata = 2.0 * a_nuovo * b
    assert (a_nuovo, b_errata) == (-3.0, -12.0)
    assert quadrato_coppia((1.0, 2.0)) == (-3.0, 4.0)


def test_quattro_tracce_canoniche_con_stato_iniziale_e_aggiornamenti():
    parametri = {
        "c_zero_da_zero": 0.0j,
        "c_meno_uno_da_zero": -1.0 + 0.0j,
        "c_uno_da_zero": 1.0 + 0.0j,
        "c_i_da_zero": 1.0j,
    }
    for nome_traccia, c in parametri.items():
        attesa = TRACCE_ORBITE_CANONICHE[nome_traccia]
        traccia = traccia_orbita(0.0j, c, len(attesa) - 1)
        assert traccia == attesa
        # La traccia contiene un termine per lo stato iniziale più uno per aggiornamento.
        assert len(traccia) == len(attesa)
        # L'oracolo su coppie di reali produce gli stessi valori.
        traccia_reali = traccia_orbita_coppia((0.0, 0.0), (c.real, c.imag), len(attesa) - 1)
        for coppia, valore in zip(traccia_reali, attesa, strict=True):
            assert concorda_con_complex(coppia, valore)

    # Ripetizioni dichiarate: punto fisso, ciclo di periodo 2, divergenza, preperiodo.
    assert traccia_orbita(0.0j, 0.0j, 4) == (0.0j, 0.0j, 0.0j, 0.0j, 0.0j)
    assert traccia_orbita(0.0j, -1.0 + 0.0j, 4)[1] == -1.0 + 0.0j
    assert traccia_orbita(0.0j, 1.0 + 0.0j, 4)[3] == 5.0 + 0.0j
    assert traccia_orbita(0.0j, 1.0j, 4)[4] == -1.0 + 1.0j


def test_passo_singolo_e_traccia_con_zero_passi():
    assert passo_quadratico(1.0 + 2.0j, 3.0 - 1.0j) == (1.0 + 2.0j) ** 2 + (3.0 - 1.0j)
    assert passo_quadratico_coppia((1.0, 2.0), (0.0, 1.0)) == (-3.0, 5.0)
    assert traccia_orbita(2.0 + 0.0j, 0.0j, 0) == (2.0 + 0.0j,)
    assert traccia_orbita_coppia((2.0, 0.0), (0.0, 0.0), 0) == ((2.0, 0.0),)


def test_tabella_orbita_con_indice_valore_e_modulo():
    tabella = tabella_orbita(0.0j, 1.0 + 0.0j, 4)
    assert [riga["indice"] for riga in tabella] == [0, 1, 2, 3, 4]
    assert [riga["valore"] for riga in tabella] == [
        0.0j,
        1.0 + 0.0j,
        2.0 + 0.0j,
        5.0 + 0.0j,
        26.0 + 0.0j,
    ]
    attesi_moduli = [0.0, 1.0, 2.0, 5.0, 26.0]
    for riga, atteso in zip(tabella, attesi_moduli, strict=True):
        assert math.isclose(riga["modulo"], atteso, abs_tol=TOLLERANZA_COMPLESSI)
    # Confronto con la soglia 2: il termine di indice 2 è sul cerchio, quello di indice 3 è esterno.
    assert tabella[2]["modulo"] == 2.0
    assert tabella[3]["modulo"] > 2.0
    assert modulo_massimo_traccia(traccia_orbita(0.0j, 1.0 + 0.0j, 4)) == 26.0


def test_costruzione_dai_campi_e_lettura_delle_parti():
    costruito = costruisci_complesso(1.0, 2.0)
    assert costruito == 1.0 + 2.0j
    assert parti(1.0 + 2.0j) == (1.0, 2.0)
    assert parti(5.0) == (5.0, 0.0)
    # Python usa `j` per l'unità immaginaria: `1j` è il letterale, `complex(a, b)` la costruzione.
    assert complex(0.0, 1.0) == 1j
    assert (1.0j).real == 0.0
    assert (1.0j).imag == 1.0


def test_errori_di_dominio_su_complessi_e_orbite():
    with pytest.raises(TypeError):
        costruisci_complesso(True, 2.0)
    with pytest.raises(ValueError):
        costruisci_complesso(float("nan"), 0.0)
    with pytest.raises(ValueError):
        modulo_complesso(complex(float("inf"), 0.0))
    with pytest.raises(TypeError):
        traccia_orbita(0.0j, 1.0 + 0.0j, True)
    with pytest.raises(ValueError):
        traccia_orbita(0.0j, 1.0 + 0.0j, -1)
    with pytest.raises(ValueError):
        modulo_massimo_traccia(())
    with pytest.raises(TypeError):
        passo_quadratico_coppia((1.0, 2.0), "c")
