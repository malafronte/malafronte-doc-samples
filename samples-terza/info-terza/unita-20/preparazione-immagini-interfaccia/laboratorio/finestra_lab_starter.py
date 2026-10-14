"""Starter del laboratorio LAB-PY-U20-B — Unità 20 (L6).

Il file fornisce l'infrastruttura del laboratorio, lasciando allo studente
il lavoro previsto dalle fasi:

- forniti: ricostruzione della vista `4×2` (fase 1), colorazione di una
  matrice di esiti fornita con salvataggio e riapertura del PNG (fase 2),
  conversione dalla posizione nel widget alla cella con offset e scala
  (fasi 4–5);
- da completare (fase 3): `converti_campo_intero` per i campi della finestra
  (conversione da stringa con messaggio su campo, dominio e correzione);
- da completare (fase 4): `mostra_immagine_su_canvas` con conservazione
  esplicita del riferimento all'immagine Tk.

La soluzione completa e verificata dei meccanismi è negli esempi
preparatori (`coordinate_esempi.py`, `palette_esempi.py`,
`griglia_pillow.py`, `finestra_griglia.py`); questo starter conserva il
lavoro richiesto senza integrare i generatori dei frattali, che resta compito
della consegna autonoma. Eseguire dalla radice del progetto
`preparazione-immagini-interfaccia`:

```powershell
uv run pytest -q laboratorio/test_pubblici.py
```
"""

from pathlib import Path

from PIL import Image

from coordinate_esempi import griglia_punti
from finestra_griglia import posizione_widget_a_cella
from griglia_pillow import matrice_a_immagine, riapri_png_verificato, salva_png


def punti_vista_4x2() -> tuple[tuple[complex, ...], ...]:
    """Restituisce gli otto punti della vista canonica `4×2` (fornita, fase 1)."""
    return griglia_punti(4, 2, 0.0, 0.0, 4.0)


def colori_matrice_fornita() -> dict[tuple[int, int], tuple[int, int, int]]:
    """Colora la matrice `((None, 0), (1, 2))` con `bande`, `N = 6` (fornita, fase 2)."""
    matrice = ((None, 0), (1, 2))
    immagine = matrice_a_immagine(matrice, 6, "bande")
    colori: dict[tuple[int, int], tuple[int, int, int]] = {}
    for q in range(2):
        for p in range(2):
            colori[(p, q)] = immagine.getpixel((p, q))
    return colori


def salva_e_riapri_matrice_fornita(cartella: Path) -> Image.Image:
    """Salva e riapre la matrice fornita come PNG `2×2` (fornita, fase 2)."""
    matrice = ((None, 0), (1, 2))
    immagine = matrice_a_immagine(matrice, 6, "bande")
    percorso = salva_png(immagine, cartella / "matrice-fornita.png")
    return riapri_png_verificato(percorso, 2, 2)


def cella_da_posizione_immagine(
    x_widget: float, y_widget: float, scala_anteprima: int = 1
) -> tuple[int, int] | None:
    """Converte la posizione nel widget nella cella della zona `320×240` (fornita, fasi 4–5).

    La zona dell'immagine ha offset `(8, 8)` e mostra la griglia dimostrativa
    `160×120`; la scala distingue l'immagine calcolata dall'anteprima.
    """
    return posizione_widget_a_cella(x_widget, y_widget, 8.0, 8.0, scala_anteprima, 160, 120)


def converti_campo_intero(testo: str, nome_campo: str, minimo: int, massimo: int) -> int:
    """Converte il testo di un campo in intero validato (da completare, fase 3).

    Il messaggio di errore identifica campo, dominio ammesso e correzione.
    """
    raise NotImplementedError("Fase 3: convertire la stringa e validare l'intervallo.")


def mostra_immagine_su_canvas(canvas, immagine, fabbrica_immagine, registro_riferimenti):
    """Mostra l'immagine sul canvas conservandone il riferimento (da completare, fase 4).

    Crea l'oggetto immagine con `fabbrica_immagine`, lo dispone sul canvas
    all'offset `(8, 8)` con ancora `"nw"`, conserva il riferimento in
    `registro_riferimenti` (senza il riferimento Python l'immagine Tk
    scomparirebbe) e restituisce l'identificativo dell'oggetto canvas.
    """
    raise NotImplementedError("Fase 4: creare l'immagine, conservarne il riferimento.")
