"""Genera i PNG didattici del capitolo PY-40 — Unità 20 (L5).

Lo script applica gli algoritmi verificati dei lotti precedenti (costruzioni
geometriche L2, kernel di fuga L4, coordinate e palette L5) e produce le sei
immagini didattiche del capitolo con parametri dichiarati:

- Mandelbrot nella vista iniziale e in un ingrandimento moderato;
- Julia con `c = 0` e con `c = -0.8 + 0.156i`;
- fiocco di Koch e triangolo di Sierpiński ai livelli applicativi.

Esegue inoltre il confronto per il problema svolto (raddoppio di una sola
dimensione, di entrambe e aumento di `N` sulla stessa vista) con conteggio
degli aggiornamenti effettivi e tempo misurato.

Esecuzione dalla cartella `unita-20` (gli import attraversano i due progetti
preparatori fratelli)::

    $env:PYTHONPATH = "preparazione-geometria-orbite"
    $env:PYTHONPATH += ";preparazione-immagini-interfaccia"
    uv run --directory preparazione-immagini-interfaccia `
        python ../figure/genera_png_py40.py --dest <cartella>

Ambiente: CPython 3.14 con `pillow` dell'ambiente `preparazione-immagini-interfaccia`.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from dati_canonici import TRIANGOLO_SIERPINSKI_BASE, VERTICI_FIOCCO_ORARIO
from fuga_esempi import esito_julia, esito_mandelbrot
from geometria_esempi import fiocco_koch, triangoli_sierpinski

from coordinate_esempi import adatta_geometria_a_raster
from griglia_pillow import (
    costruisci_matrice_esiti,
    disegna_segmenti,
    disegna_triangoli_pieni,
    matrice_a_immagine,
    salva_png,
    statistiche_matrice,
)

VISTA_MANDELBROT_INIZIALE = {"centro": (-0.5, 0.0), "s_x": 3.5}
VISTA_MANDELBROT_ZOOM = {"centro": (-0.745, 0.1), "s_x": 0.5}
VISTA_JULIA = {"centro": (0.0, 0.0), "s_x": 3.5}
RISOLUZIONE_DIDATTICA = (320, 240)
LIMITE_DIDATTICO = 100
PALETTE_DIDATTICA = "bande"


def classifica_mandelbrot(punto: complex) -> int | None:
    """Restituisce l'indice di fuga di Mandelbrot con il kernel verificato L4."""
    return esito_mandelbrot(punto, LIMITE_DIDATTICO).indice_fuga


def classifica_julia_zero(punto: complex) -> int | None:
    """Restituisce l'indice di fuga di Julia con `c = 0` e `N = 100`."""
    return esito_julia(punto, 0.0j, LIMITE_DIDATTICO).indice_fuga


def classifica_julia_dendrite(punto: complex) -> int | None:
    """Restituisce l'indice di fuga di Julia con `c = -0.8 + 0.156i` e `N = 100`."""
    return esito_julia(punto, complex(-0.8, 0.156), LIMITE_DIDATTICO).indice_fuga


def confronto_problema_svolto() -> None:
    """Confronta raddoppi di risoluzione e di budget sulla vista iniziale di Mandelbrot."""
    print("Problema svolto: raddoppi di risoluzione e di budget (vista iniziale di Mandelbrot)")
    print(f"{'caso':<22}{'W':>5}{'H':>5}{'N':>5}{'W·H·N':>12}{'aggiornamenti':>15}{'tempo_ms':>10}")
    for etichetta, w, h, n_max in (
        ("base 80x60 N=50", 80, 60, 50),
        ("raddoppio W 160x60", 160, 60, 50),
        ("raddoppio W,H 160x120", 160, 120, 50),
        ("raddoppio N 80x60", 80, 60, 100),
    ):
        conteggio = {"totale": 0}

        def classifica(punto: complex, limite: int = n_max) -> int | None:
            esito = esito_mandelbrot(punto, limite)
            conteggio["totale"] += limite if esito.indice_fuga is None else esito.indice_fuga
            return esito.indice_fuga

        inizio = time.perf_counter()
        matrice = costruisci_matrice_esiti(classifica, w, h, -0.5, 0.0, 3.5, n_max)
        durata_ms = (time.perf_counter() - inizio) * 1000.0
        statistiche = statistiche_matrice(matrice, n_max)
        assert conteggio["totale"] == statistiche.aggiornamenti_totali
        print(
            f"{etichetta:<22}{w:>5}{h:>5}{n_max:>5}"
            f"{w * h * n_max:>12}{conteggio['totale']:>15}{durata_ms:>10.1f}"
        )


def genera_numeriche(dest: Path) -> None:
    """Genera i quattro PNG numerici con vista, risoluzione, budget e palette registrati."""
    w, h = RISOLUZIONE_DIDATTICA
    casi = (
        (
            "mandelbrot-vista-iniziale.png",
            classifica_mandelbrot,
            *VISTA_MANDELBROT_INIZIALE["centro"],
            VISTA_MANDELBROT_INIZIALE["s_x"],
        ),
        (
            "mandelbrot-zoom-moderato.png",
            classifica_mandelbrot,
            *VISTA_MANDELBROT_ZOOM["centro"],
            VISTA_MANDELBROT_ZOOM["s_x"],
        ),
        ("julia-c-zero.png", classifica_julia_zero, *VISTA_JULIA["centro"], VISTA_JULIA["s_x"]),
        (
            "julia-c-meno08-0156.png",
            classifica_julia_dendrite,
            *VISTA_JULIA["centro"],
            VISTA_JULIA["s_x"],
        ),
    )
    for nome, classifica, x_c, y_c, s_x in casi:
        matrice = costruisci_matrice_esiti(classifica, w, h, x_c, y_c, s_x, LIMITE_DIDATTICO)
        statistiche = statistiche_matrice(matrice, LIMITE_DIDATTICO)
        immagine = matrice_a_immagine(matrice, LIMITE_DIDATTICO, PALETTE_DIDATTICA)
        percorso = salva_png(immagine, dest / nome)
        print(
            f"{nome}: centro=({x_c}, {y_c}) s_x={s_x} {w}x{h} N={LIMITE_DIDATTICO} "
            f"palette={PALETTE_DIDATTICA} fuga={statistiche.punti_fuga}/{statistiche.punti_totali} "
            f"aggiornamenti={statistiche.aggiornamenti_totali}/{statistiche.limite_superiore} "
            f"byte={percorso.stat().st_size}"
        )


def genera_geometriche(dest: Path) -> None:
    """Genera i due PNG geometrici dai generatori verificati L2."""
    w, h = RISOLUZIONE_DIDATTICA
    segmenti = fiocco_koch(VERTICI_FIOCCO_ORARIO, 3)
    punti_fiocco = [p for segmento in segmenti for p in segmento]
    fiocco_px = adatta_geometria_a_raster(punti_fiocco, w, h)
    segmenti_px = [(fiocco_px[2 * i], fiocco_px[2 * i + 1]) for i in range(len(segmenti))]
    fiocco = disegna_segmenti(w, h, segmenti_px, (14, 107, 133))
    print(f"koch-fiocco-livello3.png: {len(segmenti)} segmenti, livello=3, {w}x{h}")

    triangoli = triangoli_sierpinski(TRIANGOLO_SIERPINSKI_BASE, 4, "pieno")
    punti_sierpinski = [p for triangolo in triangoli for p in triangolo]
    adatti_px = adatta_geometria_a_raster(punti_sierpinski, w, h)
    triangoli_px = [
        (adatti_px[3 * i], adatti_px[3 * i + 1], adatti_px[3 * i + 2])
        for i in range(len(triangoli))
    ]
    figura = disegna_triangoli_pieni(
        w, h, triangoli_px, (28, 126, 214), colore_contorno=(11, 30, 46)
    )
    print(f"sierpinski-livello4.png: {len(triangoli)} triangoli, livello=4, stile=pieno, {w}x{h}")
    salva_png(fiocco, dest / "koch-fiocco-livello3.png")
    salva_png(figura, dest / "sierpinski-livello4.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera i PNG didattici di PY-40.")
    parser.add_argument(
        "--dest", type=Path, required=True, help="Cartella di destinazione dei PNG."
    )
    args = parser.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)
    confronto_problema_svolto()
    genera_numeriche(args.dest)
    genera_geometriche(args.dest)


if __name__ == "__main__":
    main()
