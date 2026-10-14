"""Casi pubblici del laboratorio LAB-PY-U20-B — Unità 20 (L6).

I casi LAB-B-01–LAB-B-08 verificano le sei fasi del laboratorio su un
dominio circoscritto, senza integrare i generatori dei frattali (compito
della consegna autonoma). Esito iniziale previsto: 5 casi superati e 3
falliti con `NotImplementedError` sui punti di lavoro delle fasi 3 e 4.
"""

from finestra_lab_starter import (
    cella_da_posizione_immagine,
    colori_matrice_fornita,
    converti_campo_intero,
    mostra_immagine_su_canvas,
    punti_vista_4x2,
    salva_e_riapri_matrice_fornita,
)


class CanvasFinto:
    """Sostituto del canvas Tk per le prove senza finestra."""

    def __init__(self) -> None:
        self.chiamate: list[tuple] = []

    def create_image(self, x, y, anchor=None, image=None):
        self.chiamate.append((x, y, anchor, image))
        return 7


def test_lab_b_01_vista_4x2_otto_punti() -> None:
    griglia = punti_vista_4x2()
    assert len(griglia) == 2
    assert griglia[0][0] == complex(-1.5, 0.5)
    assert griglia[0][3] == complex(1.5, 0.5)
    assert griglia[1][0] == complex(-1.5, -0.5)
    assert griglia[1][3] == complex(1.5, -0.5)


def test_lab_b_02_colori_matrice_fornita() -> None:
    colori = colori_matrice_fornita()
    assert colori[(0, 0)] == (11, 30, 46)
    assert colori[(1, 0)] == (24, 100, 171)
    assert colori[(0, 1)] == (28, 126, 214)
    assert colori[(1, 1)] == (14, 107, 133)


def test_lab_b_03_png_matrice_fornita_riaperto(tmp_path) -> None:
    riaperta = salva_e_riapri_matrice_fornita(tmp_path)
    assert riaperta.size == (2, 2)
    assert riaperta.mode == "RGB"
    assert riaperta.getpixel((0, 0)) == (11, 30, 46)


def test_lab_b_04_cella_al_centro_dell_immagine() -> None:
    assert cella_da_posizione_immagine(88.0, 68.0) == (80, 60)


def test_lab_b_05_cella_fuori_dall_immagine() -> None:
    assert cella_da_posizione_immagine(4.0, 68.0) is None
    assert cella_da_posizione_immagine(88.0, 400.0) is None


def test_lab_b_06_conversione_campo_valido() -> None:
    assert converti_campo_intero("160", "larghezza", 1, 800) == 160


def test_lab_b_07_conversione_campo_invalido_con_messaggio() -> None:
    try:
        converti_campo_intero("abc", "larghezza", 1, 800)
    except ValueError as causa:
        messaggio = str(causa)
        assert "larghezza" in messaggio
        assert "1" in messaggio and "800" in messaggio
    else:
        raise AssertionError("Il testo 'abc' richiede ValueError.")


def test_lab_b_08_mostra_immagine_con_riferimento() -> None:
    canvas = CanvasFinto()
    fabbricate: list[object] = []

    def fabbrica(immagine):
        fabbricate.append(immagine)
        return "FOTO-SENTINELLA"

    registro: list[object] = []
    identificativo = mostra_immagine_su_canvas(canvas, "IMMAGINE", fabbrica, registro)
    assert identificativo == 7
    assert fabbricate == ["IMMAGINE"]
    assert registro == ["FOTO-SENTINELLA"]
    assert canvas.chiamate == [(8, 8, "nw", "FOTO-SENTINELLA")]
