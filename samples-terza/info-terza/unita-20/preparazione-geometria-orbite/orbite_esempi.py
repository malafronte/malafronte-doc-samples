"""Iterazione quadratica `z_{n+1} = z_n^2 + c` e tabelle di orbita — Unità 20 (L3).

Il modulo implementa gli esempi preparatori dei nuclei F–G del capitolo PY-38
(*Numeri complessi e iterazioni nel piano*):

- un passo dell'iterazione quadratica `f_c(z) = z^2 + c`, sia con il tipo
  `complex` sia con coppie `(x, y)` di reali ad aggiornamento simultaneo;
- la traccia d'orbita `z_0, z_1, ..., z_n` da un valore iniziale dichiarato,
  dove l'indice `n` conta gli aggiornamenti già eseguiti;
- la tabella d'orbita con indice, valore e modulo di ogni termine, usata dal
  problema svolto del capitolo per confrontare ciascun modulo con la soglia
  `2` prima della motivazione matematica delle soglie in PY-39.

La classificazione dei punti (fuga rilevata oppure non rilevata entro il
budget `N`) appartiene al kernel di fuga del lotto L4: questo modulo costruisce
e mostra le orbite, senza classificarle.

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O
né apre finestre grafiche all'importazione.
"""

from complessi_esempi import (
    CoppiaReale,
    valida_complesso_finito,
    valida_coppia_reale,
)
from dati_canonici import valida_intero_non_booleano


def valida_numero_passi(numero_passi: object) -> int:
    """Verifica che `numero_passi` sia un intero non booleano maggiore o uguale a zero."""
    return valida_intero_non_booleano(numero_passi, "numero_passi", minimo=0)


def passo_quadratico(z: object, c: object) -> complex:
    """Restituisce un passo dell'iterazione: `f_c(z) = z^2 + c`."""
    valore = valida_complesso_finito(z, "z")
    parametro = valida_complesso_finito(c, "c")
    return valore * valore + parametro


def passo_quadratico_coppia(z: object, c: object) -> CoppiaReale:
    """Restituisce un passo dell'iterazione su coppie di reali.

    Da `(x, y)` con parametro `(cx, cy)` produce
    `(x^2 - y^2 + cx, 2xy + cy)`, calcolando entrambe le componenti dai valori
    iniziali `x` e `y`, conservati prima di qualsiasi assegnazione.
    """
    x, y = valida_coppia_reale(z, "z")
    cx, cy = valida_coppia_reale(c, "c")
    return (x * x - y * y + cx, 2.0 * x * y + cy)


def traccia_orbita(z_iniziale: object, c: object, numero_passi: object) -> tuple[complex, ...]:
    """Restituisce la tupla `(z_0, z_1, ..., z_n)` con `n = numero_passi` aggiornamenti.

    La traccia contiene `numero_passi + 1` termini: il valore iniziale
    dichiarato `z_0` seguito da un termine per ogni aggiornamento eseguito.
    Con `numero_passi = 0` restituisce la tupla con il solo valore iniziale.
    """
    z_0 = valida_complesso_finito(z_iniziale, "z_iniziale")
    parametro = valida_complesso_finito(c, "c")
    n = valida_numero_passi(numero_passi)
    termini: list[complex] = [z_0]
    for _ in range(n):
        termini.append(termini[-1] * termini[-1] + parametro)
    return tuple(termini)


def traccia_orbita_coppia(
    z_iniziale: object, c: object, numero_passi: object
) -> tuple[CoppiaReale, ...]:
    """Restituisce la traccia d'orbita come tupla di coppie `(x, y)` di reali.

    Oracolo indipendente della versione su `complex`: applica lo stesso
    aggiornamento simultaneo senza usare il tipo `complex`. Le due tracce
    coincidono entro `TOLLERANZA_COMPLESSI` (confronto PY-U20-X01).
    """
    x_0, y_0 = valida_coppia_reale(z_iniziale, "z_iniziale")
    cx, cy = valida_coppia_reale(c, "c")
    n = valida_numero_passi(numero_passi)
    termini: list[CoppiaReale] = [(x_0, y_0)]
    for _ in range(n):
        x, y = termini[-1]
        termini.append((x * x - y * y + cx, 2.0 * x * y + cy))
    return tuple(termini)


def tabella_orbita(z_iniziale: object, c: object, numero_passi: object) -> list[dict[str, object]]:
    """Costruisce la tabella d'orbita: una riga per ogni termine della traccia.

    Ogni riga è un dizionario con chiavi `"indice"` (`int`, numero di
    aggiornamenti già eseguiti), `"valore"` (`complex`, il termine `z_n`) e
    `"modulo"` (`float`, `|z_n|` da confrontare con la soglia `2`).
    La tabella contiene `numero_passi + 1` righe, inclusa la riga iniziale
    con indice `0`.
    """
    traccia = traccia_orbita(z_iniziale, c, numero_passi)
    righe: list[dict[str, object]] = []
    for indice, valore in enumerate(traccia):
        righe.append({"indice": indice, "valore": valore, "modulo": abs(valore)})
    return righe


def modulo_massimo_traccia(traccia: object) -> float:
    """Restituisce il massimo dei moduli dei termini della traccia data."""
    if not isinstance(traccia, (tuple, list)) or len(traccia) == 0:
        raise ValueError("Il parametro 'traccia' richiede una sequenza non vuota di valori.")
    moduli = [abs(valida_complesso_finito(valore, "traccia[...]")) for valore in traccia]
    return max(moduli)


if __name__ == "__main__":
    for parametro in (0.0j, -1.0 + 0.0j, 1.0 + 0.0j, 1.0j):
        traccia = traccia_orbita(0.0j, parametro, 4)
        print(f"c = {parametro}: {[str(z) for z in traccia]}")
