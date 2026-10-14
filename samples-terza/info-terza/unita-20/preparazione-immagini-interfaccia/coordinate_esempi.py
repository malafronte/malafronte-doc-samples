"""Coordinate fra pixel e piano complesso e adattamento geometrico — Unità 20 (L5).

Il modulo implementa gli esempi preparatori dei nuclei B ed E del capitolo PY-40
(*Immagini dei frattali: pixel, coordinate e colori*):

- ampiezza verticale a scala uniforme (`s_y = s_x * H / W`) e campionamento al
  centro del pixel con asse verticale invertito (la riga `q` cresce verso il
  basso, la coordinata immaginaria cresce verso l'alto);
- griglia dei punti campionati, passo di campionamento e vista canonica `4×2`
  con gli otto punti attesi dal contratto L1;
- adattamento di una figura geometrica a un canvas raster con scala uniforme,
  margine e inversione verticale (stesso contratto dell'oracolo L1);
- zoom (varia l'ampiezza conservando il centro), spostamento (varia il centro
  conservando ampiezza e risoluzione) e limiti operativi della vista.

Le validazioni seguono le stesse regole dell'oracolo L1
(`contratti_raster_json.py`): interi non booleani, reali finiti non booleani e
rifiuto di `NaN`/`Infinity`. I limiti operativi della vista (centro in
`[-100, 100]`, ampiezza in `[1e-6, 20]`) sono quelli di `LIMITI_APPLICATIVI`.

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O
né apre finestre grafiche all'importazione.
"""

import math
from dataclasses import replace

from contratti_raster_json import LIMITI_APPLICATIVI, SpecificaVistaCanonico

type Punto2D = tuple[float, float]


def valida_intero_non_booleano(
    valore: object, nome_parametro: str, minimo: int | None = None
) -> int:
    """Verifica che `valore` sia un intero non booleano, oltre `minimo` se dichiarato."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError(f"Il parametro '{nome_parametro}' richiede un intero non booleano.")
    if minimo is not None and valore < minimo:
        raise ValueError(f"Il parametro '{nome_parametro}' richiede un valore >= {minimo}.")
    return valore


def valida_reale_finito(valore: object, nome_parametro: str) -> float:
    """Verifica che `valore` sia un numero reale finito non booleano."""
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        raise TypeError(f"Il parametro '{nome_parametro}' richiede un numero reale non booleano.")
    risultato = float(valore)
    if not math.isfinite(risultato):
        raise ValueError(f"Il parametro '{nome_parametro}' non ammette NaN o infinito.")
    return risultato


def ampiezza_verticale(
    ampiezza_orizzontale: object,
    larghezza: object,
    altezza: object,
) -> float:
    """Restituisce l'ampiezza verticale `s_y = s_x * H / W` a scala uniforme.

    La scala uniforme conserva le proporzioni geometriche: il passo orizzontale
    `s_x / W` e il passo verticale `s_y / H` coincidono.
    """
    s_x = valida_reale_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    if s_x <= 0.0:
        raise ValueError("Il parametro 'ampiezza_orizzontale' richiede un valore positivo.")
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    return s_x * (h / w)


def punto_da_pixel(
    colonna_p: object,
    riga_q: object,
    larghezza: object,
    altezza: object,
    centro_reale: object,
    centro_immaginaria: object,
    ampiezza_orizzontale: object,
) -> complex:
    """Restituisce il punto del piano campionato al centro del pixel `(p, q)`.

    Con `0 <= p < W`, `0 <= q < H` e `s_y = s_x * H / W`:

    - `x = x_c - s_x / 2 + (p + 0.5) * s_x / W`
    - `y = y_c + s_y / 2 - (q + 0.5) * s_y / H`

    Il mezzo pixel (`+ 0.5`) sposta il campione al centro della cella; il segno
    meno nella coordinata `y` inverte l'asse verticale perché la riga `q`
    cresce verso il basso mentre l'asse immaginario cresce verso l'alto. Gli
    estremi geometrici della vista sono i bordi dell'immagine; i centri dei
    pixel più esterni si trovano mezzo passo all'interno.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    p = valida_intero_non_booleano(colonna_p, "colonna_p", minimo=0)
    q = valida_intero_non_booleano(riga_q, "riga_q", minimo=0)
    if p >= w:
        raise ValueError(f"L'indice di colonna p={p} esce dall'intervallo 0..{w - 1}.")
    if q >= h:
        raise ValueError(f"L'indice di riga q={q} esce dall'intervallo 0..{h - 1}.")
    x_c = valida_reale_finito(centro_reale, "centro_reale")
    y_c = valida_reale_finito(centro_immaginaria, "centro_immaginaria")
    s_x = valida_reale_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    if s_x <= 0.0:
        raise ValueError("Il parametro 'ampiezza_orizzontale' richiede un valore positivo.")

    s_y = s_x * (h / w)
    x = x_c - (s_x / 2.0) + (p + 0.5) * (s_x / w)
    y = y_c + (s_y / 2.0) - (q + 0.5) * (s_y / h)
    return complex(x, y)


def griglia_punti(
    larghezza: object,
    altezza: object,
    centro_reale: object,
    centro_immaginaria: object,
    ampiezza_orizzontale: object,
) -> tuple[tuple[complex, ...], ...]:
    """Restituisce la matrice `H × W` dei punti campionati al centro dei pixel.

    La matrice si consulta con `griglia[q][p]`: l'indice di riga `q` seleziona
    la riga dell'immagine, l'indice di colonna `p` il pixel nella riga.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    x_c = valida_reale_finito(centro_reale, "centro_reale")
    y_c = valida_reale_finito(centro_immaginaria, "centro_immaginaria")
    s_x = valida_reale_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    if s_x <= 0.0:
        raise ValueError("Il parametro 'ampiezza_orizzontale' richiede un valore positivo.")
    return tuple(
        tuple(punto_da_pixel(p, q, w, h, x_c, y_c, s_x) for p in range(w)) for q in range(h)
    )


def passo_campionamento(
    larghezza: object,
    altezza: object,
    ampiezza_orizzontale: object,
) -> tuple[float, float]:
    """Restituisce la coppia `(passo_x, passo_y)` delle distanze fra campioni adiacenti.

    A scala uniforme i due passi coincidono: `passo_x = s_x / W` e
    `passo_y = s_y / H` con `s_y = s_x * H / W`.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    s_x = valida_reale_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    if s_x <= 0.0:
        raise ValueError("Il parametro 'ampiezza_orizzontale' richiede un valore positivo.")
    s_y = s_x * (h / w)
    return (s_x / w, s_y / h)


def valida_punto_geometrico(valore: object, nome_parametro: str) -> Punto2D:
    """Verifica che `valore` sia una coppia `(x, y)` di reali finiti non booleani."""
    if not isinstance(valore, (tuple, list)) or len(valore) != 2:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede una coppia (x, y).")
    x = valida_reale_finito(valore[0], f"{nome_parametro}[0]")
    y = valida_reale_finito(valore[1], f"{nome_parametro}[1]")
    return (x, y)


def adatta_geometria_a_raster(
    punti: object,
    larghezza: object,
    altezza: object,
    margine_relativo: object = 0.08,
) -> tuple[Punto2D, ...]:
    """Adatta punti geometrici a un canvas `W × H` con scala uniforme e margine.

    Il procedimento calcola il rettangolo di contenimento dei punti, applica
    un margine relativo sui quattro lati, sceglie un unico fattore di scala
    (il minore fra quello orizzontale e quello verticale, così le proporzioni
    si conservano), centra la figura nel canvas e inverte l'asse verticale
    (la `y` geometrica cresce verso l'alto, la riga del pixel cresce verso il
    basso). Un triangolo equilatero resta equilatero in finestre larghe e
    strette; il vertice con `y` maggiore ottiene la coordinata pixel minore.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    margine = valida_reale_finito(margine_relativo, "margine_relativo")
    if not (0.0 <= margine < 0.45):
        raise ValueError("Il parametro 'margine_relativo' richiede un valore in [0.0, 0.45).")
    if not isinstance(punti, (tuple, list)) or len(punti) == 0:
        raise ValueError("Il parametro 'punti' richiede una sequenza non vuota di punti.")
    validati = [valida_punto_geometrico(punto, f"punti[{i}]") for i, punto in enumerate(punti)]

    x_min = min(p[0] for p in validati)
    x_max = max(p[0] for p in validati)
    y_min = min(p[1] for p in validati)
    y_max = max(p[1] for p in validati)
    estensione_x = max(x_max - x_min, 1e-12)
    estensione_y = max(y_max - y_min, 1e-12)

    area_utile_x = w * (1.0 - 2.0 * margine)
    area_utile_y = h * (1.0 - 2.0 * margine)
    scala = min(area_utile_x / estensione_x, area_utile_y / estensione_y)

    centro_geom_x = 0.5 * (x_min + x_max)
    centro_geom_y = 0.5 * (y_min + y_max)
    centro_pixel_x = 0.5 * w
    centro_pixel_y = 0.5 * h
    return tuple(
        (
            centro_pixel_x + (x - centro_geom_x) * scala,
            centro_pixel_y - (y - centro_geom_y) * scala,
        )
        for x, y in validati
    )


def zoom_vista(vista: object, fattore: object) -> SpecificaVistaCanonico:
    """Restituisce la vista con ampiezza moltiplicata per `fattore`, a centro invariato.

    Un fattore `0 < f < 1` avvicina (zoom avanti, ampiezza ridotta); un fattore
    `f > 1` allontana (zoom indietro, ampiezza allargata). La risoluzione resta
    invariata e l'ampiezza verticale segue dal rapporto d'aspetto. Uno zoom
    avanti con fattore `0.5` seguito da uno zoom indietro con fattore `2.0`
    ricostruisce l'ampiezza iniziale entro la tolleranza delle coordinate.
    """
    if not isinstance(vista, SpecificaVistaCanonico):
        raise TypeError("Il parametro 'vista' richiede una SpecificaVistaCanonico.")
    f = valida_reale_finito(fattore, "fattore")
    if f <= 0.0:
        raise ValueError("Il parametro 'fattore' richiede un valore strettamente positivo.")
    nuova_ampiezza = vista.ampiezza_orizzontale * f
    limiti = LIMITI_APPLICATIVI
    if not (limiti.ampiezza_vista_min <= nuova_ampiezza <= limiti.ampiezza_vista_max):
        raise ValueError(
            f"L'ampiezza {nuova_ampiezza} esce dai limiti "
            f"[{limiti.ampiezza_vista_min}, {limiti.ampiezza_vista_max}]."
        )
    return replace(vista, ampiezza_orizzontale=nuova_ampiezza)


def sposta_vista(
    vista: object,
    delta_reale: object,
    delta_immaginaria: object,
) -> SpecificaVistaCanonico:
    """Restituisce la vista con centro spostato, ad ampiezza e risoluzione invariate.

    Lo spostamento somma `delta_reale` alla componente reale del centro e
    `delta_immaginaria` alla componente immaginaria; le componenti del nuovo
    centro devono restare nei limiti operativi `[-100, 100]`.
    """
    if not isinstance(vista, SpecificaVistaCanonico):
        raise TypeError("Il parametro 'vista' richiede una SpecificaVistaCanonico.")
    dx = valida_reale_finito(delta_reale, "delta_reale")
    dy = valida_reale_finito(delta_immaginaria, "delta_immaginaria")
    limiti = LIMITI_APPLICATIVI
    nuovo_reale = vista.centro_reale + dx
    nuova_immaginaria = vista.centro_immaginaria + dy
    for nome, valore in (("centro_reale", nuovo_reale), ("centro_immaginaria", nuova_immaginaria)):
        if not (limiti.componente_centro_min <= valore <= limiti.componente_centro_max):
            raise ValueError(
                f"Il campo '{nome}' ({valore}) esce dai limiti "
                f"[{limiti.componente_centro_min}, {limiti.componente_centro_max}]."
            )
    return replace(vista, centro_reale=nuovo_reale, centro_immaginaria=nuova_immaginaria)


if __name__ == "__main__":
    for q in range(2):
        for p in range(4):
            print(f"({p}, {q}) -> {punto_da_pixel(p, q, 4, 2, 0.0, 0.0, 4.0)}")
    print("passo:", passo_campionamento(4, 2, 4.0))
    print("pixel unico:", punto_da_pixel(0, 0, 1, 1, -0.5, 0.25, 3.5))
