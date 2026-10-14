"""Verifica di coordinate, palette, matrici e PNG — Unità 20 (L5).

La suite verifica i moduli applicativi di PY-40 (`coordinate_esempi.py`,
`palette_esempi.py`, `griglia_pillow.py`) contro gli oracoli del contratto L1
(`contratti_raster_json.py`), senza aprire finestre grafiche:

- gli otto punti della griglia canonica `4×2` e il pixel unico `1×1`;
- la scala uniforme su due rapporti d'immagine diversi;
- zoom e spostamento della vista con i limiti operativi;
- l'accordo con l'oracolo delle palette e la distinzione `None` contro `0`;
- la conservazione degli esiti matematici al cambio di palette;
- la matrice degli esiti con un classificatore indipendente e le statistiche
  di costo (`W`, `H`, `N`, aggiornamenti effettivi, memoria);
- il salvataggio PNG con riapertura e verifica di dimensioni, modalità RGB,
  pixel scelti e riproducibilità dei byte.
"""

import math

import pytest

from contratti_raster_json import (
    GRIGLIA_CANONICA_4X2,
    PALETTE_AMMESSE,
    TOLLERANZA_COORDINATE,
    VISTA_CANONICA_1X1,
    VISTA_CANONICA_4X2,
    colora_esito_riferimento,
    costruisci_griglia_campioni_riferimento,
    trasforma_punti_geometrici_in_pixel_riferimento,
)
from coordinate_esempi import (
    adatta_geometria_a_raster,
    ampiezza_verticale,
    griglia_punti,
    passo_campionamento,
    punto_da_pixel,
    sposta_vista,
    zoom_vista,
)
from griglia_pillow import (
    costruisci_matrice_esiti,
    disegna_segmenti,
    disegna_triangoli_pieni,
    matrice_a_immagine,
    riapri_png_verificato,
    salva_png,
    statistiche_matrice,
    valida_matrice_esiti,
)
from palette_esempi import colora_esito, legenda_palette


def classifica_mandelbrot_giocattolo(punto: complex, limite: int = 6) -> int | None:
    """Oracolo indipendente del kernel di Mandelbrot per le prove sulla matrice.

    Applica lo stesso contratto di PY-39 (seme `z_0 = 0`, raggio `2.0`,
    controllo iniziale, aggiornamento seguito dal confronto stretto `|z| > 2`,
    `None` a budget esaurito) senza importare i moduli del progetto gemello.
    """
    z = 0.0j
    if abs(z) > 2.0:
        return 0
    for passo in range(1, limite + 1):
        z = z * z + punto
        if abs(z) > 2.0:
            return passo
    return None


def test_otto_punti_griglia_canonica_e_pixel_unico() -> None:
    assert math.isclose(ampiezza_verticale(4.0, 4, 2), 2.0, abs_tol=TOLLERANZA_COORDINATE)
    griglia = griglia_punti(4, 2, 0.0, 0.0, 4.0)
    assert len(griglia) == 2
    assert all(len(riga) == 4 for riga in griglia)
    for q in range(2):
        for p in range(4):
            assert abs(griglia[q][p] - GRIGLIA_CANONICA_4X2[q][p]) < TOLLERANZA_COORDINATE
    # Confronto con l'oracolo L1 sulla stessa vista canonica
    attesi = costruisci_griglia_campioni_riferimento(VISTA_CANONICA_4X2)
    for q in range(2):
        for p in range(4):
            assert abs(griglia[q][p] - attesi[q][p]) < TOLLERANZA_COORDINATE
    # Il pixel unico campiona esattamente il centro della vista
    unico = punto_da_pixel(0, 0, 1, 1, -0.5, 0.25, 3.5)
    assert abs(unico - (-0.5 + 0.25j)) < TOLLERANZA_COORDINATE
    assert griglia_punti(1, 1, -0.5, 0.25, 3.5) == ((-0.5 + 0.25j,),)
    assert VISTA_CANONICA_1X1.larghezza == 1 and VISTA_CANONICA_1X1.altezza == 1


def test_passo_uniforme_e_due_rapporti_immagine() -> None:
    passo_x, passo_y = passo_campionamento(4, 2, 4.0)
    assert math.isclose(passo_x, 1.0, abs_tol=TOLLERANZA_COORDINATE)
    assert math.isclose(passo_y, passo_x, abs_tol=TOLLERANZA_COORDINATE)
    # La riga superiore ha immaginaria maggiore: l'asse verticale è invertito
    griglia = griglia_punti(4, 2, 0.0, 0.0, 4.0)
    assert griglia[0][0].imag > griglia[1][0].imag

    triangolo = ((0.0, 0.0), (3.0, 0.0), (1.5, 1.5 * math.sqrt(3.0)))
    for larghezza, altezza in ((320, 240), (240, 480)):
        punti = adatta_geometria_a_raster(triangolo, larghezza, altezza)
        attesi = trasforma_punti_geometrici_in_pixel_riferimento(
            list(triangolo), larghezza=larghezza, altezza=altezza
        )
        for osservato, atteso in zip(punti, attesi, strict=True):
            assert math.isclose(osservato[0], atteso[0], rel_tol=1e-9)
            assert math.isclose(osservato[1], atteso[1], rel_tol=1e-9)
        lato_01 = math.hypot(punti[1][0] - punti[0][0], punti[1][1] - punti[0][1])
        lato_12 = math.hypot(punti[2][0] - punti[1][0], punti[2][1] - punti[1][1])
        lato_20 = math.hypot(punti[0][0] - punti[2][0], punti[0][1] - punti[2][1])
        assert math.isclose(lato_01, lato_12, rel_tol=1e-9)
        assert math.isclose(lato_12, lato_20, rel_tol=1e-9)
        # Il vertice superiore (y maggiore) ottiene la coordinata pixel minore
        assert punti[2][1] < punti[0][1]


def test_zoom_conserva_centro_e_ricostruisce_ampiezza() -> None:
    avvicinata = zoom_vista(VISTA_CANONICA_4X2, 0.5)
    assert avvicinata.centro_reale == VISTA_CANONICA_4X2.centro_reale
    assert avvicinata.centro_immaginaria == VISTA_CANONICA_4X2.centro_immaginaria
    assert math.isclose(avvicinata.ampiezza_orizzontale, 2.0, abs_tol=TOLLERANZA_COORDINATE)
    assert math.isclose(avvicinata.ampiezza_verticale, 1.0, abs_tol=TOLLERANZA_COORDINATE)
    ripristinata = zoom_vista(avvicinata, 2.0)
    assert abs(ripristinata.ampiezza_orizzontale - 4.0) < TOLLERANZA_COORDINATE
    with pytest.raises(ValueError, match="positiv"):
        zoom_vista(VISTA_CANONICA_4X2, 0.0)
    with pytest.raises(ValueError, match="limiti"):
        zoom_vista(VISTA_CANONICA_4X2, 10.0)
    with pytest.raises(TypeError):
        zoom_vista((0.0, 0.0, 4.0), 0.5)


def test_sposta_centro_conserva_ampiezza_e_risoluzione() -> None:
    spostata = sposta_vista(VISTA_CANONICA_4X2, -0.5, 0.25)
    assert (spostata.centro_reale, spostata.centro_immaginaria) == (-0.5, 0.25)
    assert spostata.ampiezza_orizzontale == VISTA_CANONICA_4X2.ampiezza_orizzontale
    assert (spostata.larghezza, spostata.altezza) == (4, 2)
    punto = punto_da_pixel(
        0,
        0,
        spostata.larghezza,
        spostata.altezza,
        spostata.centro_reale,
        spostata.centro_immaginaria,
        spostata.ampiezza_orizzontale,
    )
    assert abs(punto - (-2.0 + 0.75j)) < TOLLERANZA_COORDINATE
    with pytest.raises(ValueError, match="limiti"):
        sposta_vista(VISTA_CANONICA_4X2, 200.0, 0.0)


@pytest.mark.parametrize("nome_palette", PALETTE_AMMESSE)
def test_palette_accordano_oracolo_e_rgb_validi(nome_palette: str) -> None:
    for indice in (None, 0, 1, 50, 100):
        colore = colora_esito(indice, 100, nome_palette)
        assert colore == colora_esito_riferimento(indice, 100, nome_palette)
        assert len(colore) == 3
        assert all(isinstance(c, int) and 0 <= c <= 255 for c in colore)
    # La distinzione obbligatoria: None non è 0 e la ripetizione è deterministica
    assert colora_esito(None, 100, nome_palette) != colora_esito(0, 100, nome_palette)
    assert colora_esito(100, 100, nome_palette) != colora_esito(None, 100, nome_palette)
    assert colora_esito(0, 100, nome_palette) == colora_esito(0, 100, nome_palette)
    legenda = legenda_palette(nome_palette, 100)
    assert f"'{nome_palette}'" in legenda and "N = 100" in legenda


def test_cambio_palette_conserva_esiti_matematici() -> None:
    matrice = costruisci_matrice_esiti(classifica_mandelbrot_giocattolo, 4, 2, 0.0, 0.0, 4.0, 6)
    immagine_bande = matrice_a_immagine(matrice, 6, "bande")
    immagine_binaria = matrice_a_immagine(matrice, 6, "binaria")
    assert immagine_bande.size == immagine_binaria.size == (4, 2)
    assert immagine_bande.mode == immagine_binaria.mode == "RGB"
    # Gli esiti matematici restano gli stessi: cambia solo la veste RGB
    assert valida_matrice_esiti(matrice) == matrice
    assert immagine_bande.tobytes() != immagine_binaria.tobytes()
    # Il pixel interno (None) usa il colore dedicato della legenda
    for q in range(2):
        for p in range(4):
            atteso = colora_esito(matrice[q][p], 6, "bande")
            assert immagine_bande.getpixel((p, q)) == atteso


def test_matrice_esiti_ordine_e_statistiche_di_costo() -> None:
    matrice = costruisci_matrice_esiti(classifica_mandelbrot_giocattolo, 4, 2, 0.0, 0.0, 4.0, 6)
    assert len(matrice) == 2 and all(len(riga) == 4 for riga in matrice)
    # L'accesso segue la convenzione delle righe: matrice[q][p]
    assert matrice[0][0] == classifica_mandelbrot_giocattolo(-1.5 + 0.5j, 6)
    assert matrice[1][3] == classifica_mandelbrot_giocattolo(1.5 - 0.5j, 6)
    statistiche = statistiche_matrice(matrice, 6)
    assert statistiche.larghezza == 4 and statistiche.altezza == 2
    assert statistiche.limite_iterazioni == 6
    assert statistiche.punti_totali == 8
    assert statistiche.punti_fuga + statistiche.punti_interni == 8
    assert statistiche.limite_superiore == 8 * 6
    assert statistiche.aggiornamenti_totali <= statistiche.limite_superiore
    assert statistiche.byte_immagine_rgb == 8 * 3
    # Almeno un bordo fugge e almeno un centro resta interno sulla vista canonica
    assert statistiche.punti_fuga >= 1 and statistiche.punti_interni >= 1
    with pytest.raises(ValueError, match="supera"):
        statistiche_matrice(((7,),), 6)


def test_png_riaperto_verifica_dimensioni_modalita_pixel(tmp_path) -> None:
    matrice = ((None, 0), (1, 2))
    immagine = matrice_a_immagine(matrice, 6, "bande")
    assert immagine.getpixel((0, 0)) == colora_esito(None, 6, "bande")
    assert immagine.getpixel((1, 0)) == colora_esito(0, 6, "bande")
    percorso = salva_png(immagine, tmp_path / "annidata" / "prova.png")
    assert percorso.is_file()
    riaperta = riapri_png_verificato(percorso, 2, 2)
    assert riaperta.size == (2, 2) and riaperta.mode == "RGB"
    assert riaperta.getpixel((0, 0)) == colora_esito(None, 6, "bande")
    assert riaperta.getpixel((1, 1)) == colora_esito(2, 6, "bande")
    # Il salvataggio è riproducibile: due scritture producono gli stessi byte
    percorso_bis = salva_png(immagine, tmp_path / "annidata" / "prova-bis.png")
    assert percorso.read_bytes() == percorso_bis.read_bytes()
    with pytest.raises(ValueError, match="attesi"):
        riapri_png_verificato(percorso, 3, 2)
    with pytest.raises(FileNotFoundError):
        riapri_png_verificato(tmp_path / "assente.png", 2, 2)


def test_disegno_geometrico_produce_immagini_rgb() -> None:
    punti = adatta_geometria_a_raster(((0.0, 0.0), (3.0, 0.0), (1.5, 1.5)), 60, 40)
    segmenti = [(punti[0], punti[1]), (punti[1], punti[2]), (punti[2], punti[0])]
    figura = disegna_segmenti(60, 40, segmenti, (11, 30, 46))
    assert figura.size == (60, 40) and figura.mode == "RGB"
    triangoli = disegna_triangoli_pieni(
        60, 40, [punti], (232, 241, 245), colore_contorno=(11, 30, 46)
    )
    assert triangoli.size == (60, 40) and triangoli.mode == "RGB"
    with pytest.raises(ValueError, match="non vuota"):
        disegna_segmenti(60, 40, [], (0, 0, 0))


def test_rifiuta_input_invalidi() -> None:
    with pytest.raises(TypeError):
        punto_da_pixel(0, 0, True, 2, 0.0, 0.0, 4.0)
    with pytest.raises(ValueError):
        punto_da_pixel(0, 0, 4, 2, 0.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        punto_da_pixel(4, 0, 4, 2, 0.0, 0.0, 4.0)
    with pytest.raises(ValueError):
        colora_esito(0, 100, "acquerello")
    with pytest.raises(ValueError, match="0\\.\\.100"):
        colora_esito(101, 100, "bande")
    with pytest.raises(TypeError):
        colora_esito(True, 100, "bande")
    with pytest.raises(TypeError):
        valida_matrice_esiti([])
    with pytest.raises(ValueError, match="prima riga"):
        valida_matrice_esiti(((None, 0), (None,)))
    with pytest.raises(TypeError):
        costruisci_matrice_esiti("non-chiamabile", 4, 2, 0.0, 0.0, 4.0, 6)
    with pytest.raises(ValueError, match=".png"):
        salva_png(matrice_a_immagine(((None,),), 1), "immagine.jpg")
