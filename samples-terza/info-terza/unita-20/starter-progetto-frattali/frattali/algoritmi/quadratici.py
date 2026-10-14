"""Classificatori di Mandelbrot e Julia (da completare, tappe FR-M3 e FR-M4).

Contratto: ogni funzione restituisce l'indice di fuga (`int >= 0`) oppure
`None` a budget esaurito, con controllo iniziale sul seme prima di
qualsiasi aggiornamento e confronto stretto con il raggio.

- `classifica_mandelbrot`: seme fisso `z_0 = 0`, parametro variabile `c`,
  raggio `R = 2.0` (requisito FR-02).
- `classifica_julia`: parametro `c` fisso, seme variabile `z_0`, raggio
  sicuro `R = max(2.0, |c|)` (requisito FR-03).
- `raggio_sicuro_julia`: raggio della famiglia Julia per il parametro dato.
"""


def classifica_mandelbrot(punto: object, limite_iterazioni: object):
    """Classifica il punto come parametro `c` di Mandelbrot (da completare, FR-M3)."""
    raise NotImplementedError("FR-M3: seme z_0 = 0 fisso, R = 2.0, convenzione unica.")


def classifica_julia(punto: object, parametro_c: object, limite_iterazioni: object):
    """Classifica il punto come seme di Julia (da completare, FR-M4)."""
    raise NotImplementedError("FR-M4: c fisso, R = max(2.0, |c|), convenzione unica.")


def raggio_sicuro_julia(parametro_c: object):
    """Restituisce il raggio sicuro di Julia (da completare, FR-M4)."""
    raise NotImplementedError("FR-M4: restituire max(2.0, |c|) con c validato.")
