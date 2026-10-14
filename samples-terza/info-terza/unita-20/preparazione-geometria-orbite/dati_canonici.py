"""Contratti, fixture e oracoli canonici per geometria, complessi e fuga — Unità 20 (L1).

Il modulo definisce i dati stabili e gli oracoli indipendenti condivisi dai capitoli
PY-37, PY-38 e PY-39, dal laboratorio LAB-PY-U20-A, dalle raccolte di esercizi e dai
test pubblici del progetto autonomo:

1. Rappresentazioni geometriche (`Punto2D`, `Segmento2D`, `Triangolo2D`), vertici e
   segmenti dei livelli piccoli di Koch e Sierpiński, orientamento orario del fiocco
   di Koch per ottenere punte rivolte verso l'esterno e formule esatte dei conteggi.
2. Casi canonici sulle operazioni dei numeri complessi (`a + bi`) e prefissi esatti
   delle orbite quadratiche `z_{n+1} = z_n^2 + c`.
3. Contratto del kernel di fuga con risultato `EsitoFugaCanonico` (`indice_fuga: int | None`,
   `aggiornamenti_eseguiti: int`, `valore_finale: complex`), i dodici casi discriminanti
   `M-01`–`M-07` e `J-01`–`J-05` e un oracolo indipendente calcolato esclusivamente
   tramite coppie di numeri reali `(x, y)`.

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O né apre
finestre grafiche all'importazione.
"""

import math
from dataclasses import dataclass

type Punto2D = tuple[float, float]
type Segmento2D = tuple[Punto2D, Punto2D]
type Triangolo2D = tuple[Punto2D, Punto2D, Punto2D]

TOLLERANZA_GEOMETRIA: float = 1e-9
TOLLERANZA_COMPLESSI: float = 1e-12

# ---------------------------------------------------------------------------
# 1. Contratti e casi canonici per i frattali geometrici (PY-37, §4)
# ---------------------------------------------------------------------------

COSENO_60: float = 0.5
SENO_60: float = math.sqrt(3.0) / 2.0

LATO_KOCH_CANONICO: float = 3.0
SEGMENTO_KOCH_BASE: Segmento2D = ((0.0, 0.0), (3.0, 0.0))

VERTICI_KOCH_LIVELLO_1: tuple[Punto2D, ...] = (
    (0.0, 0.0),
    (1.0, 0.0),
    (1.5, SENO_60),
    (2.0, 0.0),
    (3.0, 0.0),
)

SEGMENTI_KOCH_LIVELLO_1: tuple[Segmento2D, ...] = (
    ((0.0, 0.0), (1.0, 0.0)),
    ((1.0, 0.0), (1.5, SENO_60)),
    ((1.5, SENO_60), (2.0, 0.0)),
    ((2.0, 0.0), (3.0, 0.0)),
)

# Nel piano cartesiano con asse y rivolto verso l'alto, la rotazione di +60 gradi
# del terzo centrale sposta la punta a sinistra del segmento orientato A -> B.
# Per ottenere le punte del fiocco di Koch rivolte verso l'esterno del triangolo
# equilatero iniziale, il contorno va quindi percorso in senso orario:
# V0 (in basso a sinistra) -> V1 (vertice superiore) -> V2 (in basso a destra) -> V0.
VERTICI_FIOCCO_ORARIO: Triangolo2D = (
    (0.0, 0.0),
    (1.5, 3.0 * SENO_60),
    (3.0, 0.0),
)

LATI_INIZIALI_FIOCCO_ORARIO: tuple[Segmento2D, Segmento2D, Segmento2D] = (
    (VERTICI_FIOCCO_ORARIO[0], VERTICI_FIOCCO_ORARIO[1]),
    (VERTICI_FIOCCO_ORARIO[1], VERTICI_FIOCCO_ORARIO[2]),
    (VERTICI_FIOCCO_ORARIO[2], VERTICI_FIOCCO_ORARIO[0]),
)

BARICENTRO_FIOCCO_BASE: Punto2D = (1.5, SENO_60)
APOTEMA_FIOCCO_BASE: float = SENO_60
RAGGIO_CIRCOSCRITTO_FIOCCO_BASE: float = 2.0 * SENO_60

# Punte prodotte al livello 1 sui tre lati del fiocco percorso in senso orario:
# ciascuna punta si trova a distanza sqrt(3) (= 2 * apotema, pari al raggio
# circoscritto del triangolo iniziale) dal baricentro (> apotema = sqrt(3)/2).
PUNTE_ESTERNE_FIOCCO_LIVELLO_1: tuple[Punto2D, Punto2D, Punto2D] = (
    (0.0, 2.0 * SENO_60),
    (3.0, 2.0 * SENO_60),
    (1.5, -SENO_60),
)

LATO_SIERPINSKI_CANONICO: float = 4.0
TRIANGOLO_SIERPINSKI_BASE: Triangolo2D = (
    (0.0, 0.0),
    (4.0, 0.0),
    (2.0, 4.0 * SENO_60),
)

TRIANGOLI_SIERPINSKI_LIVELLO_1: tuple[Triangolo2D, Triangolo2D, Triangolo2D] = (
    ((0.0, 0.0), (2.0, 0.0), (1.0, 2.0 * SENO_60)),
    ((2.0, 0.0), (4.0, 0.0), (3.0, 2.0 * SENO_60)),
    ((1.0, 2.0 * SENO_60), (3.0, 2.0 * SENO_60), (2.0, 4.0 * SENO_60)),
)

# Il triangolo centrale individuato dai tre punti medi viene escluso al livello 1.
TRIANGOLO_CENTRALE_ESCLUSO_LIVELLO_1: Triangolo2D = (
    (2.0, 0.0),
    (3.0, 2.0 * SENO_60),
    (1.0, 2.0 * SENO_60),
)

LIVELLO_DEFAULT_KOCH: int = 3
LIVELLO_MAX_APPLICATIVO_KOCH: int = 6
LIVELLO_DEFAULT_SIERPINSKI: int = 4
LIVELLO_MAX_APPLICATIVO_SIERPINSKI: int = 7

CONTEGGI_SEGMENTI_KOCH_CURVA: dict[int, int] = {livello: 4**livello for livello in range(7)}
CONTEGGI_SEGMENTI_KOCH_FIOCCO: dict[int, int] = {livello: 3 * (4**livello) for livello in range(7)}
CONTEGGI_TRIANGOLI_SIERPINSKI: dict[int, int] = {livello: 3**livello for livello in range(8)}


def valida_intero_non_booleano(valore: object, nome_parametro: str, minimo: int = 0) -> int:
    """Verifica che `valore` sia un intero non booleano maggiore o uguale a `minimo`."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError(f"Il parametro '{nome_parametro}' richiede un int non booleano.")
    if valore < minimo:
        raise ValueError(f"Il parametro '{nome_parametro}' richiede un valore >= {minimo}.")
    return valore


def valida_reale_finito(valore: object, nome_parametro: str) -> float:
    """Verifica che `valore` sia un numero reale finito non booleano."""
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        raise TypeError(f"Il parametro '{nome_parametro}' richiede un numero reale finito.")
    risultato = float(valore)
    if not math.isfinite(risultato):
        raise ValueError(f"Il parametro '{nome_parametro}' richiede un valore finito.")
    return risultato


def numero_segmenti_koch_curva(livello: int) -> int:
    """Restituisce il numero esatto `4**d` di segmenti della curva di Koch al livello `d`."""
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return 4**d


def numero_segmenti_koch_fiocco(livello: int) -> int:
    """Restituisce il numero esatto `3 * 4**d` di segmenti del fiocco di Koch al livello `d`."""
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return 3 * (4**d)


def lunghezza_segmento_koch(lato_iniziale: float, livello: int) -> float:
    """Restituisce la lunghezza `L / 3**d` di ciascun segmento finale di Koch."""
    lato = valida_reale_finito(lato_iniziale, "lato_iniziale")
    if lato <= 0.0:
        raise ValueError("Il parametro 'lato_iniziale' richiede un valore positivo.")
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return lato / (3.0**d)


def lunghezza_totale_koch_curva(lato_iniziale: float, livello: int) -> float:
    """Restituisce la lunghezza totale `L * (4/3)**d` della curva di Koch al livello `d`."""
    lato = valida_reale_finito(lato_iniziale, "lato_iniziale")
    if lato <= 0.0:
        raise ValueError("Il parametro 'lato_iniziale' richiede un valore positivo.")
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return lato * ((4.0 / 3.0) ** d)


def numero_triangoli_sierpinski(livello: int) -> int:
    """Restituisce il numero esatto `3**d` di triangoli pieni di Sierpiński al livello `d`."""
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return 3**d


def lato_triangolo_sierpinski(lato_iniziale: float, livello: int) -> float:
    """Restituisce la lunghezza `L / 2**d` del lato di ciascun triangolo finale."""
    lato = valida_reale_finito(lato_iniziale, "lato_iniziale")
    if lato <= 0.0:
        raise ValueError("Il parametro 'lato_iniziale' richiede un valore positivo.")
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return lato / (2.0**d)


def area_totale_sierpinski(area_iniziale: float, livello: int) -> float:
    """Restituisce l'area complessiva `A * (3/4)**d` dei triangoli di Sierpiński al livello `d`."""
    area = valida_reale_finito(area_iniziale, "area_iniziale")
    if area <= 0.0:
        raise ValueError("Il parametro 'area_iniziale' richiede un valore positivo.")
    d = valida_intero_non_booleano(livello, "livello", minimo=0)
    return area * ((3.0 / 4.0) ** d)


def suddividi_segmento_koch_riferimento(segmento: Segmento2D) -> tuple[Segmento2D, ...]:
    """Oracolo geometrico di livello 1: sostituisce un segmento con i 4 segmenti di Koch."""
    (x_a, y_a), (x_b, y_b) = segmento
    dx = (x_b - x_a) / 3.0
    dy = (y_b - y_a) / 3.0
    p_1: Punto2D = (x_a + dx, y_a + dy)
    p_2: Punto2D = (x_a + 2.0 * dx, y_a + 2.0 * dy)
    punta: Punto2D = (
        p_1[0] + dx * COSENO_60 - dy * SENO_60,
        p_1[1] + dx * SENO_60 + dy * COSENO_60,
    )
    return (
        ((x_a, y_a), p_1),
        (p_1, punta),
        (punta, p_2),
        (p_2, (x_b, y_b)),
    )


# ---------------------------------------------------------------------------
# 2. Casi canonici sui numeri complessi e sulle orbite quadratiche (PY-38, §5)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CasoOperazioneComplessa:
    """Caso canonico per verificare componenti, modulo o operazioni su `complex`."""

    nome: str
    z_1: complex
    z_2: complex | None
    risultato_atteso: complex | float
    descrizione: str


CASI_OPERAZIONI_COMPLESSE: tuple[CasoOperazioneComplessa, ...] = (
    CasoOperazioneComplessa(
        nome="modulo_3_piu_4j",
        z_1=3.0 + 4.0j,
        z_2=None,
        risultato_atteso=5.0,
        descrizione="Modulo esatto |3 + 4i| = sqrt(9 + 16) = 5.",
    ),
    CasoOperazioneComplessa(
        nome="somma_1_piu_2j_e_3_meno_j",
        z_1=1.0 + 2.0j,
        z_2=3.0 - 1.0j,
        risultato_atteso=4.0 + 1.0j,
        descrizione="Somma per componenti: (1 + 2i) + (3 - i) = 4 + i.",
    ),
    CasoOperazioneComplessa(
        nome="sottrazione_3_meno_j_e_1_piu_2j",
        z_1=3.0 - 1.0j,
        z_2=1.0 + 2.0j,
        risultato_atteso=2.0 - 3.0j,
        descrizione="Sottrazione per componenti: (3 - i) - (1 + 2i) = 2 - 3i.",
    ),
    CasoOperazioneComplessa(
        nome="prodotto_1_piu_2j_per_3_meno_j",
        z_1=1.0 + 2.0j,
        z_2=3.0 - 1.0j,
        risultato_atteso=5.0 + 5.0j,
        descrizione="Prodotto: (1 + 2i)(3 - i) = (3 + 2) + (-1 + 6)i = 5 + 5i.",
    ),
    CasoOperazioneComplessa(
        nome="quadrato_1_piu_2j",
        z_1=1.0 + 2.0j,
        z_2=None,
        risultato_atteso=-3.0 + 4.0j,
        descrizione="Quadrato fondamentale: (1 + 2i)^2 = (1 - 4) + 2(1)(2)i = -3 + 4i.",
    ),
)

TRACCE_ORBITE_CANONICHE: dict[str, tuple[complex, ...]] = {
    "c_zero_da_zero": (0.0j, 0.0j, 0.0j, 0.0j, 0.0j),
    "c_meno_uno_da_zero": (0.0j, -1.0 + 0.0j, 0.0j, -1.0 + 0.0j, 0.0j),
    "c_uno_da_zero": (0.0j, 1.0 + 0.0j, 2.0 + 0.0j, 5.0 + 0.0j, 26.0 + 0.0j),
    "c_i_da_zero": (0.0j, 1.0j, -1.0 + 1.0j, -1.0j, -1.0 + 1.0j),
}


# ---------------------------------------------------------------------------
# 3. Contratto del kernel di fuga e i 12 casi canonici M/J (PY-39, §6.D–F)
# ---------------------------------------------------------------------------

RAGGIO_FUGA_MANDELBROT: float = 2.0


def raggio_fuga_julia(c: complex) -> float:
    """Restituisce il raggio di fuga sicuro `R = max(2.0, abs(c))` per l'insieme di Julia."""
    if isinstance(c, bool) or not isinstance(c, (int, float, complex)):
        raise TypeError("Il parametro 'c' richiede un numero complesso o reale finito.")
    c_complesso = complex(c)
    if not (math.isfinite(c_complesso.real) and math.isfinite(c_complesso.imag)):
        raise ValueError("Le componenti del parametro 'c' devono essere finite.")
    return max(2.0, abs(c_complesso))


@dataclass(frozen=True)
class EsitoFugaCanonico:
    """Esito della classificazione di un punto sotto l'iterazione quadratica `z^2 + c`.

    - `indice_fuga`: intero `0 <= n <= limite_iterazioni` se il modulo supera strettamente
      `raggio_fuga` al passo `n` (`0` indica superamento già su `z_0` con zero aggiornamenti);
      `None` se dopo tutti gli `N = limite_iterazioni` aggiornamenti il modulo non ha mai
      superato strettamente `raggio_fuga`.
    - `aggiornamenti_eseguiti`: numero di valutazioni effettive di `z = z * z + c` (`0..N`).
    - `valore_finale`: ultimo valore di `z` calcolato al momento dell'arresto.
    """

    indice_fuga: int | None
    aggiornamenti_eseguiti: int
    valore_finale: complex


@dataclass(frozen=True)
class CasoFugaCanonico:
    """Scheda completa di uno dei dodici casi canonici del piano U20 (§6.F)."""

    codice: str
    famiglia: str
    z_iniziale: complex
    c: complex
    limite_iterazioni: int
    raggio_fuga: float
    indice_fuga_atteso: int | None
    aggiornamenti_attesi: int
    valore_finale_atteso: complex
    prefisso_orbita: tuple[complex, ...]
    scopo_didattico: str


CASI_FUGA_CANONICI: tuple[CasoFugaCanonico, ...] = (
    CasoFugaCanonico(
        codice="M-01",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=0.0j,
        prefisso_orbita=(0.0j, 0.0j, 0.0j, 0.0j),
        scopo_didattico="Punto fisso nell'origine: orbita costantemente nulla.",
    ),
    CasoFugaCanonico(
        codice="M-02",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=-1.0 + 0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=0.0j,
        prefisso_orbita=(0.0j, -1.0 + 0.0j, 0.0j, -1.0 + 0.0j),
        scopo_didattico="Ciclo periodico di periodo 2 tra 0 e -1.",
    ),
    CasoFugaCanonico(
        codice="M-03",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=-2.0 + 0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=2.0 + 0.0j,
        prefisso_orbita=(0.0j, -2.0 + 0.0j, 2.0 + 0.0j, 2.0 + 0.0j),
        scopo_didattico="Estremo sinistro su |z| = 2: discrimina il confronto stretto > da >=.",
    ),
    CasoFugaCanonico(
        codice="M-04",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=1.0 + 0.0j,
        limite_iterazioni=2,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=2,
        valore_finale_atteso=2.0 + 0.0j,
        prefisso_orbita=(0.0j, 1.0 + 0.0j, 2.0 + 0.0j),
        scopo_didattico="Con budget N=2 il modulo finale vale 2 <= 2: fuga non ancora rilevata.",
    ),
    CasoFugaCanonico(
        codice="M-05",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=1.0 + 0.0j,
        limite_iterazioni=3,
        raggio_fuga=2.0,
        indice_fuga_atteso=3,
        aggiornamenti_attesi=3,
        valore_finale_atteso=5.0 + 0.0j,
        prefisso_orbita=(0.0j, 1.0 + 0.0j, 2.0 + 0.0j, 5.0 + 0.0j),
        scopo_didattico="Fuga esattamente sull'ultimo passo N=3 (distinta da indice_fuga=None).",
    ),
    CasoFugaCanonico(
        codice="M-06",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=2.0 + 0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=2,
        aggiornamenti_attesi=2,
        valore_finale_atteso=6.0 + 0.0j,
        prefisso_orbita=(0.0j, 2.0 + 0.0j, 6.0 + 0.0j),
        scopo_didattico="Al passo 1 vale 2 <= 2; al passo 2 vale 6 > 2 con arresto immediato.",
    ),
    CasoFugaCanonico(
        codice="M-07",
        famiglia="mandelbrot",
        z_iniziale=0.0j,
        c=1.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=-1.0 + 1.0j,
        prefisso_orbita=(0.0j, 1.0j, -1.0 + 1.0j, -1.0j, -1.0 + 1.0j),
        scopo_didattico="Orbita preperiodica nel piano complesso con |z_n| <= sqrt(2) <= 2.",
    ),
    CasoFugaCanonico(
        codice="J-01",
        famiglia="julia",
        z_iniziale=1.0 + 0.0j,
        c=0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=1.0 + 0.0j,
        prefisso_orbita=(1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j),
        scopo_didattico="Punto fisso z=1 sulla frontiera J_0 del disco unitario pieno K_0.",
    ),
    CasoFugaCanonico(
        codice="J-02",
        famiglia="julia",
        z_iniziale=1.0j,
        c=0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=1.0 + 0.0j,
        prefisso_orbita=(1.0j, -1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j),
        scopo_didattico="Punto sulla circonferenza unitaria |z|=1 che cade sul punto fisso 1.",
    ),
    CasoFugaCanonico(
        codice="J-03",
        famiglia="julia",
        z_iniziale=2.0 + 0.0j,
        c=0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=1,
        aggiornamenti_attesi=1,
        valore_finale_atteso=4.0 + 0.0j,
        prefisso_orbita=(2.0 + 0.0j, 4.0 + 0.0j),
        scopo_didattico="Al passo 0 vale |z_0|=2 <= 2; al passo 1 vale |z_1|=4 > 2.",
    ),
    CasoFugaCanonico(
        codice="J-04",
        famiglia="julia",
        z_iniziale=3.0 + 0.0j,
        c=0.0j,
        limite_iterazioni=10,
        raggio_fuga=2.0,
        indice_fuga_atteso=0,
        aggiornamenti_attesi=0,
        valore_finale_atteso=3.0 + 0.0j,
        prefisso_orbita=(3.0 + 0.0j,),
        scopo_didattico="Fuga già al controllo iniziale su z_0 con indice 0 e zero aggiornamenti.",
    ),
    CasoFugaCanonico(
        codice="J-05",
        famiglia="julia",
        z_iniziale=3.0 + 0.0j,
        c=-6.0 + 0.0j,
        limite_iterazioni=10,
        raggio_fuga=6.0,
        indice_fuga_atteso=None,
        aggiornamenti_attesi=10,
        valore_finale_atteso=3.0 + 0.0j,
        prefisso_orbita=(3.0 + 0.0j, 3.0 + 0.0j, 3.0 + 0.0j),
        scopo_didattico=(
            "Caso discriminante del raggio R=max(2,|c|)=6: z_0=3 è punto fisso (3^2-6=3)."
        ),
    ),
)

CASI_FUGA_PER_CODICE: dict[str, CasoFugaCanonico] = {
    caso.codice: caso for caso in CASI_FUGA_CANONICI
}


def oracolo_fuga_componenti_reali(
    x_iniziale: float,
    y_iniziale: float,
    c_reale: float,
    c_immaginaria: float,
    limite_iterazioni: int,
    raggio_fuga: float,
) -> EsitoFugaCanonico:
    """Oracolo indipendente per il tempo di fuga basato solo su aritmetica reale `(x, y)`.

    Usa l'aggiornamento simultaneo delle componenti `x_nuovo = x^2 - y^2 + c_x` e
    `y_nuovo = 2*x*y + c_y` e il confronto stretto sul quadrato del modulo
    `x^2 + y^2 > raggio_fuga^2`. Serve a verificare in modo indipendente sia i dodici
    casi canonici sia i kernel su `complex` che verranno introdotti in L4.
    """
    x = valida_reale_finito(x_iniziale, "x_iniziale")
    y = valida_reale_finito(y_iniziale, "y_iniziale")
    cx = valida_reale_finito(c_reale, "c_reale")
    cy = valida_reale_finito(c_immaginaria, "c_immaginaria")
    n_max = valida_intero_non_booleano(limite_iterazioni, "limite_iterazioni", minimo=1)
    raggio = valida_reale_finito(raggio_fuga, "raggio_fuga")
    if raggio <= 0.0:
        raise ValueError("Il parametro 'raggio_fuga' richiede un valore positivo.")

    soglia_quadrata = raggio * raggio
    if x * x + y * y > soglia_quadrata:
        return EsitoFugaCanonico(
            indice_fuga=0,
            aggiornamenti_eseguiti=0,
            valore_finale=complex(x, y),
        )

    for passo in range(1, n_max + 1):
        x_nuovo = x * x - y * y + cx
        y_nuovo = 2.0 * x * y + cy
        x, y = x_nuovo, y_nuovo
        if x * x + y * y > soglia_quadrata:
            return EsitoFugaCanonico(
                indice_fuga=passo,
                aggiornamenti_eseguiti=passo,
                valore_finale=complex(x, y),
            )

    return EsitoFugaCanonico(
        indice_fuga=None,
        aggiornamenti_eseguiti=n_max,
        valore_finale=complex(x, y),
    )
