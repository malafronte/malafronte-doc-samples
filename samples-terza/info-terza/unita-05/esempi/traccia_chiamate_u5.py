"""Listato canonico per la traccia delle chiamate (cap. PY-08 C).

Collocare il file in `programmi/traccia_chiamate_u5.py`.
Eseguire con: uv run python programmi/traccia_chiamate_u5.py
Output atteso: 5
"""


def costo_sala(durata_min: int) -> int:
    """Restituisce il costo in euro per una durata intera da 1 a 240 minuti."""
    if durata_min <= 60:
        return 2
    if durata_min <= 120:
        return 3
    return 5


def costo_due_prenotazioni(prima_min: int, seconda_min: int) -> int:
    """Somma i costi di due prenotazioni, ciascuna di durata ammessa."""
    primo_costo = costo_sala(prima_min)
    secondo_costo = costo_sala(seconda_min)
    totale = primo_costo + secondo_costo
    return totale


risultato = costo_due_prenotazioni(30, 90)
print(risultato)
