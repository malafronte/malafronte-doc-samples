"""Casi pubblici di accettazione del laboratorio LAB-PY-U16.

I test corrispondono ai casi LAB16-01…LAB16-12 della pagina del laboratorio e
falliscono finché le parti marcate `TODO` dello starter non sono completate.
Si eseguono dalla cartella `unita-16` con:

    uv run pytest -q laboratorio/test_lista_coda_starter.py
"""

from __future__ import annotations

import pytest

from lista_coda_starter import (
    DATASET_LAB,
    CodaConcatenataStarter,
    ListaConcatenataStarter,
    client_elaborazione,
    controlla_invarianti,
)


def test_lab16_01_vuoto():
    lista = ListaConcatenataStarter()
    assert len(lista) == 0
    assert lista._testa is None and lista._coda is None
    assert lista.a_lista() == []
    with pytest.raises(IndexError):
        lista.primo()
    with pytest.raises(IndexError):
        lista.rimuovi_primo()
    assert controlla_invarianti(lista) == []  # lo stato è conservato


def test_lab16_02_primo_inserimento():
    lista = ListaConcatenataStarter()
    lista.aggiungi_in_testa(12)
    assert lista._testa is lista._coda
    assert lista._testa.successivo is None
    assert len(lista) == 1
    assert controlla_invarianti(lista) == []


def test_lab16_03_sequenza_mista():
    lista = ListaConcatenataStarter()
    lista.aggiungi_in_coda(12)
    lista.aggiungi_in_testa(7)
    lista.aggiungi_in_coda(19)
    assert lista.a_lista() == [7, 12, 19]
    assert controlla_invarianti(lista) == []


def test_lab16_04_ultima_rimozione():
    lista = ListaConcatenataStarter()
    lista.aggiungi_in_coda(12)
    assert lista.rimuovi_primo() == 12
    assert lista._testa is None and lista._coda is None
    assert controlla_invarianti(lista) == []
    lista.aggiungi_in_coda(7)  # il successivo accodamento deve funzionare
    assert lista.a_lista() == [7]


def test_lab16_05_duplicati():
    lista = ListaConcatenataStarter()
    for valore in DATASET_LAB:
        lista.aggiungi_in_coda(valore)
    assert lista.rimuovi(7) is True
    assert lista.a_lista() == [12, 7, 19]
    assert controlla_invarianti(lista) == []


def test_lab16_06_assenza():
    lista = ListaConcatenataStarter()
    for valore in DATASET_LAB:
        lista.aggiungi_in_coda(valore)
    assert lista.rimuovi(99) is False
    assert lista.a_lista() == DATASET_LAB
    assert len(lista) == 4
    assert controlla_invarianti(lista) == []


def test_lab16_07_estremi():
    dalla_testa = ListaConcatenataStarter()
    dalla_coda = ListaConcatenataStarter()
    for lista in (dalla_testa, dalla_coda):
        for valore in DATASET_LAB:
            lista.aggiungi_in_coda(valore)
    assert dalla_testa.rimuovi(12) is True  # cancellazione in testa
    assert dalla_coda.rimuovi(19) is True  # cancellazione in coda
    assert dalla_testa.a_lista() == [7, 7, 19]
    assert dalla_coda.a_lista() == [12, 7, 7]
    assert controlla_invarianti(dalla_testa) == []
    assert controlla_invarianti(dalla_coda) == []


def test_lab16_08_dati_falsi():
    lista = ListaConcatenataStarter()
    for valore in (0, False, None):
        lista.aggiungi_in_coda(valore)
    assert lista.contiene(0) is True
    assert lista.contiene(None) is True
    assert lista.a_lista() == [0, False, None]
    assert lista.rimuovi(None) is True
    assert lista.a_lista() == [0, False]
    assert controlla_invarianti(lista) == []


def test_lab16_09_fifo_intercalato():
    coda = CodaConcatenataStarter()
    coda.accoda("A")
    coda.accoda("B")
    assert coda.estrai() == "A"
    coda.accoda("C")
    assert [coda.estrai(), coda.estrai()] == ["B", "C"]
    assert coda.vuota() is True
    assert controlla_invarianti(coda._elementi) == []


def test_lab16_10_collaboratori_intercambiabili():
    atteso = ["A", "B", "C"]
    assert client_elaborazione(CodaConcatenataStarter(), ["A", "B", "C"]) == atteso
    coda_deque = CodaDequeStarter()
    assert client_elaborazione(coda_deque, ["A", "B", "C"]) == atteso
    for coda in (CodaConcatenataStarter(), CodaDequeStarter()):
        with pytest.raises(IndexError):
            coda.estrai()  # stesso comportamento sul vuoto
        with pytest.raises(IndexError):
            coda.fronte()


class CodaDequeStarter:
    """Seconda rappresentazione del caso LAB16-10: coda su `collections.deque`."""

    def __init__(self) -> None:
        from collections import deque

        self._elementi = deque()

    def __len__(self) -> int:
        return len(self._elementi)

    def vuota(self) -> bool:
        return not self._elementi

    def accoda(self, valore) -> None:
        self._elementi.append(valore)

    def estrai(self):
        if not self._elementi:
            raise IndexError("estrazione da coda vuota")
        return self._elementi.popleft()

    def fronte(self):
        if not self._elementi:
            raise IndexError("fronte di coda vuota")
        return self._elementi[0]


def test_lab16_11_indipendenza():
    prima = ListaConcatenataStarter()
    seconda = ListaConcatenataStarter()
    for valore in DATASET_LAB:
        prima.aggiungi_in_coda(valore)
        seconda.aggiungi_in_coda(valore)
    prima.rimuovi(7)
    assert seconda.a_lista() == DATASET_LAB  # la catena dell'altra è preservata
    assert controlla_invarianti(prima) == []
    assert controlla_invarianti(seconda) == []


def test_lab16_12_inversione():
    lista = ListaConcatenataStarter()
    for valore in DATASET_LAB:
        lista.aggiungi_in_coda(valore)
    nodi_prima = nodi_della_catena(lista)
    inverti_collegamenti(lista)
    assert lista.a_lista() == [19, 7, 7, 12]
    assert nodi_della_catena(lista) == list(reversed(nodi_prima))  # stessi nodi
    inverti_collegamenti(lista)
    assert lista.a_lista() == DATASET_LAB
    assert controlla_invarianti(lista) == []


def nodi_della_catena(lista: ListaConcatenataStarter) -> list[int]:
    """Restituisce gli identificativi dei nodi nell'ordine della catena."""
    identificativi = []
    corrente = lista._testa
    while corrente is not None:
        identificativi.append(id(corrente))
        corrente = corrente.successivo
    return identificativi


def inverti_collegamenti(lista: ListaConcatenataStarter) -> None:
    """Inverte i collegamenti riusando i nodi (attività guidata LAB16-12)."""
    precedente = None
    corrente = lista._testa
    lista._coda = lista._testa
    while corrente is not None:
        successivo = corrente.successivo
        corrente.successivo = precedente
        precedente = corrente
        corrente = successivo
    lista._testa = precedente
