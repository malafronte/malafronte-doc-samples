"""Operazioni sui numeri complessi con `complex` e con coppie di reali — Unità 20 (L3).

Il modulo implementa gli esempi preparatori dei nuclei A–E del capitolo PY-38
(*Numeri complessi e iterazioni nel piano*):

- costruzione di un numero complesso da due campi reali (come quelli della
  futura GUI) con `complex(parte_reale, parte_immaginaria)` e lettura delle
  componenti con `.real` e `.imag`;
- somma, sottrazione, prodotto, quadrato e modulo calcolati sia con il tipo
  `complex` di Python sia con coppie `(a, b)` di numeri reali, così da
  confrontare le due strade con la tolleranza `1e-12` dei contratti L1;
- la regola dell'aggiornamento simultaneo: nella versione su coppie di reali
  entrambe le componenti del risultato si calcolano dai valori iniziali,
  conservati prima di qualsiasi assegnazione (errore PY-U20-E02).

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O
né apre finestre grafiche all'importazione.
"""

import math

from dati_canonici import TOLLERANZA_COMPLESSI, valida_reale_finito

type CoppiaReale = tuple[float, float]


def valida_complesso_finito(valore: object, nome_parametro: str) -> complex:
    """Verifica che `valore` sia un numero finito e lo restituisce come `complex`.

    Accetta `complex`, `float` e `int` non booleani; i reali diventano complessi
    con parte immaginaria nulla. Rifiuta i booleani (`True` è istanza di `int`)
    e qualsiasi valore con componenti non finite (`nan`, `inf`).
    """
    if isinstance(valore, bool):
        raise TypeError(f"Il parametro '{nome_parametro}' richiede un numero finito.")
    if isinstance(valore, complex):
        risultato = valore
    elif isinstance(valore, (int, float)):
        risultato = complex(valore, 0.0)
    else:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede un numero finito.")
    if not (math.isfinite(risultato.real) and math.isfinite(risultato.imag)):
        raise ValueError(f"Le componenti del parametro '{nome_parametro}' devono essere finite.")
    return risultato


def valida_coppia_reale(valore: object, nome_parametro: str) -> CoppiaReale:
    """Verifica che `valore` sia una coppia `(a, b)` di reali finiti non booleani."""
    if not isinstance(valore, (tuple, list)) or len(valore) != 2:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede una coppia (a, b).")
    a = valida_reale_finito(valore[0], f"{nome_parametro}[0]")
    b = valida_reale_finito(valore[1], f"{nome_parametro}[1]")
    return (a, b)


def costruisci_complesso(parte_reale: object, parte_immaginaria: object) -> complex:
    """Costruisce `complex(a, b)` dai due valori reali `a` e `b`.

    Replica la costruzione usata dalla futura GUI, che legge le componenti
    di `c` da due campi di testo e le converte prima di chiamare `complex`.
    """
    a = valida_reale_finito(parte_reale, "parte_reale")
    b = valida_reale_finito(parte_immaginaria, "parte_immaginaria")
    return complex(a, b)


def parti(z: object) -> CoppiaReale:
    """Restituisce la coppia `(z.real, z.imag)` delle componenti di `z`."""
    numero = valida_complesso_finito(z, "z")
    return (numero.real, numero.imag)


def somma_complessi(z_1: object, z_2: object) -> complex:
    """Restituisce `(a + u) + (b + v)i` per `z_1 = a + bi` e `z_2 = u + vi`."""
    primo = valida_complesso_finito(z_1, "z_1")
    secondo = valida_complesso_finito(z_2, "z_2")
    return primo + secondo


def differenza_complessi(z_1: object, z_2: object) -> complex:
    """Restituisce `(a - u) + (b - v)i` per `z_1 = a + bi` e `z_2 = u + vi`."""
    primo = valida_complesso_finito(z_1, "z_1")
    secondo = valida_complesso_finito(z_2, "z_2")
    return primo - secondo


def prodotto_complessi(z_1: object, z_2: object) -> complex:
    """Restituisce `(au - bv) + (av + bu)i`, con `i^2 = -1`.

    Esempio canonico: `(1 + 2i)(3 - i) = (3 + 2) + (-1 + 6)i = 5 + 5i`.
    """
    primo = valida_complesso_finito(z_1, "z_1")
    secondo = valida_complesso_finito(z_2, "z_2")
    return primo * secondo


def quadrato_complesso(z: object) -> complex:
    """Restituisce `(a^2 - b^2) + 2abi`, quadrato di `z = a + bi`.

    Esempio fondamentale: `(1 + 2i)^2 = (1 - 4) + 2(1)(2)i = -3 + 4i`.
    """
    numero = valida_complesso_finito(z, "z")
    return numero * numero


def modulo_complesso(z: object) -> float:
    """Restituisce `|z| = sqrt(a^2 + b^2)`, distanza di `z` dall'origine.

    Esempio esatto: `|3 + 4i| = sqrt(9 + 16) = 5.0`.
    """
    numero = valida_complesso_finito(z, "z")
    return abs(numero)


def modulo_quadro_complesso(z: object) -> float:
    """Restituisce `|z|^2 = a^2 + b^2`, confrontabile con `R^2` senza radice."""
    numero = valida_complesso_finito(z, "z")
    return numero.real**2 + numero.imag**2


def somma_coppie(z_1: object, z_2: object) -> CoppiaReale:
    """Somma per componenti: `(a, b) + (u, v) = (a + u, b + v)`."""
    a, b = valida_coppia_reale(z_1, "z_1")
    u, v = valida_coppia_reale(z_2, "z_2")
    return (a + u, b + v)


def differenza_coppie(z_1: object, z_2: object) -> CoppiaReale:
    """Sottrazione per componenti: `(a, b) - (u, v) = (a - u, b - v)`."""
    a, b = valida_coppia_reale(z_1, "z_1")
    u, v = valida_coppia_reale(z_2, "z_2")
    return (a - u, b - v)


def prodotto_coppie(z_1: object, z_2: object) -> CoppiaReale:
    """Prodotto su reali: `(a, b)(u, v) = (au - bv, av + bu)`."""
    a, b = valida_coppia_reale(z_1, "z_1")
    u, v = valida_coppia_reale(z_2, "z_2")
    return (a * u - b * v, a * v + b * u)


def quadrato_coppia(z: object) -> CoppiaReale:
    """Quadrato su reali: `(a, b)^2 = (a^2 - b^2, 2ab)`.

    Entrambe le componenti del risultato usano i valori iniziali `a` e `b`:
    aggiornare `a` e usare subito il nuovo valore per calcolare la parte
    immaginaria produrrebbe un risultato diverso (errore PY-U20-E02).
    """
    a, b = valida_coppia_reale(z, "z")
    return (a * a - b * b, 2.0 * a * b)


def modulo_coppia(z: object) -> float:
    """Modulo da coppia di reali: `|(a, b)| = sqrt(a^2 + b^2)`."""
    a, b = valida_coppia_reale(z, "z")
    return math.hypot(a, b)


def concorda_con_complex(z_coppia: object, z_complex: object) -> bool:
    """Confronta una coppia `(a, b)` con un `complex` entro `1e-12`.

    La tolleranza è `TOLLERANZA_COMPLESSI` dei contratti L1: i confronti fra
    esiti a virgola mobile usano la tolleranza, mentre i conteggi di passi e
    gli indici restano interi esatti.
    """
    a, b = valida_coppia_reale(z_coppia, "z_coppia")
    numero = valida_complesso_finito(z_complex, "z_complex")
    return abs(complex(a, b) - numero) < TOLLERANZA_COMPLESSI


if __name__ == "__main__":
    z = costruisci_complesso(1.0, 2.0)
    print("z =", z, "| parti =", parti(z))
    print("z^2 =", quadrato_complesso(z), "| su reali =", quadrato_coppia((1.0, 2.0)))
    print("|3 + 4i| =", modulo_complesso(complex(3.0, 4.0)))
