"""Dominio dell'applicazione dei frattali: eccezioni, valori e configurazione.

Stato dello starter:

- forniti: eccezioni di dominio, `VistaComplessa` e `ParametriImmagine`
  con validazione (tappe FR-M1 e FR-M7);
- da completare: parametri delle quattro famiglie e `ConfigurazioneFrattale`
  con composizione, validazione del budget e conversioni JSON (tappe FR-M1
  e FR-M7, requisiti FR-09 e FR-11).

I kernel preparatori dei capitoli restano consultabili per confronto sui
meccanismi; trasferimento, integrazione e progettazione personale restano
lavoro dello studente.
"""

import math

FAMIGLIE_AMMESSE = ("koch", "sierpinski", "mandelbrot", "julia")
PALETTE_AMMESSE = ("binaria", "bande", "gradiente")

LARGHEZZA_MIN = 1
LARGHEZZA_MAX = 800
ALTEZZA_MIN = 1
ALTEZZA_MAX = 600
BUDGET_AGGIORNAMENTI_MAX = 100_000_000
CENTRO_MIN = -100.0
CENTRO_MAX = 100.0
AMPIEZZA_MIN = 1e-6
AMPIEZZA_MAX = 20.0


class ErroreConfigurazione(ValueError):
    """Configurazione invalida nel dominio o nei limiti operativi."""


class VersioneNonSupportata(ErroreConfigurazione):
    """Versione dello schema JSON diversa da quella supportata."""


class TipoNonSupportato(ErroreConfigurazione):
    """Famiglia, palette, variante o stile non appartenente ai contratti."""


class LimiteOperativoSuperato(ErroreConfigurazione):
    """Parametro oltre i limiti dell'applicazione o budget superato."""


def valida_intero(valore: object, nome: str) -> int:
    """Verifica che `valore` sia un intero non booleano (fornita)."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError(f"Il campo '{nome}' richiede un intero non booleano.")
    return valore


def valida_reale(valore: object, nome: str) -> float:
    """Verifica che `valore` sia un numero reale finito non booleano (fornita)."""
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        raise TypeError(f"Il campo '{nome}' richiede un numero reale non booleano.")
    risultato = float(valore)
    if not math.isfinite(risultato):
        raise ValueError(f"Il campo '{nome}' non ammette NaN o infinito.")
    return risultato


class VistaComplessa:
    """Vista rettangolare del piano complesso (fornita).

    Centro con componenti in `[-100, 100]`, ampiezza orizzontale in
    `[1e-6, 20]`; l'ampiezza verticale deriva dalla scala uniforme.
    """

    def __init__(
        self, centro_reale: object, centro_immaginaria: object, ampiezza_orizzontale: object
    ) -> None:
        x_c = valida_reale(centro_reale, "centro_reale")
        y_c = valida_reale(centro_immaginaria, "centro_immaginaria")
        s_x = valida_reale(ampiezza_orizzontale, "ampiezza_orizzontale")
        if not (CENTRO_MIN <= x_c <= CENTRO_MAX):
            raise ErroreConfigurazione("Il campo 'centro_reale' esce da [-100, 100].")
        if not (CENTRO_MIN <= y_c <= CENTRO_MAX):
            raise ErroreConfigurazione("Il campo 'centro_immaginaria' esce da [-100, 100].")
        if not (AMPIEZZA_MIN <= s_x <= AMPIEZZA_MAX):
            raise ErroreConfigurazione("Il campo 'ampiezza_orizzontale' esce da [1e-6, 20].")
        self.centro_reale = x_c
        self.centro_immaginaria = y_c
        self.ampiezza_orizzontale = s_x


class ParametriImmagine:
    """Dimensioni in pixel e palette dell'immagine (fornita).

    Larghezza in `1..800`, altezza in `1..600`, palette fra quelle ammesse;
    il budget `W * H * N` si controlla nella configurazione.
    """

    def __init__(self, larghezza: object, altezza: object, palette: object = "bande") -> None:
        w = valida_intero(larghezza, "larghezza")
        h = valida_intero(altezza, "altezza")
        if not (LARGHEZZA_MIN <= w <= LARGHEZZA_MAX):
            raise LimiteOperativoSuperato("Larghezza fuori dai limiti 1..800.")
        if not (ALTEZZA_MIN <= h <= ALTEZZA_MAX):
            raise LimiteOperativoSuperato("Altezza fuori dai limiti 1..600.")
        if not isinstance(palette, str) or palette not in PALETTE_AMMESSE:
            raise TipoNonSupportato(f"Palette non valida; ammesse: {PALETTE_AMMESSE}.")
        self.larghezza = w
        self.altezza = h
        self.palette = palette


class ParametriMandelbrot:
    """Budget di iterazioni di Mandelbrot (da completare, tappe FR-M1 e FR-M3)."""

    def __init__(self, limite_iterazioni: object = 100) -> None:
        raise NotImplementedError("FR-M1/FR-M3: validare N in 1..500 e conservarlo.")


class ParametriJulia:
    """Budget e parametro `c` di Julia (da completare, tappe FR-M1 e FR-M4)."""

    def __init__(
        self,
        limite_iterazioni: object = 100,
        c: object = complex(-0.8, 0.156),
    ) -> None:
        raise NotImplementedError("FR-M1/FR-M4: validare N e c con componenti in [-10, 10].")


class ParametriKoch:
    """Livello, variante e lato di Koch (da completare, tappe FR-M1 e FR-M2)."""

    def __init__(
        self, livello: object = 3, variante: object = "fiocco", lato_iniziale: object = 3.0
    ) -> None:
        raise NotImplementedError("FR-M1/FR-M2: validare livello 0..6, variante e lato.")


class ParametriSierpinski:
    """Livello, stile e lato di Sierpiński (da completare, tappe FR-M1 e FR-M2)."""

    def __init__(
        self, livello: object = 4, stile: object = "pieno", lato_iniziale: object = 4.0
    ) -> None:
        raise NotImplementedError("FR-M1/FR-M2: validare livello 0..7, stile e lato.")


class ConfigurazioneFrattale:
    """Composizione di famiglia, parametri, vista e immagine (da completare, FR-M1/FR-M7).

    La configurazione riunisce i valori validati, controlla il budget
    `W * H * N` delle famiglie numeriche e offre conversioni verso e da
    dizionari JSON della versione 1 (`a_dizionario`, `da_dizionario`) con
    gli stessi controlli della finestra.
    """

    def __init__(
        self, tipo_frattale: object, vista: object, immagine: object, parametri: object
    ) -> None:
        raise NotImplementedError("FR-M1/FR-M7: comporre, validare budget e convertire.")
