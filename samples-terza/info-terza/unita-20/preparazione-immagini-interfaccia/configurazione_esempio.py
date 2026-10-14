"""Modello a componenti, persistenza JSON e costi — Unità 20 (L7).

Il modulo implementa gli esempi preparatori del capitolo PY-42
(*Modello, persistenza, test e costi*):

- oggetti di valore immutabili (`VistaComplessa`, `ParametriImmagine`,
  `ParametriMandelbrot`, `ParametriJulia`, `ParametriKoch`,
  `ParametriSierpinski`) con validazione nel costruttore;
- due contratti di dominio come `Protocol`: `ClassificatoreQuadratico`
  (classifica un punto in `int | None`) e `ProduttoreGeometrico`
  (produce gli elementi finiti di una costruzione), con due
  implementazioni sostituibili ciascuno;
- il contratto `Colorazione` con tre strategie deterministiche
  (`Binaria`, `Bande`, `Gradiente`) che colorano la stessa matrice senza
  ricalcolare le orbite;
- la composizione `ConfigurazioneFrattale` (famiglia, vista, immagine,
  parametri) con conversione verso e da dizionari JSON della versione 1;
- l'`ArchivioConfigurazioni` con salvataggio atomico tramite file
  temporaneo e caricamento che preserva la configurazione corrente in
  caso di errore;
- gli aiuti per l'analisi dei costi (stime, conteggi e misura
  del lavoro effettivo con i confini dichiarati).

La direzione delle dipendenze è dominio e algoritmi verso dati di
risultato: il modello importa soltanto validatori e tabelle dei contratti
(`contratti_raster_json`, `coordinate_esempi`, `palette_esempi`) e non
importa né Tkinter né Pillow. L'importazione del modulo non apre finestre,
non crea immagini e non esegue operazioni di I/O.

L'esempio preparatorio resta distinto dalla soluzione integrale del
progetto autonomo (L8): i generatori coprono un dominio circoscritto
(Koch sulla base canonica, Sierpiński sul triangolo canonico,
classificatori con il contratto unico di fuga) e la finestra completa con
i quattro generatori integrati resta compito della consegna.

Ambiente: CPython 3.14 sul computer. I tempi misurati con
`time.perf_counter` documentano ordini di grandezza sull'hardware usato;
i test di correttezza restano indipendenti dalla velocità dell'hardware.
"""

from __future__ import annotations

import json
import math
import os
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from contratti_raster_json import (
    FAMIGLIE_FRATTALI_AMMESSE,
    LIMITI_APPLICATIVI,
    PALETTE_AMMESSE,
    STILI_SIERPINSKI_AMMESSI,
    VARIANTI_KOCH_AMMESSE,
    VERSIONE_SCHEMA_ATTUALE,
    valida_dizionario_configurazione_riferimento,
)
from coordinate_esempi import valida_intero_non_booleano, valida_reale_finito
from palette_esempi import colora_esito, valida_limite_iterazioni

type ColoreRGB = tuple[int, int, int]
type EsitoPixel = int | None
type Punto2D = tuple[float, float]
type Segmento2D = tuple[Punto2D, Punto2D]
type Triangolo2D = tuple[Punto2D, Punto2D, Punto2D]


# ---------------------------------------------------------------------------
# Eccezioni di dominio proporzionate (§9.4)
# ---------------------------------------------------------------------------


class ErroreConfigurazione(ValueError):
    """Configurazione di un frattale invalida nel dominio o nei limiti operativi."""


class VersioneNonSupportata(ErroreConfigurazione):
    """Versione dello schema JSON diversa da quella supportata."""


class TipoNonSupportato(ErroreConfigurazione):
    """Famiglia, palette, variante o stile non appartenente ai contratti."""


class LimiteOperativoSuperato(ErroreConfigurazione):
    """Parametro oltre i limiti dell'applicazione didattica o budget superato."""


# ---------------------------------------------------------------------------
# Oggetti di valore: vista, immagine e parametri delle quattro famiglie
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class VistaComplessa:
    """Vista rettangolare del piano complesso con centro e ampiezza orizzontale.

    L'ampiezza verticale deriva dalla scala uniforme (`s_y = s_x * H / W`)
    al momento dell'uso, così la vista conserva le proporzioni per ogni
    risoluzione. Le componenti del centro appartengono a `[-100, 100]`,
    l'ampiezza orizzontale a `[1e-6, 20]`.
    """

    centro_reale: float
    centro_immaginaria: float
    ampiezza_orizzontale: float

    def __post_init__(self) -> None:
        x_c = valida_reale_finito(self.centro_reale, "centro_reale")
        y_c = valida_reale_finito(self.centro_immaginaria, "centro_immaginaria")
        s_x = valida_reale_finito(self.ampiezza_orizzontale, "ampiezza_orizzontale")
        limiti = LIMITI_APPLICATIVI
        if not (limiti.componente_centro_min <= x_c <= limiti.componente_centro_max):
            raise ErroreConfigurazione(
                f"Il campo 'centro_reale' richiede un valore in "
                f"[{limiti.componente_centro_min}, {limiti.componente_centro_max}]."
            )
        if not (limiti.componente_centro_min <= y_c <= limiti.componente_centro_max):
            raise ErroreConfigurazione(
                f"Il campo 'centro_immaginaria' richiede un valore in "
                f"[{limiti.componente_centro_min}, {limiti.componente_centro_max}]."
            )
        if not (limiti.ampiezza_vista_min <= s_x <= limiti.ampiezza_vista_max):
            raise ErroreConfigurazione(
                f"Il campo 'ampiezza_orizzontale' richiede un valore in "
                f"[{limiti.ampiezza_vista_min}, {limiti.ampiezza_vista_max}]."
            )
        object.__setattr__(self, "centro_reale", x_c)
        object.__setattr__(self, "centro_immaginaria", y_c)
        object.__setattr__(self, "ampiezza_orizzontale", s_x)


@dataclass(frozen=True)
class ParametriImmagine:
    """Dimensioni in pixel e palette dell'immagine da produrre.

    I limiti operativi sono `1..800` per la larghezza e `1..600` per
    l'altezza; il budget combinato `W * H * N` si controlla nella
    configurazione, dove il limite di iterazioni è noto.
    """

    larghezza: int
    altezza: int
    palette: str = "bande"

    def __post_init__(self) -> None:
        limiti = LIMITI_APPLICATIVI
        w = valida_intero_non_booleano(self.larghezza, "larghezza")
        h = valida_intero_non_booleano(self.altezza, "altezza")
        if not (limiti.larghezza_min <= w <= limiti.larghezza_max):
            raise LimiteOperativoSuperato(
                f"Larghezza {w} fuori dai limiti [{limiti.larghezza_min}, {limiti.larghezza_max}]."
            )
        if not (limiti.altezza_min <= h <= limiti.altezza_max):
            raise LimiteOperativoSuperato(
                f"Altezza {h} fuori dai limiti [{limiti.altezza_min}, {limiti.altezza_max}]."
            )
        if not isinstance(self.palette, str) or self.palette not in PALETTE_AMMESSE:
            raise TipoNonSupportato(
                f"Palette '{self.palette}' non valida; ammesse: {PALETTE_AMMESSE}."
            )


@dataclass(frozen=True)
class ParametriMandelbrot:
    """Budget di iterazioni della famiglia di Mandelbrot (`1..500`, default `100`)."""

    limite_iterazioni: int = 100

    def __post_init__(self) -> None:
        valida_limite_operativo(valida_limite_iterazioni(self.limite_iterazioni))


@dataclass(frozen=True)
class ParametriJulia:
    """Budget di iterazioni e parametro `c` della famiglia di Julia.

    Ciascuna componente di `c` appartiene a `[-10, 10]`, intervallo che
    include il caso diagnostico `c = -6` del punto fisso `z_0 = 3`.
    """

    limite_iterazioni: int = 100
    c_reale: float = -0.8
    c_immaginaria: float = 0.156

    def __post_init__(self) -> None:
        valida_limite_operativo(valida_limite_iterazioni(self.limite_iterazioni))
        limiti = LIMITI_APPLICATIVI
        c_re = valida_reale_finito(self.c_reale, "c_reale")
        c_im = valida_reale_finito(self.c_immaginaria, "c_immaginaria")
        if not (limiti.componente_julia_min <= c_re <= limiti.componente_julia_max):
            raise LimiteOperativoSuperato(
                f"La componente reale di 'c' ({c_re}) richiede un valore in "
                f"[{limiti.componente_julia_min}, {limiti.componente_julia_max}]."
            )
        if not (limiti.componente_julia_min <= c_im <= limiti.componente_julia_max):
            raise LimiteOperativoSuperato(
                f"La componente immaginaria di 'c' ({c_im}) richiede un valore in "
                f"[{limiti.componente_julia_min}, {limiti.componente_julia_max}]."
            )
        object.__setattr__(self, "c_reale", c_re)
        object.__setattr__(self, "c_immaginaria", c_im)


@dataclass(frozen=True)
class ParametriKoch:
    """Livello (`0..6`), variante e lato iniziale (`0.1..20`) di Koch."""

    livello: int = 3
    variante: str = "fiocco"
    lato_iniziale: float = 3.0

    def __post_init__(self) -> None:
        limiti = LIMITI_APPLICATIVI
        livello = valida_intero_non_booleano(self.livello, "livello")
        if not (limiti.livello_koch_min <= livello <= limiti.livello_koch_max):
            raise LimiteOperativoSuperato(
                f"Livello di Koch {livello} fuori dai limiti "
                f"[{limiti.livello_koch_min}, {limiti.livello_koch_max}]."
            )
        if not isinstance(self.variante, str) or self.variante not in VARIANTI_KOCH_AMMESSE:
            raise TipoNonSupportato(
                f"Variante di Koch non valida; ammesse: {VARIANTI_KOCH_AMMESSE}."
            )
        lato = valida_reale_finito(self.lato_iniziale, "lato_iniziale")
        if not (limiti.lato_iniziale_min <= lato <= limiti.lato_iniziale_max):
            raise LimiteOperativoSuperato("Lato iniziale di Koch fuori dai limiti operativi.")


@dataclass(frozen=True)
class ParametriSierpinski:
    """Livello (`0..7`), stile e lato iniziale (`0.1..20`) di Sierpiński."""

    livello: int = 4
    stile: str = "pieno"
    lato_iniziale: float = 4.0

    def __post_init__(self) -> None:
        limiti = LIMITI_APPLICATIVI
        livello = valida_intero_non_booleano(self.livello, "livello")
        if not (limiti.livello_sierpinski_min <= livello <= limiti.livello_sierpinski_max):
            raise LimiteOperativoSuperato(
                f"Livello di Sierpiński {livello} fuori dai limiti "
                f"[{limiti.livello_sierpinski_min}, {limiti.livello_sierpinski_max}]."
            )
        if not isinstance(self.stile, str) or self.stile not in STILI_SIERPINSKI_AMMESSI:
            raise TipoNonSupportato(
                f"Stile di Sierpiński non valido; ammessi: {STILI_SIERPINSKI_AMMESSI}."
            )
        lato = valida_reale_finito(self.lato_iniziale, "lato_iniziale")
        if not (limiti.lato_iniziale_min <= lato <= limiti.lato_iniziale_max):
            raise LimiteOperativoSuperato("Lato iniziale di Sierpiński fuori dai limiti operativi.")


def valida_limite_operativo(limite_iterazioni: int) -> int:
    """Controlla il budget `N` contro i limiti operativi `1..500`."""
    limiti = LIMITI_APPLICATIVI
    if not (limiti.iterazioni_min <= limite_iterazioni <= limiti.iterazioni_max):
        raise LimiteOperativoSuperato(
            f"Limite iterazioni {limite_iterazioni} fuori dai limiti "
            f"[{limiti.iterazioni_min}, {limiti.iterazioni_max}]."
        )
    return limite_iterazioni


# ---------------------------------------------------------------------------
# Contratto quadratico: classificazione di un punto con il kernel di fuga
# ---------------------------------------------------------------------------


def indice_fuga_quadratico(
    seme_z0: complex, parametro_c: complex, limite_iterazioni: int, raggio_fuga: float
) -> EsitoPixel:
    """Restituisce l'indice di fuga del seme o `None` a budget esaurito.

    L'ordine segue il contratto unico: controllo iniziale su `z_0 = punto`
    prima di qualsiasi aggiornamento, poi aggiornamento `z = z * z + c`
    con confronto stretto `>` al raggio. Il confronto usa i quadrati dei
    moduli per chiarezza del costo; la semantica coincide con `abs`.
    """
    n_max = valida_limite_iterazioni(limite_iterazioni)
    raggio = valida_reale_finito(raggio_fuga, "raggio_fuga")
    if raggio <= 0.0:
        raise ValueError("Il parametro 'raggio_fuga' richiede un valore positivo.")
    if not isinstance(seme_z0, complex) or not isinstance(parametro_c, complex):
        raise TypeError("I parametri 'seme_z0' e 'parametro_c' richiedono numeri complessi.")
    z = seme_z0
    if z.real * z.real + z.imag * z.imag > raggio * raggio:
        return 0
    for passo in range(1, n_max + 1):
        z = z * z + parametro_c
        if z.real * z.real + z.imag * z.imag > raggio * raggio:
            return passo
    return None


@runtime_checkable
class ClassificatoreQuadratico(Protocol):
    """Contratto dei generatori numerici: classifica un punto della vista."""

    def classifica(self, punto: complex) -> EsitoPixel:
        """Restituisce l'indice di fuga del punto oppure `None`."""
        ...


class ClassificatoreMandelbrot:
    """Generatore di Mandelbrot: seme fisso `z_0 = 0`, parametro variabile `c`."""

    def __init__(self, limite_iterazioni: object = 100) -> None:
        self.limite_iterazioni = valida_limite_operativo(
            valida_limite_iterazioni(limite_iterazioni)
        )

    def classifica(self, punto: complex) -> EsitoPixel:
        """Classifica il punto come parametro `c` con seme zero e `R = 2.0`."""
        if not isinstance(punto, complex):
            raise TypeError("Il parametro 'punto' richiede un numero complesso.")
        return indice_fuga_quadratico(complex(0.0, 0.0), punto, self.limite_iterazioni, 2.0)


class ClassificatoreJulia:
    """Generatore di Julia: parametro `c` fisso, seme variabile `z_0`."""

    def __init__(
        self,
        limite_iterazioni: object = 100,
        c: object = complex(-0.8, 0.156),
    ) -> None:
        self.limite_iterazioni = valida_limite_operativo(
            valida_limite_iterazioni(limite_iterazioni)
        )
        if not isinstance(c, complex):
            raise TypeError("Il parametro 'c' richiede un numero complesso.")
        if not (math.isfinite(c.real) and math.isfinite(c.imag)):
            raise ValueError("Il parametro 'c' non ammette componenti NaN o infinite.")
        limiti = LIMITI_APPLICATIVI
        if not (limiti.componente_julia_min <= c.real <= limiti.componente_julia_max):
            raise LimiteOperativoSuperato("La componente reale di 'c' esce da [-10, 10].")
        if not (limiti.componente_julia_min <= c.imag <= limiti.componente_julia_max):
            raise LimiteOperativoSuperato("La componente immaginaria di 'c' esce da [-10, 10].")
        self.parametro_c = c

    def classifica(self, punto: complex) -> EsitoPixel:
        """Classifica il punto come seme con raggio sicuro `max(2.0, |c|)`.

        Il raggio `max(2.0, |c|)` rende il punto fisso `z_0 = 3` con `c = -6`
        correttamente interno (`3^2 - 6 = 3`, raggio `6`); il raggio
        universale `2` produrrebbe una falsa fuga.
        """
        raggio = max(2.0, abs(self.parametro_c))
        return indice_fuga_quadratico(punto, self.parametro_c, self.limite_iterazioni, raggio)


def classifica_punti(
    classificatore: ClassificatoreQuadratico, punti: list[complex] | tuple[complex, ...]
) -> tuple[EsitoPixel, ...]:
    """Classifica una sequenza di punti con un qualsiasi classificatore.

    La funzione accetta qualunque implementazione del contratto, così la
    sostituzione di Mandelbrot con Julia (o viceversa) non richiede
    modifiche al codice che usa il risultato.
    """
    if not isinstance(classificatore, ClassificatoreQuadratico):
        raise TypeError("Il parametro 'classificatore' richiede un ClassificatoreQuadratico.")
    return tuple(classificatore.classifica(punto) for punto in punti)


# ---------------------------------------------------------------------------
# Contratto geometrico: produzione finita di Koch e Sierpiński
# ---------------------------------------------------------------------------


def _punta_koch_60_gradi(base_x: float, base_y: float, delta_x: float, delta_y: float) -> Punto2D:
    coseno_60 = 0.5
    seno_60 = math.sqrt(3.0) / 2.0
    return (
        base_x + delta_x * coseno_60 - delta_y * seno_60,
        base_y + delta_x * seno_60 + delta_y * coseno_60,
    )


def _suddividi_segmento_koch(segmento: Segmento2D) -> tuple[Segmento2D, ...]:
    (x_a, y_a), (x_b, y_b) = segmento
    delta_x = (x_b - x_a) / 3.0
    delta_y = (y_b - y_a) / 3.0
    primo = (x_a + delta_x, y_a + delta_y)
    secondo = (x_a + 2.0 * delta_x, y_a + 2.0 * delta_y)
    punta = _punta_koch_60_gradi(primo[0], primo[1], delta_x, delta_y)
    origine: Punto2D = (x_a, y_a)
    fine: Punto2D = (x_b, y_b)
    return ((origine, primo), (primo, punta), (punta, secondo), (secondo, fine))


def _punto_medio(primo: Punto2D, secondo: Punto2D) -> Punto2D:
    return ((primo[0] + secondo[0]) / 2.0, (primo[1] + secondo[1]) / 2.0)


@runtime_checkable
class ProduttoreGeometrico(Protocol):
    """Contratto dei generatori geometrici: produce gli elementi finiti."""

    def produci(self) -> tuple:
        """Restituisce gli elementi (segmenti o triangoli) del livello."""
        ...

    def conta_elementi(self) -> int:
        """Restituisce il numero esatto di elementi del livello."""
        ...


class ProduttoreKoch:
    """Generatore di Koch sulla base canonica con lato dichiarato.

    La variante `"curva"` parte dal segmento `((0, 0), (lato, 0))`; la
    variante `"fiocco"` percorre in senso orario il triangolo con vertici
    `(0, 0)`, `(lato/2, lato/2 * √3)`, `(lato, 0)`, così le punte risultano
    esterne come nel contratto L1. I conteggi sono `4^d` per la curva e
    `3 * 4^d` per il fiocco.
    """

    def __init__(
        self,
        livello: object = 3,
        variante: object = "fiocco",
        lato_iniziale: object = 3.0,
    ) -> None:
        parametri = ParametriKoch(
            livello=livello,
            variante=variante,
            lato_iniziale=lato_iniziale,  # type: ignore[arg-type]
        )
        self.livello = parametri.livello
        self.variante = parametri.variante
        self.lato_iniziale = parametri.lato_iniziale

    def _segmenti_iniziali(self) -> tuple[Segmento2D, ...]:
        lato = self.lato_iniziale
        if self.variante == "curva":
            return (((0.0, 0.0), (lato, 0.0)),)
        vertice_alto: Punto2D = (lato / 2.0, lato / 2.0 * math.sqrt(3.0))
        return (
            ((0.0, 0.0), vertice_alto),
            (vertice_alto, (lato, 0.0)),
            ((lato, 0.0), (0.0, 0.0)),
        )

    def produci(self) -> tuple[Segmento2D, ...]:
        """Costruisce i segmenti con accumulatore e singolo `append` per foglia."""
        segmenti: list[Segmento2D] = []

        def visita(segmento: Segmento2D, livello_rimasto: int) -> None:
            if livello_rimasto == 0:
                segmenti.append(segmento)
                return
            for sotto in _suddividi_segmento_koch(segmento):
                visita(sotto, livello_rimasto - 1)

        for iniziale in self._segmenti_iniziali():
            visita(iniziale, self.livello)
        return tuple(segmenti)

    def conta_elementi(self) -> int:
        """Restituisce `4^d` per la curva e `3 * 4^d` per il fiocco."""
        base = 4**self.livello
        return base if self.variante == "curva" else 3 * base


class ProduttoreSierpinski:
    """Generatore di Sierpiński sul triangolo canonico con lato dichiarato.

    La base ha vertici `(0, 0)`, `(lato, 0)`, `(lato/2, lato * √3/2)`; ogni
    livello ricorre sui tre triangoli d'angolo ed esclude il centrale. Lo
    stile (`"pieno"` o `"contorno"`) riguarda la resa e non gli elementi:
    i triangoli prodotti sono gli stessi. Il conteggio è `3^d`.
    """

    def __init__(
        self,
        livello: object = 4,
        stile: object = "pieno",
        lato_iniziale: object = 4.0,
    ) -> None:
        parametri = ParametriSierpinski(
            livello=livello,
            stile=stile,
            lato_iniziale=lato_iniziale,  # type: ignore[arg-type]
        )
        self.livello = parametri.livello
        self.stile = parametri.stile
        self.lato_iniziale = parametri.lato_iniziale

    def _triangolo_iniziale(self) -> Triangolo2D:
        lato = self.lato_iniziale
        return ((0.0, 0.0), (lato, 0.0), (lato / 2.0, lato * math.sqrt(3.0) / 2.0))

    def produci(self) -> tuple[Triangolo2D, ...]:
        """Costruisce i triangoli con accumulatore e singolo `append` per foglia."""
        triangoli: list[Triangolo2D] = []

        def visita(triangolo: Triangolo2D, livello_rimasto: int) -> None:
            if livello_rimasto == 0:
                triangoli.append(triangolo)
                return
            vertice_a, vertice_b, vertice_c = triangolo
            medio_ab = _punto_medio(vertice_a, vertice_b)
            medio_bc = _punto_medio(vertice_b, vertice_c)
            medio_ca = _punto_medio(vertice_c, vertice_a)
            visita((vertice_a, medio_ab, medio_ca), livello_rimasto - 1)
            visita((medio_ab, vertice_b, medio_bc), livello_rimasto - 1)
            visita((medio_ca, medio_bc, vertice_c), livello_rimasto - 1)

        visita(self._triangolo_iniziale(), self.livello)
        return tuple(triangoli)

    def conta_elementi(self) -> int:
        """Restituisce `3^d` triangoli del livello."""
        return 3**self.livello


def elementi_geometrici(produttore: ProduttoreGeometrico) -> tuple:
    """Restituisce gli elementi di un qualsiasi produttore geometrico.

    La funzione accetta qualunque implementazione del contratto, così la
    sostituzione di Koch con Sierpiński (o viceversa) non richiede
    modifiche al codice che usa il risultato.
    """
    if not isinstance(produttore, ProduttoreGeometrico):
        raise TypeError("Il parametro 'produttore' richiede un ProduttoreGeometrico.")
    elementi = produttore.produci()
    if len(elementi) != produttore.conta_elementi():
        raise AssertionError("Il conteggio dichiarato non coincide con gli elementi prodotti.")
    return elementi


# ---------------------------------------------------------------------------
# Contratto di colorazione: tre strategie sostituibili sugli stessi esiti
# ---------------------------------------------------------------------------


@runtime_checkable
class Colorazione(Protocol):
    """Contratto delle strategie di colorazione deterministica."""

    @property
    def nome(self) -> str:
        """Restituisce il nome canonico della palette."""
        ...

    def colora(self, indice_fuga: EsitoPixel, limite_iterazioni: int) -> ColoreRGB:
        """Traduce un esito in RGB distinguendo `None` da `0` con `is None`."""
        ...


class ColorazioneBinaria:
    """Strategia binaria: interno dedicato contro unico colore di fuga."""

    @property
    def nome(self) -> str:
        return "binaria"

    def colora(self, indice_fuga: EsitoPixel, limite_iterazioni: int) -> ColoreRGB:
        return colora_esito(indice_fuga, limite_iterazioni, "binaria")


class ColorazioneBande:
    """Strategia a bande: tabella di otto colori con `n % 8`."""

    @property
    def nome(self) -> str:
        return "bande"

    def colora(self, indice_fuga: EsitoPixel, limite_iterazioni: int) -> ColoreRGB:
        return colora_esito(indice_fuga, limite_iterazioni, "bande")


class ColorazioneGradiente:
    """Strategia a gradiente: interpolazione lineare fra gli estremi."""

    @property
    def nome(self) -> str:
        return "gradiente"

    def colora(self, indice_fuga: EsitoPixel, limite_iterazioni: int) -> ColoreRGB:
        return colora_esito(indice_fuga, limite_iterazioni, "gradiente")


def colora_riga_esiti(
    colorazione: Colorazione,
    riga_esiti: list[EsitoPixel] | tuple[EsitoPixel, ...],
    limite_iterazioni: int,
) -> tuple[ColoreRGB, ...]:
    """Colora una riga di esiti con una qualsiasi strategia di colorazione.

    La stessa riga assume vesti diverse senza ricalcolare le orbite: la
    prova di sostituibilità confronta le tre strategie sugli stessi esiti.
    """
    if not isinstance(colorazione, Colorazione):
        raise TypeError("Il parametro 'colorazione' richiede una Colorazione.")
    n_max = valida_limite_iterazioni(limite_iterazioni)
    return tuple(colorazione.colora(esito, n_max) for esito in riga_esiti)


# ---------------------------------------------------------------------------
# Composizione: la configurazione riunisce famiglia, vista e immagine
# ---------------------------------------------------------------------------

ParametriFamiglia = ParametriMandelbrot | ParametriJulia | ParametriKoch | ParametriSierpinski

PARAMETRI_PER_FAMIGLIA: dict[str, tuple[type, ...]] = {
    "mandelbrot": (ParametriMandelbrot,),
    "julia": (ParametriJulia,),
    "koch": (ParametriKoch,),
    "sierpinski": (ParametriSierpinski,),
}


def complesso_a_oggetto(punto: complex) -> dict[str, float]:
    """Converte un complesso nell'oggetto JSON con chiavi `reale` e `immaginaria`."""
    if not isinstance(punto, complex):
        raise TypeError("Il parametro 'punto' richiede un numero complesso.")
    if not (math.isfinite(punto.real) and math.isfinite(punto.imag)):
        raise ValueError("Il punto non ammette componenti NaN o infinite.")
    return {"reale": punto.real, "immaginaria": punto.imag}


def oggetto_a_complesso(valore: object, nome_campo: str, minimo: float, massimo: float) -> complex:
    """Ricostruisce un complesso validando chiavi, finitezza e intervallo."""
    if not isinstance(valore, dict):
        raise TypeError(
            f"Il campo '{nome_campo}' deve essere un oggetto con 'reale' e 'immaginaria'."
        )
    if set(valore.keys()) != {"reale", "immaginaria"}:
        raise ValueError(
            f"Il campo '{nome_campo}' deve contenere esattamente 'reale' e 'immaginaria'."
        )
    reale = valida_reale_finito(valore["reale"], f"{nome_campo}.reale")
    immaginaria = valida_reale_finito(valore["immaginaria"], f"{nome_campo}.immaginaria")
    if not (minimo <= reale <= massimo) or not (minimo <= immaginaria <= massimo):
        raise ErroreConfigurazione(
            f"Le componenti di '{nome_campo}' devono appartenere a [{minimo}, {massimo}]."
        )
    return complex(reale, immaginaria)


@dataclass(frozen=True)
class ConfigurazioneFrattale:
    """Composizione di famiglia, parametri, vista e immagine di un frattale.

    La configurazione è l'unità salvata nel JSON: contiene i parametri,
    non i milioni di pixel né le orbite. Il budget combinato `W * H * N`
    delle famiglie numeriche non supera `100_000_000` aggiornamenti.
    """

    tipo_frattale: str
    vista: VistaComplessa
    immagine: ParametriImmagine
    parametri: ParametriFamiglia

    def __post_init__(self) -> None:
        if not isinstance(self.tipo_frattale, str) or (
            self.tipo_frattale not in FAMIGLIE_FRATTALI_AMMESSE
        ):
            raise TipoNonSupportato(
                f"Tipo frattale non supportato; ammessi: {FAMIGLIE_FRATTALI_AMMESSE}."
            )
        if not isinstance(self.vista, VistaComplessa):
            raise TypeError("Il campo 'vista' richiede una VistaComplessa.")
        if not isinstance(self.immagine, ParametriImmagine):
            raise TypeError("Il campo 'immagine' richiede dei ParametriImmagine.")
        attesi = PARAMETRI_PER_FAMIGLIA[self.tipo_frattale]
        if not isinstance(self.parametri, attesi):
            raise ErroreConfigurazione(
                f"La famiglia '{self.tipo_frattale}' richiede parametri {attesi[0].__name__}."
            )
        if self.tipo_frattale in ("mandelbrot", "julia"):
            limite = self.parametri.limite_iterazioni  # type: ignore[union-attr]
            budget = self.immagine.larghezza * self.immagine.altezza * limite
            if budget > LIMITI_APPLICATIVI.budget_aggiornamenti_max:
                raise LimiteOperativoSuperato(
                    f"Il budget stimato W*H*N = {budget} supera il limite operativo "
                    f"di {LIMITI_APPLICATIVI.budget_aggiornamenti_max} aggiornamenti; "
                    f"ridurre risoluzione o N."
                )

    def a_dizionario(self) -> dict[str, Any]:
        """Restituisce il documento JSON versione 1 della configurazione."""
        centro = complesso_a_oggetto(
            complex(self.vista.centro_reale, self.vista.centro_immaginaria)
        )
        documento: dict[str, Any] = {
            "versione_schema": VERSIONE_SCHEMA_ATTUALE,
            "tipo_frattale": self.tipo_frattale,
            "immagine": {
                "larghezza": self.immagine.larghezza,
                "altezza": self.immagine.altezza,
                "palette": self.immagine.palette,
            },
            "vista": {
                "centro": centro,
                "ampiezza_orizzontale": self.vista.ampiezza_orizzontale,
            },
            "parametri": self._parametri_a_dizionario(),
        }
        return documento

    def _parametri_a_dizionario(self) -> dict[str, Any]:
        parametri = self.parametri
        if isinstance(parametri, ParametriMandelbrot):
            return {"limite_iterazioni": parametri.limite_iterazioni}
        if isinstance(parametri, ParametriJulia):
            return {
                "limite_iterazioni": parametri.limite_iterazioni,
                "c": complesso_a_oggetto(complex(parametri.c_reale, parametri.c_immaginaria)),
            }
        if isinstance(parametri, ParametriKoch):
            return {
                "livello": parametri.livello,
                "variante": parametri.variante,
                "lato_iniziale": parametri.lato_iniziale,
            }
        if isinstance(parametri, ParametriSierpinski):
            return {
                "livello": parametri.livello,
                "stile": parametri.stile,
                "lato_iniziale": parametri.lato_iniziale,
            }
        raise ErroreConfigurazione("Parametri di famiglia non riconosciuti.")  # pragma: no cover

    @classmethod
    def da_dizionario(cls, dati: object) -> ConfigurazioneFrattale:
        """Ricostruisce la configurazione validando come la GUI.

        Il documento attraversa prima l'oracolo di validazione condiviso
        (stesse regole della finestra), poi la costruzione degli oggetti
        che valida di nuovo ogni campo: un documento caricato è valido
        quanto uno composto nella GUI. Versioni e tipi non supportati
        sollevano le eccezioni dedicate.
        """
        if not isinstance(dati, dict):
            raise TypeError("Il documento di configurazione deve essere un oggetto (dict).")
        try:
            validati = valida_dizionario_configurazione_riferimento(dati)
        except ValueError as causa:
            messaggio = str(causa)
            if "Versione schema" in messaggio:
                raise VersioneNonSupportata(messaggio) from causa
            if "non supportato" in messaggio or "non valida" in messaggio:
                raise TipoNonSupportato(messaggio) from causa
            if "supera il limite" in messaggio or "fuori dai limiti" in messaggio:
                raise LimiteOperativoSuperato(messaggio) from causa
            raise ErroreConfigurazione(messaggio) from causa
        return cls._costruisci_da_validati(validati)

    @classmethod
    def _costruisci_da_validati(cls, dati: dict[str, Any]) -> ConfigurazioneFrattale:
        limiti = LIMITI_APPLICATIVI
        vista_dati = dati["vista"]
        centro = oggetto_a_complesso(
            vista_dati["centro"],
            "vista.centro",
            limiti.componente_centro_min,
            limiti.componente_centro_max,
        )
        vista = VistaComplessa(
            centro_reale=centro.real,
            centro_immaginaria=centro.imag,
            ampiezza_orizzontale=vista_dati["ampiezza_orizzontale"],
        )
        immagine_dati = dati["immagine"]
        immagine = ParametriImmagine(
            larghezza=immagine_dati["larghezza"],
            altezza=immagine_dati["altezza"],
            palette=immagine_dati["palette"],
        )
        tipo = dati["tipo_frattale"]
        parametri_dati = dati["parametri"]
        if tipo == "mandelbrot":
            parametri: ParametriFamiglia = ParametriMandelbrot(
                limite_iterazioni=parametri_dati["limite_iterazioni"]
            )
        elif tipo == "julia":
            costante = oggetto_a_complesso(
                parametri_dati["c"],
                "parametri.c",
                limiti.componente_julia_min,
                limiti.componente_julia_max,
            )
            parametri = ParametriJulia(
                limite_iterazioni=parametri_dati["limite_iterazioni"],
                c_reale=costante.real,
                c_immaginaria=costante.imag,
            )
        elif tipo == "koch":
            parametri = ParametriKoch(
                livello=parametri_dati["livello"],
                variante=parametri_dati["variante"],
                lato_iniziale=parametri_dati["lato_iniziale"],
            )
        else:
            parametri = ParametriSierpinski(
                livello=parametri_dati["livello"],
                stile=parametri_dati["stile"],
                lato_iniziale=parametri_dati["lato_iniziale"],
            )
        return cls(tipo_frattale=tipo, vista=vista, immagine=immagine, parametri=parametri)

    def riepilogo(self) -> str:
        """Restituisce il riepilogo testuale con famiglia e parametri principali."""
        immagine = self.immagine
        base = (
            f"{self.tipo_frattale} {immagine.larghezza}x{immagine.altezza} "
            f"palette {immagine.palette}, vista ({self.vista.centro_reale}, "
            f"{self.vista.centro_immaginaria}) ampiezza {self.vista.ampiezza_orizzontale}"
        )
        return base + ", " + self._riepilogo_parametri()

    def _riepilogo_parametri(self) -> str:
        parametri = self.parametri
        if isinstance(parametri, ParametriMandelbrot):
            return f"N={parametri.limite_iterazioni}"
        if isinstance(parametri, ParametriJulia):
            return (
                f"N={parametri.limite_iterazioni}, c={parametri.c_reale}+{parametri.c_immaginaria}i"
            )
        if isinstance(parametri, ParametriKoch):
            return (
                f"livello={parametri.livello}, variante={parametri.variante}, "
                f"lato={parametri.lato_iniziale}"
            )
        if isinstance(parametri, ParametriSierpinski):
            return (
                f"livello={parametri.livello}, stile={parametri.stile}, "
                f"lato={parametri.lato_iniziale}"
            )
        raise ErroreConfigurazione("Parametri di famiglia non riconosciuti.")  # pragma: no cover


# ---------------------------------------------------------------------------
# Persistenza: salvataggio atomico e caricamento senza perdita dello stato
# ---------------------------------------------------------------------------


class ArchivioConfigurazioni:
    """Caricamento e salvataggio JSON delle configurazioni con garanzie esplicite.

    Il salvataggio scrive prima in un file temporaneo nella stessa
    directory e sostituisce il file finale soltanto a scrittura completata:
    se l'operazione fallisce, il file precedente resta preservato. Il
    caricamento fallito solleva l'errore senza modificare la
    configurazione corrente del chiamante, che conserva il proprio oggetto.
    I testi usano UTF-8 e rifiutano `NaN` e infiniti anche in scrittura
    (`allow_nan=False`).
    """

    @staticmethod
    def a_testo_json(configurazione: ConfigurazioneFrattale) -> str:
        """Serializza la configurazione in testo JSON valido."""
        if not isinstance(configurazione, ConfigurazioneFrattale):
            raise TypeError("Il parametro 'configurazione' richiede una ConfigurazioneFrattale.")
        return json.dumps(
            configurazione.a_dizionario(), indent=2, ensure_ascii=False, allow_nan=False
        )

    @staticmethod
    def da_testo_json(testo_json: object) -> ConfigurazioneFrattale:
        """Deserializza e valida un testo JSON con rifiuto di `NaN` e infiniti."""
        if not isinstance(testo_json, str):
            raise TypeError("Il parametro 'testo_json' richiede una stringa.")

        def _rifiuta_costanti_non_finite(costante: str) -> Any:
            raise ErroreConfigurazione(f"Costante JSON non finita non ammessa: {costante}.")

        try:
            dati = json.loads(testo_json, parse_constant=_rifiuta_costanti_non_finite)
        except json.JSONDecodeError as causa:
            raise ErroreConfigurazione(
                f"Documento JSON malformato: {causa.msg} alla riga {causa.lineno}."
            ) from causa
        return ConfigurazioneFrattale.da_dizionario(dati)

    def salva(
        self, percorso: str | os.PathLike[str], configurazione: ConfigurazioneFrattale
    ) -> Path:
        """Salva la configurazione con scrittura atomica e restituisce il percorso."""
        destinazione = Path(percorso)
        testo = self.a_testo_json(configurazione)
        cartella = destinazione.parent
        if str(cartella) not in ("", "."):
            cartella.mkdir(parents=True, exist_ok=True)
        temporaneo: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=str(cartella) if str(cartella) not in ("", ".") else ".",
                prefix=destinazione.name + ".",
                suffix=".tmp",
                delete=False,
            ) as maniglia:
                temporaneo = Path(maniglia.name)
                maniglia.write(testo)
            os.replace(temporaneo, destinazione)
        except Exception:
            if temporaneo is not None and temporaneo.exists():
                try:
                    temporaneo.unlink()
                except OSError:
                    pass
            raise
        return destinazione

    def carica(self, percorso: str | os.PathLike[str]) -> ConfigurazioneFrattale:
        """Carica e valida la configurazione; in caso di errore solleva senza effetti.

        La funzione restituisce sempre un nuovo oggetto: la configurazione
        corrente del chiamante resta invariata quando il caricamento
        fallisce (errori di I/O, JSON malformato o dominio invalido).
        """
        origine = Path(percorso)
        try:
            testo = origine.read_text(encoding="utf-8")
        except FileNotFoundError as causa:
            raise ErroreConfigurazione(f"File di configurazione non trovato: {origine}.") from causa
        except OSError as causa:
            raise ErroreConfigurazione(
                f"Lettura del file di configurazione non riuscita: {causa}."
            ) from causa
        return self.da_testo_json(testo)


# ---------------------------------------------------------------------------
# Costi: stime, conteggi e misura del lavoro con confini dichiarati
# ---------------------------------------------------------------------------


def stima_budget_aggiornamenti(
    larghezza: object, altezza: object, limite_iterazioni: object
) -> int:
    """Restituisce il limite superiore `W * H * N` degli aggiornamenti.

    Se il prodotto supera il budget operativo, solleva
    `LimiteOperativoSuperato` indicando di ridurre risoluzione o `N`.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    n_max = valida_limite_operativo(valida_limite_iterazioni(limite_iterazioni))
    budget = w * h * n_max
    if budget > LIMITI_APPLICATIVI.budget_aggiornamenti_max:
        raise LimiteOperativoSuperato(
            f"Il budget stimato W*H*N = {budget} supera il limite operativo "
            f"di {LIMITI_APPLICATIVI.budget_aggiornamenti_max} aggiornamenti; "
            f"ridurre risoluzione o N."
        )
    return budget


def lavoro_effettivo_da_matrice(matrice_esiti: list | tuple, limite_iterazioni: object) -> int:
    """Conta il lavoro effettivo `K`: `N` per `None`, `n` per l'indice `n`.

    Il conteggio distingue l'esito `None` (budget intero speso su quel
    pixel) dall'indice `0` (fuga immediata, zero aggiornamenti su quel
    pixel): il controllo usa `is None`. Vale sempre `K <= W * H * N`.
    """
    n_max = valida_limite_iterazioni(limite_iterazioni)
    if not isinstance(matrice_esiti, (tuple, list)) or len(matrice_esiti) == 0:
        raise TypeError("Il parametro 'matrice_esiti' richiede righe non vuote di esiti.")
    totale = 0
    for q, riga in enumerate(matrice_esiti):
        if not isinstance(riga, (tuple, list)) or len(riga) == 0:
            raise TypeError(f"La riga {q} richiede una sequenza non vuota di esiti.")
        for esito in riga:
            if esito is None:
                totale += n_max
            elif isinstance(esito, bool) or not isinstance(esito, int) or esito < 0:
                raise TypeError("Gli esiti richiedono interi >= 0 oppure None.")
            elif esito > n_max:
                raise ValueError(f"L'esito {esito} supera il limite {n_max}.")
            else:
                totale += esito
    return totale


def misura_classificazione(
    classifica: Callable[[complex], EsitoPixel],
    larghezza: int,
    altezza: int,
    centro: complex,
    ampiezza_orizzontale: float,
    limite_iterazioni: int,
) -> dict[str, Any]:
    """Misura il lavoro di classificazione con i confini dichiarati.

    La preparazione (costruzione della vista e del classificatore) resta
    fuori dalla regione cronometrata; il tempo copre soltanto il doppio
    ciclo di campionamento e classificazione. Restituisce matrice, lavoro
    `K`, limite superiore e secondi trascorsi.
    """
    from coordinate_esempi import griglia_punti

    if not callable(classifica):
        raise TypeError("Il parametro 'classifica' richiede una funzione chiamabile.")
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    if not isinstance(centro, complex):
        raise TypeError("Il parametro 'centro' richiede un numero complesso.")
    s_x = valida_reale_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    n_max = valida_limite_operativo(valida_limite_iterazioni(limite_iterazioni))
    griglia = griglia_punti(w, h, centro.real, centro.imag, s_x)
    inizio = time.perf_counter()
    matrice = tuple(tuple(classifica(punto) for punto in riga_punti) for riga_punti in griglia)
    secondi = time.perf_counter() - inizio
    lavoro = lavoro_effettivo_da_matrice(matrice, n_max)
    return {
        "matrice": matrice,
        "lavoro_effettivo": lavoro,
        "limite_superiore": w * h * n_max,
        "secondi": secondi,
    }
