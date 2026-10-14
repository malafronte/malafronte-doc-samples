"""Kernel a tempo di fuga per Mandelbrot e Julia — Unità 20 (L4).

Il modulo implementa gli esempi preparatori dei nuclei E–G del capitolo PY-39
(*Mandelbrot e Julia: algoritmi a tempo di fuga*):

- l'esito `EsitoFuga` con `indice_fuga: int | None` (`None` indica fuga non
  rilevata entro il budget, distinto dall'indice `0` di fuga immediata),
  numero di aggiornamenti eseguiti e valore finale;
- il kernel `esito_fuga` su `complex` con l'ordine esatto del contratto L1:
  controllo iniziale su `z_0` (passo `0`, zero aggiornamenti), poi per
  `n = 1, ..., N` aggiornamento `z = z * z + c` seguito dal confronto
  stretto `|z| > R`;
- l'oracolo `esito_fuga_reali` sulle due componenti con aggiornamento
  simultaneo e confronto sul quadrato del modulo, per il confronto
  `complex` contro reali richiesto dal piano (§18.1);
- le chiamate `esito_mandelbrot` (seme `z_0 = 0` fisso, parametro `c`
  variabile, `R = 2.0`) ed `esito_julia` (parametro `c` fisso, seme `z_0`
  variabile, `R = max(2.0, |c|)`);
- il raggio sicuro `raggio_fuga_julia`, che preserva il punto fisso
  `z_0 = 3` per `c = -6` (caso J-05).

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O
né apre finestre grafiche all'importazione.
"""

from dataclasses import dataclass

from complessi_esempi import valida_complesso_finito
from dati_canonici import valida_intero_non_booleano, valida_reale_finito

RAGGIO_FUGA_MANDELBROT: float = 2.0


@dataclass(frozen=True)
class EsitoFuga:
    """Risultato del kernel a tempo di fuga (stessa forma di `EsitoFugaCanonico` L1).

    Il campo `indice_fuga` vale `0 <= n <= limite_iterazioni` se il modulo
    supera strettamente il raggio al passo `n` (`0` indica superamento già su
    `z_0`, con zero aggiornamenti); vale `None` se dopo tutti gli `N`
    aggiornamenti il modulo non ha mai superato strettamente il raggio.
    """

    indice_fuga: int | None
    aggiornamenti_eseguiti: int
    valore_finale: complex


def valida_limite_iterazioni(valore: object) -> int:
    """Verifica che `valore` sia un intero non booleano maggiore o uguale a 1."""
    return valida_intero_non_booleano(valore, "limite_iterazioni", minimo=1)


def valida_raggio_fuga(valore: object) -> float:
    """Verifica che `valore` sia un reale finito strettamente positivo."""
    raggio = valida_reale_finito(valore, "raggio_fuga")
    if raggio <= 0.0:
        raise ValueError("Il parametro 'raggio_fuga' richiede un valore positivo.")
    return raggio


def raggio_fuga_julia(c: object) -> float:
    """Restituisce il raggio sicuro `max(2.0, |c|)` per l'insieme di Julia.

    Per `c = -6` il raggio vale `6.0`: il punto `z_0 = 3` è un punto fisso
    (`3^2 - 6 = 3`) e non viene classificato come fuga (caso J-05). Usare
    sempre il raggio `2.0` anche per Julia lo classificherebbe
    erroneamente come fuga al passo `0` (errore PY-U20-E04).
    """
    parametro = valida_complesso_finito(c, "c")
    return max(RAGGIO_FUGA_MANDELBROT, abs(parametro))


def esito_fuga(
    z_iniziale: object,
    c: object,
    limite_iterazioni: object,
    raggio_fuga: object,
) -> EsitoFuga:
    """Classifica un punto con il kernel a tempo di fuga su `complex`.

    Ordine esatto del contratto: prima valida gli input, poi controlla il
    valore iniziale `z_0` (fuga al passo `0` con zero aggiornamenti se
    `|z_0| > R`); quindi per `n = 1, ..., N` aggiorna `z = z * z + c` e
    controlla `|z| > R` al primo superamento; se il budget si esaurisce
    senza superamento restituisce `indice_fuga = None` con `N` aggiornamenti.
    Il confronto con la soglia è stretto (`>`): un modulo uguale al raggio
    non costituisce fuga (caso M-03).
    """
    z = valida_complesso_finito(z_iniziale, "z_iniziale")
    parametro = valida_complesso_finito(c, "c")
    n_max = valida_limite_iterazioni(limite_iterazioni)
    raggio = valida_raggio_fuga(raggio_fuga)

    if abs(z) > raggio:
        return EsitoFuga(indice_fuga=0, aggiornamenti_eseguiti=0, valore_finale=z)

    for passo in range(1, n_max + 1):
        z = z * z + parametro
        if abs(z) > raggio:
            return EsitoFuga(indice_fuga=passo, aggiornamenti_eseguiti=passo, valore_finale=z)

    return EsitoFuga(indice_fuga=None, aggiornamenti_eseguiti=n_max, valore_finale=z)


def esito_fuga_reali(
    x_iniziale: object,
    y_iniziale: object,
    c_reale: object,
    c_immaginaria: object,
    limite_iterazioni: object,
    raggio_fuga: object,
) -> EsitoFuga:
    """Oracolo indipendente del kernel sulle due componenti reali.

    Applica lo stesso ordine di controllo e aggiornamento senza usare il tipo
    `complex`: aggiornamento simultaneo `x_nuovo = x^2 - y^2 + c_x`,
    `y_nuovo = 2xy + c_y` e confronto stretto sul quadrato del modulo
    `x^2 + y^2 > R^2`. Gli esiti coincidono con quelli di `esito_fuga`
    entro la tolleranza dei complessi sui valori finali non esatti.
    """
    x = valida_reale_finito(x_iniziale, "x_iniziale")
    y = valida_reale_finito(y_iniziale, "y_iniziale")
    cx = valida_reale_finito(c_reale, "c_reale")
    cy = valida_reale_finito(c_immaginaria, "c_immaginaria")
    n_max = valida_limite_iterazioni(limite_iterazioni)
    raggio = valida_raggio_fuga(raggio_fuga)

    soglia_quadrata = raggio * raggio
    if x * x + y * y > soglia_quadrata:
        return EsitoFuga(indice_fuga=0, aggiornamenti_eseguiti=0, valore_finale=complex(x, y))

    for passo in range(1, n_max + 1):
        x_nuovo = x * x - y * y + cx
        y_nuovo = 2.0 * x * y + cy
        x, y = x_nuovo, y_nuovo
        if x * x + y * y > soglia_quadrata:
            return EsitoFuga(
                indice_fuga=passo,
                aggiornamenti_eseguiti=passo,
                valore_finale=complex(x, y),
            )

    return EsitoFuga(indice_fuga=None, aggiornamenti_eseguiti=n_max, valore_finale=complex(x, y))


def esito_mandelbrot(c: object, limite_iterazioni: object) -> EsitoFuga:
    """Classifica il parametro `c` di Mandelbrot: seme `z_0 = 0`, `R = 2.0`.

    Ogni punto dell'immagine di Mandelbrot fornisce un parametro diverso; il
    seme resta zero. Il raggio `2.0` è fisso per la famiglia.
    """
    parametro = valida_complesso_finito(c, "c")
    n_max = valida_limite_iterazioni(limite_iterazioni)
    return esito_fuga(0.0j, parametro, n_max, RAGGIO_FUGA_MANDELBROT)


def esito_julia(z_iniziale: object, c: object, limite_iterazioni: object) -> EsitoFuga:
    """Classifica il seme `z_0` di Julia: parametro `c` fisso, `R = max(2, |c|)`.

    Ogni punto dell'immagine di Julia fornisce un seme diverso; il parametro
    resta quello dell'immagine. Il raggio sicuro dipende da `c`.
    """
    z_0 = valida_complesso_finito(z_iniziale, "z_iniziale")
    parametro = valida_complesso_finito(c, "c")
    n_max = valida_limite_iterazioni(limite_iterazioni)
    return esito_fuga(z_0, parametro, n_max, raggio_fuga_julia(parametro))


def fuga_rilevata(esito: EsitoFuga) -> bool:
    """Restituisce `True` se l'esito registra una fuga entro il budget.

    Il controllo usa l'identità con `None`: l'indice `0` è una fuga valida
    (immediata) e non va confuso con l'assenza di fuga (errore PY-U20-E03).
    """
    if not isinstance(esito, EsitoFuga):
        raise TypeError("Il parametro 'esito' richiede un EsitoFuga.")
    return esito.indice_fuga is not None


if __name__ == "__main__":
    for codice, z_0, c, n_max, raggio in [
        ("M-04", 0.0j, 1.0 + 0.0j, 2, 2.0),
        ("M-05", 0.0j, 1.0 + 0.0j, 3, 2.0),
        ("J-04", 3.0 + 0.0j, 0.0j, 10, 2.0),
        ("J-05", 3.0 + 0.0j, -6.0 + 0.0j, 10, 6.0),
    ]:
        print(codice, esito_fuga(z_0, c, n_max, raggio))
