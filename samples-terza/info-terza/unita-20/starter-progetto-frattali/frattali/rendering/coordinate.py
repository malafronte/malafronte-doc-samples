"""Campionamento del piano e adattamento geometrico (da completare, tappa FR-M5).

Contratto: `punto_da_pixel` campiona il centro del pixel `(p, q)` con scala
uniforme (`s_y = s_x * H / W`) e asse verticale invertito; `griglia_punti`
costruisce la matrice dei punti; `zoom_vista` cambia l'ampiezza con centro
conservato (requisiti FR-05 e FR-08).
"""


def punto_da_pixel(
    colonna_p: object,
    riga_q: object,
    larghezza: object,
    altezza: object,
    centro_reale: object,
    centro_immaginaria: object,
    ampiezza_orizzontale: object,
):
    """Restituisce il punto al centro del pixel (da completare, FR-M5)."""
    raise NotImplementedError("FR-M5: centro del pixel, scala uniforme, asse invertito.")


def griglia_punti(
    larghezza: object,
    altezza: object,
    centro_reale: object,
    centro_immaginaria: object,
    ampiezza_orizzontale: object,
):
    """Restituisce la matrice `H x W` dei punti (da completare, FR-M5)."""
    raise NotImplementedError("FR-M5: doppio ciclo con punto_da_pixel su ogni cella.")


def zoom_vista(centro: object, ampiezza_orizzontale: object, fattore: object):
    """Restituisce `(centro, ampiezza / fattore)` (da completare, FR-M5/FR-08)."""
    raise NotImplementedError("FR-M5: ampiezza divisa per il fattore, centro conservato.")
