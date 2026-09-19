"""Quindici test della sala (D01-D15). File eseguibile con pytest.

Collocare il file in `programmi/test_sala_u5.py`, accanto a `sala_u5.py`.
Comando dalla root della raccolta: uv run pytest -q programmi/test_sala_u5.py
"""

from sala_u5 import costo_sala, durata_ammessa


def test_trenta_minuti_sono_nella_prima_fascia() -> None:
    assert costo_sala(30) == 2


def test_novanta_minuti_sono_nella_seconda_fascia() -> None:
    assert costo_sala(90) == 3


def test_centottanta_minuti_sono_nella_terza_fascia() -> None:
    assert costo_sala(180) == 5


def test_un_minuto_e_il_minimo_ammesso() -> None:
    assert costo_sala(1) == 2


def test_cinquantanove_minuti_sono_prima_della_soglia() -> None:
    assert costo_sala(59) == 2


def test_sessanta_minuti_restano_nella_prima_fascia() -> None:
    assert costo_sala(60) == 2


def test_sessantuno_minuti_passano_alla_seconda_fascia() -> None:
    assert costo_sala(61) == 3


def test_centoventi_minuti_restano_nella_seconda_fascia() -> None:
    assert costo_sala(120) == 3


def test_centoventuno_minuti_passano_alla_terza_fascia() -> None:
    assert costo_sala(121) == 5


def test_duecentoquaranta_minuti_sono_il_massimo_ammesso() -> None:
    assert costo_sala(240) == 5


def test_meno_uno_non_e_ammesso() -> None:
    assert durata_ammessa(-1) is False


def test_zero_non_e_ammesso() -> None:
    assert durata_ammessa(0) is False


def test_uno_e_il_minimo_ammesso() -> None:
    assert durata_ammessa(1) is True


def test_duecentoquaranta_e_il_massimo_ammesso() -> None:
    assert durata_ammessa(240) is True


def test_duecentoquarantuno_non_e_ammesso() -> None:
    assert durata_ammessa(241) is False
