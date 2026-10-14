"""Contratti, fixture e oracoli canonici per coordinate, palette e JSON — Unità 20 (L1).

Il modulo definisce le convenzioni e i dati condivisi dai capitoli PY-40, PY-41 e PY-42,
dal laboratorio LAB-PY-U20-B, dalle raccolte di esercizi e dai test del progetto autonomo:

1. Vista del piano complesso, rapporto d'aspetto uniforme `s_y = s_x * H / W`,
   campionamento al centro del pixel e griglie canoniche `4×2` e `1×1`.
2. Adattamento geometrico al rettangolo raster con scala uniforme e inversione verticale.
3. Palette deterministiche (`"binaria"`, `"bande"`, `"gradiente"`) con distinzione esplicita
   fra esito `None` (fuga non rilevata entro il limite) e `indice_fuga == 0`.
4. Schema JSON versione `1` per le quattro famiglie (`"koch"`, `"sierpinski"`,
   `"mandelbrot"`, `"julia"`), limiti matematici e operativi e gestione dei valori
   booleani e non finiti (`NaN`, `Infinity`).

Ambiente: CPython 3.14 sul computer. Il modulo non apre finestre grafiche né esegue
operazioni di I/O all'importazione.
"""

import json
import math
from dataclasses import dataclass
from typing import Any

type ColoreRGB = tuple[int, int, int]
type Punto2D = tuple[float, float]

TOLLERANZA_COORDINATE: float = 1e-12

# ---------------------------------------------------------------------------
# 1. Vista complessa e griglie canoniche 4x2 e 1x1 (PY-40, §7.B)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpecificaVistaCanonico:
    """Parametri di una vista del piano complesso associata a una griglia W x H."""

    larghezza: int
    altezza: int
    centro_reale: float
    centro_immaginaria: float
    ampiezza_orizzontale: float

    @property
    def ampiezza_verticale(self) -> float:
        """Restituisce l'ampiezza verticale `s_y = s_x * H / W` a scala uniforme."""
        return self.ampiezza_orizzontale * (self.altezza / self.larghezza)


VISTA_CANONICA_4X2 = SpecificaVistaCanonico(
    larghezza=4,
    altezza=2,
    centro_reale=0.0,
    centro_immaginaria=0.0,
    ampiezza_orizzontale=4.0,
)

GRIGLIA_CANONICA_4X2: tuple[tuple[complex, ...], ...] = (
    (-1.5 + 0.5j, -0.5 + 0.5j, 0.5 + 0.5j, 1.5 + 0.5j),
    (-1.5 - 0.5j, -0.5 - 0.5j, 0.5 - 0.5j, 1.5 - 0.5j),
)

VISTA_CANONICA_1X1 = SpecificaVistaCanonico(
    larghezza=1,
    altezza=1,
    centro_reale=-0.5,
    centro_immaginaria=0.25,
    ampiezza_orizzontale=3.5,
)

GRIGLIA_CANONICA_1X1: tuple[tuple[complex, ...], ...] = ((-0.5 + 0.25j,),)

VISTA_INIZIALE_MANDELBROT = SpecificaVistaCanonico(
    larghezza=320,
    altezza=240,
    centro_reale=-0.5,
    centro_immaginaria=0.0,
    ampiezza_orizzontale=3.5,
)

VISTA_INIZIALE_JULIA = SpecificaVistaCanonico(
    larghezza=320,
    altezza=240,
    centro_reale=0.0,
    centro_immaginaria=0.0,
    ampiezza_orizzontale=3.5,
)


def _valida_int_non_bool(valore: object, nome: str, minimo: int | None = None) -> int:
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError(f"Il campo '{nome}' richiede un intero non booleano.")
    if minimo is not None and valore < minimo:
        raise ValueError(f"Il campo '{nome}' richiede un valore >= {minimo}.")
    return valore


def _valida_float_finito(valore: object, nome: str) -> float:
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        raise TypeError(f"Il campo '{nome}' richiede un numero reale finito non booleano.")
    risultato = float(valore)
    if not math.isfinite(risultato):
        raise ValueError(f"Il campo '{nome}' non ammette NaN o infinito.")
    return risultato


def campiona_centro_pixel_riferimento(
    colonna_p: int,
    riga_q: int,
    larghezza: int,
    altezza: int,
    centro_reale: float,
    centro_immaginaria: float,
    ampiezza_orizzontale: float,
) -> complex:
    """Oracolo per la formula di campionamento al centro del pixel `(p, q)`.

    Con `0 <= p < W`, `0 <= q < H` e `s_y = s_x * H / W`:
    - `x = x_c - s_x / 2 + (p + 0.5) * s_x / W`
    - `y = y_c + s_y / 2 - (q + 0.5) * s_y / H`
    """
    w = _valida_int_non_bool(larghezza, "larghezza", minimo=1)
    h = _valida_int_non_bool(altezza, "altezza", minimo=1)
    p = _valida_int_non_bool(colonna_p, "colonna_p", minimo=0)
    q = _valida_int_non_bool(riga_q, "riga_q", minimo=0)
    if p >= w:
        raise ValueError(f"Indice di colonna p={p} fuori dall'intervallo 0..{w - 1}.")
    if q >= h:
        raise ValueError(f"Indice di riga q={q} fuori dall'intervallo 0..{h - 1}.")

    x_c = _valida_float_finito(centro_reale, "centro_reale")
    y_c = _valida_float_finito(centro_immaginaria, "centro_immaginaria")
    s_x = _valida_float_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    if s_x <= 0.0:
        raise ValueError(
            "Il campo 'ampiezza_orizzontale' richiede un valore strettamente positivo."
        )

    s_y = s_x * (h / w)
    x = x_c - (s_x / 2.0) + (p + 0.5) * (s_x / w)
    y = y_c + (s_y / 2.0) - (q + 0.5) * (s_y / h)
    return complex(x, y)


def costruisci_griglia_campioni_riferimento(
    vista: SpecificaVistaCanonico,
) -> tuple[tuple[complex, ...], ...]:
    """Costruisce la matrice `H x W` dei punti campionati al centro di ogni pixel."""
    return tuple(
        tuple(
            campiona_centro_pixel_riferimento(
                colonna_p=p,
                riga_q=q,
                larghezza=vista.larghezza,
                altezza=vista.altezza,
                centro_reale=vista.centro_reale,
                centro_immaginaria=vista.centro_immaginaria,
                ampiezza_orizzontale=vista.ampiezza_orizzontale,
            )
            for p in range(vista.larghezza)
        )
        for q in range(vista.altezza)
    )


def trasforma_punti_geometrici_in_pixel_riferimento(
    punti: list[Punto2D] | tuple[Punto2D, ...],
    larghezza: int,
    altezza: int,
    margine_relativo: float = 0.08,
) -> tuple[Punto2D, ...]:
    """Adatta una collezione di punti geometrici 2D a un canvas `W x H` a scala uniforme.

    Conserva le proporzioni (stesso fattore di scala su x e su y), centra il rettangolo
    di contenimento nel canvas e inverte l'asse verticale (y geometrico cresce verso
    l'alto, riga pixel q cresce verso il basso).
    """
    w = _valida_int_non_bool(larghezza, "larghezza", minimo=1)
    h = _valida_int_non_bool(altezza, "altezza", minimo=1)
    margine = _valida_float_finito(margine_relativo, "margine_relativo")
    if not (0.0 <= margine < 0.45):
        raise ValueError("Il margine relativo deve appartenere all'intervallo [0.0, 0.45).")
    if not punti:
        raise ValueError("La sequenza di punti geometrici non può essere vuota.")

    xs = [p[0] for p in punti]
    ys = [p[1] for p in punti]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
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
        for x, y in punti
    )


# ---------------------------------------------------------------------------
# 2. Contratto delle palette deterministiche (PY-40, §7.C)
# ---------------------------------------------------------------------------

PALETTE_AMMESSE: tuple[str, ...] = ("binaria", "bande", "gradiente")

COLORE_INTERNO_BINARIA: ColoreRGB = (15, 28, 46)
COLORE_ESTERNO_BINARIA: ColoreRGB = (232, 241, 245)

COLORE_INTERNO_BANDE: ColoreRGB = (11, 30, 46)
TABELLA_BANDE_FUGA: tuple[ColoreRGB, ...] = (
    (24, 100, 171),
    (28, 126, 214),
    (14, 107, 133),
    (56, 163, 165),
    (128, 206, 179),
    (233, 196, 106),
    (244, 162, 97),
    (231, 111, 81),
)

COLORE_INTERNO_GRADIENTE: ColoreRGB = (11, 30, 46)
COLORE_GRADIENTE_INIZIO: ColoreRGB = (20, 88, 148)
COLORE_GRADIENTE_FINE: ColoreRGB = (246, 213, 110)


def colora_esito_riferimento(
    indice_fuga: int | None,
    limite_iterazioni: int,
    nome_palette: str = "bande",
) -> ColoreRGB:
    """Restituisce la tripla RGB `(r, g, b)` deterministica associata a `indice_fuga`.

    Regola di contratto:
    - `indice_fuga is None` riceve il colore dedicato ai punti la cui fuga non è stata
      rilevata entro `limite_iterazioni`;
    - `indice_fuga == 0` è un intero valido (`0 is not None`) e riceve il primo colore
      di fuga, distinto dal colore riservato a `None`.
    """
    n_max = _valida_int_non_bool(limite_iterazioni, "limite_iterazioni", minimo=1)
    if nome_palette not in PALETTE_AMMESSE:
        raise ValueError(f"Palette '{nome_palette}' non riconosciuta; ammesse: {PALETTE_AMMESSE}.")

    if indice_fuga is None:
        if nome_palette == "binaria":
            return COLORE_INTERNO_BINARIA
        if nome_palette == "bande":
            return COLORE_INTERNO_BANDE
        return COLORE_INTERNO_GRADIENTE

    indice = _valida_int_non_bool(indice_fuga, "indice_fuga", minimo=0)
    if indice > n_max:
        raise ValueError(
            f"L'indice di fuga ({indice}) non può superare limite_iterazioni ({n_max})."
        )

    if nome_palette == "binaria":
        return COLORE_ESTERNO_BINARIA
    if nome_palette == "bande":
        return TABELLA_BANDE_FUGA[indice % len(TABELLA_BANDE_FUGA)]

    frazione = indice / n_max
    r = round(
        COLORE_GRADIENTE_INIZIO[0]
        + frazione * (COLORE_GRADIENTE_FINE[0] - COLORE_GRADIENTE_INIZIO[0])
    )
    g = round(
        COLORE_GRADIENTE_INIZIO[1]
        + frazione * (COLORE_GRADIENTE_FINE[1] - COLORE_GRADIENTE_INIZIO[1])
    )
    b = round(
        COLORE_GRADIENTE_INIZIO[2]
        + frazione * (COLORE_GRADIENTE_FINE[2] - COLORE_GRADIENTE_INIZIO[2])
    )
    return (r, g, b)


# ---------------------------------------------------------------------------
# 3. Schema JSON versione 1 e limiti matematici/operativi (PY-42, §9.3–9.4)
# ---------------------------------------------------------------------------

VERSIONE_SCHEMA_ATTUALE: int = 1
FAMIGLIE_FRATTALI_AMMESSE: tuple[str, ...] = ("koch", "sierpinski", "mandelbrot", "julia")
VARIANTI_KOCH_AMMESSE: tuple[str, ...] = ("curva", "fiocco")
STILI_SIERPINSKI_AMMESSI: tuple[str, ...] = ("pieno", "contorno")


@dataclass(frozen=True)
class LimitiApplicativiU20:
    """Limiti operativi dichiarati per l'applicazione didattica U20 (§9.4)."""

    larghezza_min: int = 1
    larghezza_max: int = 800
    larghezza_default: int = 320
    altezza_min: int = 1
    altezza_max: int = 600
    altezza_default: int = 240
    iterazioni_min: int = 1
    iterazioni_max: int = 500
    iterazioni_default: int = 100
    budget_aggiornamenti_max: int = 100_000_000
    livello_koch_min: int = 0
    livello_koch_max: int = 6
    livello_koch_default: int = 3
    livello_sierpinski_min: int = 0
    livello_sierpinski_max: int = 7
    livello_sierpinski_default: int = 4
    componente_julia_min: float = -10.0
    componente_julia_max: float = 10.0
    ampiezza_vista_min: float = 1e-6
    ampiezza_vista_max: float = 20.0
    componente_centro_min: float = -100.0
    componente_centro_max: float = 100.0
    lato_iniziale_min: float = 0.1
    lato_iniziale_max: float = 20.0


LIMITI_APPLICATIVI = LimitiApplicativiU20()

CONFIGURAZIONI_JSON_CANONICHE: dict[str, dict[str, Any]] = {
    "koch": {
        "versione_schema": 1,
        "tipo_frattale": "koch",
        "immagine": {
            "larghezza": 320,
            "altezza": 240,
            "palette": "binaria",
        },
        "vista": {
            "centro": {"reale": 1.5, "immaginaria": 0.8660254037844386},
            "ampiezza_orizzontale": 4.0,
        },
        "parametri": {
            "livello": 3,
            "variante": "fiocco",
            "lato_iniziale": 3.0,
        },
    },
    "sierpinski": {
        "versione_schema": 1,
        "tipo_frattale": "sierpinski",
        "immagine": {
            "larghezza": 320,
            "altezza": 240,
            "palette": "binaria",
        },
        "vista": {
            "centro": {"reale": 2.0, "immaginaria": 1.7320508075688772},
            "ampiezza_orizzontale": 4.8,
        },
        "parametri": {
            "livello": 4,
            "stile": "pieno",
            "lato_iniziale": 4.0,
        },
    },
    "mandelbrot": {
        "versione_schema": 1,
        "tipo_frattale": "mandelbrot",
        "immagine": {
            "larghezza": 320,
            "altezza": 240,
            "palette": "bande",
        },
        "vista": {
            "centro": {"reale": -0.5, "immaginaria": 0.0},
            "ampiezza_orizzontale": 3.5,
        },
        "parametri": {
            "limite_iterazioni": 100,
        },
    },
    "julia": {
        "versione_schema": 1,
        "tipo_frattale": "julia",
        "immagine": {
            "larghezza": 320,
            "altezza": 240,
            "palette": "bande",
        },
        "vista": {
            "centro": {"reale": 0.0, "immaginaria": 0.0},
            "ampiezza_orizzontale": 3.5,
        },
        "parametri": {
            "limite_iterazioni": 100,
            "c": {"reale": -0.8, "immaginaria": 0.156},
        },
    },
}


def _valida_oggetto_complesso(
    valore: object,
    nome_campo: str,
    minimo: float,
    massimo: float,
) -> complex:
    if not isinstance(valore, dict):
        raise TypeError(
            f"Il campo '{nome_campo}' deve essere un oggetto con 'reale' e 'immaginaria'."
        )
    if set(valore.keys()) != {"reale", "immaginaria"}:
        raise ValueError(
            f"Il campo '{nome_campo}' deve contenere esattamente le chiavi 'reale' e 'immaginaria'."
        )
    reale = _valida_float_finito(valore["reale"], f"{nome_campo}.reale")
    immaginaria = _valida_float_finito(valore["immaginaria"], f"{nome_campo}.immaginaria")
    if not (minimo <= reale <= massimo) or not (minimo <= immaginaria <= massimo):
        raise ValueError(
            f"Le componenti di '{nome_campo}' devono appartenere "
            f"all'intervallo [{minimo}, {massimo}]."
        )
    return complex(reale, immaginaria)


def valida_dizionario_configurazione_riferimento(
    dati: object,
    limiti: LimitiApplicativiU20 = LIMITI_APPLICATIVI,
) -> dict[str, Any]:
    """Oracolo di validazione per un documento JSON di configurazione (schema versione 1).

    Controlla presenza e tipo delle chiavi, rifiuta valori booleani nei campi numerici,
    rifiuta `NaN`/`Infinity`, verifica i limiti matematici e operativi (incluso il budget
    complessivo `W * H * N <= 100_000_000` e il dominio `[-10, 10]` per il parametro `c`
    di Julia, che include `c = -6`).
    """
    if not isinstance(dati, dict):
        raise TypeError("Il documento di configurazione deve essere un oggetto JSON (dict).")

    chiavi_attese = {"versione_schema", "tipo_frattale", "immagine", "vista", "parametri"}
    mancanti = chiavi_attese - set(dati.keys())
    if mancanti:
        raise ValueError(f"Chiavi obbligatorie mancanti nella configurazione: {sorted(mancanti)}.")

    versione = _valida_int_non_bool(dati["versione_schema"], "versione_schema")
    if versione != VERSIONE_SCHEMA_ATTUALE:
        raise ValueError(
            f"Versione schema {versione} non supportata; attesa {VERSIONE_SCHEMA_ATTUALE}."
        )

    tipo = dati["tipo_frattale"]
    if not isinstance(tipo, str) or tipo not in FAMIGLIE_FRATTALI_AMMESSE:
        raise ValueError(
            f"Tipo frattale '{tipo}' non supportato; ammessi: {FAMIGLIE_FRATTALI_AMMESSE}."
        )

    immagine = dati["immagine"]
    if not isinstance(immagine, dict):
        raise TypeError("La sezione 'immagine' deve essere un oggetto JSON.")
    if {"larghezza", "altezza", "palette"} - set(immagine.keys()):
        raise ValueError("La sezione 'immagine' richiede 'larghezza', 'altezza' e 'palette'.")

    larghezza = _valida_int_non_bool(immagine["larghezza"], "immagine.larghezza")
    altezza = _valida_int_non_bool(immagine["altezza"], "immagine.altezza")
    if not (limiti.larghezza_min <= larghezza <= limiti.larghezza_max):
        raise ValueError(
            f"Larghezza {larghezza} fuori dai limiti "
            f"[{limiti.larghezza_min}, {limiti.larghezza_max}]."
        )
    if not (limiti.altezza_min <= altezza <= limiti.altezza_max):
        raise ValueError(
            f"Altezza {altezza} fuori dai limiti [{limiti.altezza_min}, {limiti.altezza_max}]."
        )

    palette = immagine["palette"]
    if not isinstance(palette, str) or palette not in PALETTE_AMMESSE:
        raise ValueError(f"Palette '{palette}' non valida; ammesse: {PALETTE_AMMESSE}.")

    vista = dati["vista"]
    if not isinstance(vista, dict):
        raise TypeError("La sezione 'vista' deve essere un oggetto JSON.")
    if {"centro", "ampiezza_orizzontale"} - set(vista.keys()):
        raise ValueError("La sezione 'vista' richiede 'centro' e 'ampiezza_orizzontale'.")

    _valida_oggetto_complesso(
        vista["centro"],
        "vista.centro",
        limiti.componente_centro_min,
        limiti.componente_centro_max,
    )
    ampiezza = _valida_float_finito(vista["ampiezza_orizzontale"], "vista.ampiezza_orizzontale")
    if not (limiti.ampiezza_vista_min <= ampiezza <= limiti.ampiezza_vista_max):
        raise ValueError(
            f"Ampiezza orizzontale {ampiezza} fuori dai limiti "
            f"[{limiti.ampiezza_vista_min}, {limiti.ampiezza_vista_max}]."
        )

    parametri = dati["parametri"]
    if not isinstance(parametri, dict):
        raise TypeError("La sezione 'parametri' deve essere un oggetto JSON.")

    if tipo in ("mandelbrot", "julia"):
        if "limite_iterazioni" not in parametri:
            raise ValueError("Il campo 'parametri.limite_iterazioni' è obbligatorio.")
        n_max = _valida_int_non_bool(
            parametri["limite_iterazioni"],
            "parametri.limite_iterazioni",
        )
        if not (limiti.iterazioni_min <= n_max <= limiti.iterazioni_max):
            raise ValueError(
                f"Limite iterazioni {n_max} fuori dai limiti "
                f"[{limiti.iterazioni_min}, {limiti.iterazioni_max}]."
            )
        budget_stimato = larghezza * altezza * n_max
        if budget_stimato > limiti.budget_aggiornamenti_max:
            raise ValueError(
                f"Il budget stimato W*H*N = {budget_stimato} supera il limite operativo "
                f"di {limiti.budget_aggiornamenti_max} aggiornamenti; ridurre risoluzione o N."
            )
        if tipo == "julia":
            if "c" not in parametri:
                raise ValueError(
                    "Per la famiglia 'julia' è obbligatorio il parametro 'parametri.c'."
                )
            _valida_oggetto_complesso(
                parametri["c"],
                "parametri.c",
                limiti.componente_julia_min,
                limiti.componente_julia_max,
            )
    elif tipo == "koch":
        if {"livello", "variante", "lato_iniziale"} - set(parametri.keys()):
            raise ValueError("Per 'koch' sono richiesti 'livello', 'variante' e 'lato_iniziale'.")
        livello = _valida_int_non_bool(parametri["livello"], "parametri.livello")
        if not (limiti.livello_koch_min <= livello <= limiti.livello_koch_max):
            raise ValueError(
                f"Livello di Koch {livello} fuori dai limiti "
                f"[{limiti.livello_koch_min}, {limiti.livello_koch_max}]."
            )
        if parametri["variante"] not in VARIANTI_KOCH_AMMESSE:
            raise ValueError(f"Variante di Koch non valida; ammesse: {VARIANTI_KOCH_AMMESSE}.")
        lato = _valida_float_finito(parametri["lato_iniziale"], "parametri.lato_iniziale")
        if not (limiti.lato_iniziale_min <= lato <= limiti.lato_iniziale_max):
            raise ValueError("Lato iniziale di Koch fuori dai limiti operativi.")
    elif tipo == "sierpinski":
        if {"livello", "stile", "lato_iniziale"} - set(parametri.keys()):
            raise ValueError(
                "Per 'sierpinski' sono richiesti 'livello', 'stile' e 'lato_iniziale'."
            )
        livello = _valida_int_non_bool(parametri["livello"], "parametri.livello")
        if not (limiti.livello_sierpinski_min <= livello <= limiti.livello_sierpinski_max):
            raise ValueError(
                f"Livello di Sierpiński {livello} fuori dai limiti "
                f"[{limiti.livello_sierpinski_min}, {limiti.livello_sierpinski_max}]."
            )
        if parametri["stile"] not in STILI_SIERPINSKI_AMMESSI:
            raise ValueError(
                f"Stile di Sierpiński non valido; ammessi: {STILI_SIERPINSKI_AMMESSI}."
            )
        lato = _valida_float_finito(parametri["lato_iniziale"], "parametri.lato_iniziale")
        if not (limiti.lato_iniziale_min <= lato <= limiti.lato_iniziale_max):
            raise ValueError("Lato iniziale di Sierpiński fuori dai limiti operativi.")

    return dati


def serializza_configurazione_json_riferimento(dati: dict[str, Any]) -> str:
    """Valida e serializza in JSON standard (UTF-8, `allow_nan=False`) la configurazione."""
    valida_dizionario_configurazione_riferimento(dati)
    return json.dumps(dati, indent=2, ensure_ascii=False, allow_nan=False)


def deserializza_configurazione_json_riferimento(testo_json: str) -> dict[str, Any]:
    """Deserializza e valida un testo JSON rifiutando costanti non standard (`NaN`, `Infinity`)."""

    def _rifiuta_costanti_non_finite(costante: str) -> Any:
        raise ValueError(f"Costante JSON non finita non ammessa: {costante}.")

    dati = json.loads(testo_json, parse_constant=_rifiuta_costanti_non_finite)
    return valida_dizionario_configurazione_riferimento(dati)
