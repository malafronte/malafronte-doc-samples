"""Suite del laboratorio LAB-PY-U6 — versione di partenza.

Stato iniziale dichiarato: un solo test completo di riferimento, su
`fattoriale_iterativo` fornito dallo starter. Il test `test_fattoriale_ric_confini`
richiama `fattoriale_ric`, che ancora non esiste in ricorsione_u6.py:
l'errore è il primo esito atteso dello starter e sparirà nella fase L2,
quando la funzione sarà implementata. Gli altri test delle fasi L2-L5
si aggiungono in coda, uno per comportamento da verificare.
Comando dalla root della raccolta:
uv run pytest -q programmi/test_ricorsione_u6.py
"""

from ricorsione_u6 import fattoriale_iterativo


def test_fattoriale_iterativo_confini() -> None:
    """L01, parte iterativa: 0 -> 1, 1 -> 1, 5 -> 120."""
    assert fattoriale_iterativo(0) == 1
    assert fattoriale_iterativo(1) == 1
    assert fattoriale_iterativo(5) == 120


def test_fattoriale_ric_confini() -> None:
    """L01, parte ricorsiva: da attivare nella fase L2 dopo l'implementazione."""
    from ricorsione_u6 import fattoriale_ric

    assert fattoriale_ric(0) == 1
    assert fattoriale_ric(1) == 1
    assert fattoriale_ric(5) == 120
