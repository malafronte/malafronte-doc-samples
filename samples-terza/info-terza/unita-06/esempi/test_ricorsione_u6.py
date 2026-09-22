"""Suite di riferimento dei sorgenti d'esempio dell'Unità 6.

Collocare il file in `programmi/test_ricorsione_u6.py`, accanto a
ricorsione_lineare_u6.py, fibonacci_u6.py e hanoi_u6.py.
Comando dalla root della raccolta:
uv run pytest -q programmi/test_ricorsione_u6.py

La suite copre i casi pubblici dei tre capitoli: confini delle funzioni
lineari, concordanza delle due versioni di Fibonacci, sequenze ed effetti
del generatore di Hanoi. È il riferimento degli esempi già svolti, distinta
dalla consegna autonoma del laboratorio.
"""

from fibonacci_u6 import fibonacci_iter, fibonacci_ric
from hanoi_u6 import hanoi
from ricorsione_lineare_u6 import fattoriale_iter, fattoriale_ric, mcd_ric, somma_ric


def test_fattoriale_confini() -> None:
    assert fattoriale_ric(0) == 1
    assert fattoriale_ric(1) == 1
    assert fattoriale_ric(3) == 6
    assert fattoriale_ric(5) == 120


def test_fattoriale_ric_e_iter_concordano() -> None:
    for n in range(11):
        assert fattoriale_ric(n) == fattoriale_iter(n)


def test_somma_confini() -> None:
    assert somma_ric(0) == 0
    assert somma_ric(1) == 1
    assert somma_ric(4) == 10
    assert somma_ric(10) == 55


def test_mcd_casi_pubblici() -> None:
    assert mcd_ric(48, 18) == 6
    assert mcd_ric(7, 0) == 7
    assert mcd_ric(0, 7) == 7
    assert mcd_ric(7, 7) == 7
    assert mcd_ric(12, 18) == 6
    assert mcd_ric(13, 8) == 1


def test_fibonacci_confini_entrambe_le_versioni() -> None:
    attesi = [0, 1, 1, 2, 3, 5, 8, 13, 21]
    for n, atteso in enumerate(attesi):
        assert fibonacci_ric(n) == atteso
        assert fibonacci_iter(n) == atteso
    assert fibonacci_ric(10) == 55
    assert fibonacci_iter(10) == 55


def test_hanoi_zero_dischi_non_accoda_nulla() -> None:
    mosse = []
    assert hanoi(0, "A", "C", "B", mosse) is None
    assert mosse == []


def test_hanoi_un_disco() -> None:
    mosse = []
    hanoi(1, "A", "C", "B", mosse)
    assert mosse == [(1, "A", "C")]


def test_hanoi_due_dischi() -> None:
    mosse = []
    hanoi(2, "A", "C", "B", mosse)
    assert mosse == [(1, "A", "B"), (2, "A", "C"), (1, "B", "C")]


def test_hanoi_tre_dischi() -> None:
    mosse = []
    hanoi(3, "A", "C", "B", mosse)
    assert mosse == [
        (1, "A", "C"),
        (2, "A", "B"),
        (1, "C", "B"),
        (3, "A", "C"),
        (1, "B", "A"),
        (2, "B", "C"),
        (1, "A", "C"),
    ]


def test_hanoi_pioli_rinominati() -> None:
    mosse = []
    hanoi(2, "C", "B", "A", mosse)
    assert mosse == [(1, "C", "A"), (2, "C", "B"), (1, "A", "B")]


def test_hanoi_prefisso_conservato() -> None:
    mosse = [(9, "X", "Y")]
    hanoi(1, "A", "C", "B", mosse)
    assert mosse == [(9, "X", "Y"), (1, "A", "C")]


def test_hanoi_liste_indipendenti() -> None:
    prima = []
    seconda = []
    hanoi(2, "A", "C", "B", prima)
    hanoi(2, "A", "C", "B", seconda)
    assert prima == seconda
    assert prima is not seconda
    terza = []
    hanoi(2, "A", "C", "B", terza)
    assert terza == [(1, "A", "B"), (2, "A", "C"), (1, "B", "C")]
    assert prima == [(1, "A", "B"), (2, "A", "C"), (1, "B", "C")]
