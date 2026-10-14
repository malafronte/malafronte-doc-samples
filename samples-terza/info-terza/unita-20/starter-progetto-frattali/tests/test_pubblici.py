"""Casi pubblici di accettazione del Laboratorio dei frattali (FR-A01–FR-A15).

I casi verificano i requisiti osservabili della consegna su un dominio
circoscritto. Esito iniziale previsto: i casi sulle parti fornite sono
superati, gli altri falliscono con `NotImplementedError` sui punti di
lavoro delle tappe FR-M1–FR-M7. Esecuzione dalla radice dello starter:

```powershell
uv run pytest -q
```
"""

import json
import subprocess
import sys
from pathlib import Path

CARTELLA_CONFIGURAZIONI = Path(__file__).resolve().parent.parent / "configurazioni"


def test_fr_a01_koch_curva_livelli_0_1_2() -> None:
    from frattali.algoritmi.geometrici import produci_koch

    assert len(produci_koch(0, "curva", 3.0)) == 1
    assert produci_koch(0, "curva", 3.0) == (((0.0, 0.0), (3.0, 0.0)),)
    assert len(produci_koch(1, "curva", 3.0)) == 4
    assert len(produci_koch(2, "curva", 3.0)) == 16
    segmenti = produci_koch(1, "curva", 3.0)
    assert segmenti[0][0] == (0.0, 0.0)
    assert segmenti[-1][1] == (3.0, 0.0)


def test_fr_a02_fiocco_chiusura_e_punte_esterne() -> None:
    from frattali.algoritmi.geometrici import produci_koch

    assert len(produci_koch(0, "fiocco", 3.0)) == 3
    livello_1 = produci_koch(1, "fiocco", 3.0)
    assert len(livello_1) == 12
    # Spezzata chiusa e continua: ogni segmento inizia dove finisce il precedente
    for precedente, successivo in zip(livello_1, livello_1[1:] + livello_1[:1], strict=True):
        assert precedente[1] == successivo[0]


def test_fr_a03_sierpinski_livelli_0_1_2() -> None:
    from frattali.algoritmi.geometrici import produci_sierpinski

    assert len(produci_sierpinski(0, "pieno", 4.0)) == 1
    assert len(produci_sierpinski(1, "pieno", 4.0)) == 3
    assert len(produci_sierpinski(2, "pieno", 4.0)) == 9
    (a, b, c), _, _ = produci_sierpinski(1, "pieno", 4.0)
    assert a == (0.0, 0.0) and b == (2.0, 0.0) and c == (1.0, 1.7320508075688772)


def test_fr_a04_mandelbrot_budget_2_e_3() -> None:
    from frattali.algoritmi.quadratici import classifica_mandelbrot

    assert classifica_mandelbrot(complex(1.0, 0.0), 2) is None
    assert classifica_mandelbrot(complex(1.0, 0.0), 3) == 3


def test_fr_a05_mandelbrot_soglia_stretta() -> None:
    from frattali.algoritmi.quadratici import classifica_mandelbrot

    assert classifica_mandelbrot(complex(-2.0, 0.0), 10) is None


def test_fr_a06_julia_fuga_zero_e_punto_fisso() -> None:
    from frattali.algoritmi.quadratici import classifica_julia, raggio_sicuro_julia

    assert raggio_sicuro_julia(complex(-6.0, 0.0)) == 6.0
    assert classifica_julia(complex(3.0, 0.0), complex(0.0, 0.0), 10) == 0
    assert classifica_julia(complex(3.0, 0.0), complex(-6.0, 0.0), 10) is None


def test_fr_a07_vista_canonica_4x2() -> None:
    from frattali.rendering.coordinate import griglia_punti

    griglia = griglia_punti(4, 2, 0.0, 0.0, 4.0)
    assert griglia[0][0] == complex(-1.5, 0.5)
    assert griglia[0][3] == complex(1.5, 0.5)
    assert griglia[1][0] == complex(-1.5, -0.5)
    assert griglia[1][3] == complex(1.5, -0.5)


def test_fr_a08_stessa_vista_due_rapporti() -> None:
    from frattali.rendering.coordinate import punto_da_pixel

    for larghezza, altezza in ((4, 2), (8, 4)):
        passo_x = (
            punto_da_pixel(1, 0, larghezza, altezza, 0.0, 0.0, 4.0)
            - punto_da_pixel(0, 0, larghezza, altezza, 0.0, 0.0, 4.0)
        ).real
        passo_y = (
            punto_da_pixel(0, 0, larghezza, altezza, 0.0, 0.0, 4.0)
            - punto_da_pixel(0, 1, larghezza, altezza, 0.0, 0.0, 4.0)
        ).real
        assert passo_x == passo_y
    assert punto_da_pixel(0, 0, 4, 2, 0.0, 0.0, 4.0) == complex(-1.5, 0.5)


def test_fr_a09_zoom_centro_conservato_e_ripristino() -> None:
    from frattali.rendering.coordinate import zoom_vista

    centro, ampiezza = zoom_vista(complex(-0.5, 0.0), 3.5, 2.0)
    assert centro == complex(-0.5, 0.0)
    assert ampiezza == 1.75
    centro_2, ampiezza_2 = zoom_vista(centro, ampiezza, 0.5)
    assert centro_2 == complex(-0.5, 0.0)
    assert abs(ampiezza_2 - 3.5) < 1e-12


def test_fr_a10_round_trip_quattro_famiglie(tmp_path) -> None:
    from frattali.persistenza import carica_configurazione, salva_configurazione

    for nome in ("mandelbrot", "julia", "koch", "sierpinski"):
        configurazione = carica_configurazione(CARTELLA_CONFIGURAZIONI / f"{nome}.json")
        copia = tmp_path / f"{nome}.json"
        salva_configurazione(copia, configurazione)
        ricaricata = carica_configurazione(copia)
        assert ricaricata.a_dizionario() == configurazione.a_dizionario()


def test_fr_a11_invalidi_con_diagnosi_e_stato_preservato(tmp_path) -> None:
    from frattali.dominio import ErroreConfigurazione
    from frattali.persistenza import carica_configurazione

    corrente = carica_configurazione(CARTELLA_CONFIGURAZIONI / "mandelbrot.json")
    troncato = tmp_path / "troncato.json"
    troncato.write_text('{"versione_schema": 1,', encoding="utf-8")
    try:
        carica_configurazione(troncato)
    except ErroreConfigurazione:
        pass
    else:
        raise AssertionError("Il JSON troncato richiede ErroreConfigurazione.")
    versione_ignota = tmp_path / "versione.json"
    documento = json.loads(
        (CARTELLA_CONFIGURAZIONI / "mandelbrot.json").read_text(encoding="utf-8")
    )
    documento["versione_schema"] = 99
    versione_ignota.write_text(json.dumps(documento), encoding="utf-8")
    try:
        carica_configurazione(versione_ignota)
    except ErroreConfigurazione:
        pass
    else:
        raise AssertionError("La versione ignota richiede ErroreConfigurazione.")
    assert (
        corrente.a_dizionario()
        == carica_configurazione(CARTELLA_CONFIGURAZIONI / "mandelbrot.json").a_dizionario()
    )


def test_fr_a12_generazione_modifica_ed_esportazione(tmp_path) -> None:
    from frattali.algoritmi.quadratici import classifica_mandelbrot
    from frattali.persistenza import carica_configurazione
    from frattali.rendering.immagini import (
        costruisci_matrice_esiti,
        matrice_a_immagine,
        riapri_png_verificato,
        salva_png,
    )

    configurazione = carica_configurazione(CARTELLA_CONFIGURAZIONI / "mandelbrot.json")
    matrice = costruisci_matrice_esiti(
        configurazione, lambda punto: classifica_mandelbrot(punto, 25)
    )
    assert len(matrice) == 60 and len(matrice[0]) == 80
    immagine = matrice_a_immagine(matrice, configurazione)
    destinazione = salva_png(immagine, tmp_path / "mandelbrot.png")
    riaperta = riapri_png_verificato(destinazione, 80, 60)
    assert riaperta.size == (80, 60)
    assert riaperta.mode == "RGB"


def test_fr_a13_annullamento_e_nuovo_lavoro() -> None:
    from frattali.rendering.stato import (
        annulla_lavoro,
        avvia_lavoro,
        esegui_blocco,
        nuovo_lavoro,
    )

    lavoro = nuovo_lavoro({"segnaposto": True}, 1)
    avvia_lavoro(lavoro)
    assert esegui_blocco(lavoro, 1, lambda q: (None,)) is True
    assert annulla_lavoro(lavoro) is True
    assert esegui_blocco(lavoro, 1, lambda q: (None,)) is False
    successore = nuovo_lavoro({"segnaposto": True}, 2)
    avvia_lavoro(successore)
    assert esegui_blocco(successore, 1, lambda q: (None,)) is False
    assert esegui_blocco(successore, 2, lambda q: (None,)) is True


def test_fr_a14_chiusura_senza_effetti_dopo_annullamento() -> None:
    from frattali.rendering.stato import (
        annulla_lavoro,
        avvia_lavoro,
        esegui_blocco,
        etichetta_risultato,
        nuovo_lavoro,
    )

    lavoro = nuovo_lavoro({"segnaposto": True}, 1)
    avvia_lavoro(lavoro)
    esegui_blocco(lavoro, 1, lambda q: (None,))
    annulla_lavoro(lavoro)
    # Dopo l'annullamento (analogo della chiusura) nessuna callback ha effetti
    assert esegui_blocco(lavoro, 1, lambda q: (None,)) is False
    assert "annullato" in etichetta_risultato(lavoro).lower()


def test_fr_a15_ambiente_ricostruibile_e_configurazioni_presenti() -> None:
    import sys

    assert sys.version_info >= (3, 14)
    import tkinter  # noqa: F401

    import PIL  # noqa: F401

    for nome in ("mandelbrot", "julia", "koch", "sierpinski"):
        percorso = CARTELLA_CONFIGURAZIONI / f"{nome}.json"
        documento = json.loads(percorso.read_text(encoding="utf-8"))
        assert documento["versione_schema"] == 1
        assert documento["tipo_frattale"] == nome
        assert set(documento.keys()) == {
            "versione_schema",
            "tipo_frattale",
            "immagine",
            "vista",
            "parametri",
        }


def test_valori_forniti_con_rifiuto_dei_bool() -> None:
    import pytest

    from frattali.dominio import LimiteOperativoSuperato, ParametriImmagine, VistaComplessa

    vista = VistaComplessa(0.0, 0.0, 3.5)
    assert vista.ampiezza_orizzontale == 3.5
    with pytest.raises(TypeError):
        VistaComplessa(True, 0.0, 3.5)
    with pytest.raises(LimiteOperativoSuperato):
        ParametriImmagine(1000, 60)


def test_interfaccia_senza_display_all_importazione() -> None:
    processo = subprocess.run(
        [sys.executable, "-c", "import frattali.interfaccia, sys; print('tkinter' in sys.modules)"],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert processo.returncode == 0, processo.stderr
    assert processo.stdout.strip() == "False"
