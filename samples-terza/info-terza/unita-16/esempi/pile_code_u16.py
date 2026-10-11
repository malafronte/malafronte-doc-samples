"""Pile LIFO e code FIFO con quattro rappresentazioni - Unità 16 (PY-31).

Le classi `PilaLista`, `PilaConcatenata`, `CodaDeque` e `CodaConcatenata`
espongono lo stesso contratto didattico:

- pila: `inserisci`, `estrai`, `cima`, `vuota`, `len`;
- coda: `accoda`, `estrai`, `fronte`, `vuota`, `len`.

Sul vuoto `estrai` e `cima`/`fronte` sollevano `IndexError` e conservano lo
stato. La cima della pila con lista Python è l'estremo destro; il fronte della
coda con `deque` è l'estremo sinistro.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations

from collections import deque

from lista_concatenata_u16 import ListaConcatenata


class PilaLista:
    """Pila LIFO costruita sulla lista Python: la cima è l'ultimo elemento."""

    def __init__(self) -> None:
        self._elementi: list = []

    def __len__(self) -> int:
        return len(self._elementi)

    def __repr__(self) -> str:
        return f"PilaLista({self._elementi!r})"

    def vuota(self) -> bool:
        """Restituisce True quando la pila non contiene elementi."""
        return not self._elementi

    def inserisci(self, valore) -> None:
        """Colloca `valore` sulla cima della pila."""
        self._elementi.append(valore)

    def estrai(self):
        """Rimuove e restituisce il valore in cima; su vuoto solleva IndexError."""
        if not self._elementi:
            raise IndexError("estrazione da pila vuota")
        return self._elementi.pop()

    def cima(self):
        """Restituisce il valore in cima conservando la pila; su vuoto solleva IndexError."""
        if not self._elementi:
            raise IndexError("cima di pila vuota")
        return self._elementi[-1]


class PilaConcatenata:
    """Pila LIFO costruita sulla lista concatenata: inserimento ed estrazione in testa."""

    def __init__(self) -> None:
        self._elementi = ListaConcatenata()

    def __len__(self) -> int:
        return len(self._elementi)

    def __repr__(self) -> str:
        return f"PilaConcatenata({self._elementi.a_lista()!r})"

    def vuota(self) -> bool:
        """Restituisce True quando la pila non contiene elementi."""
        return len(self._elementi) == 0

    def inserisci(self, valore) -> None:
        """Colloca `valore` sulla cima della pila."""
        self._elementi.aggiungi_in_testa(valore)

    def estrai(self):
        """Rimuove e restituisce il valore in cima; su vuoto solleva IndexError."""
        return self._elementi.rimuovi_primo()

    def cima(self):
        """Restituisce il valore in cima conservando la pila; su vuoto solleva IndexError."""
        return self._elementi.primo()


class CodaDeque:
    """Coda FIFO costruita su `collections.deque`: fronte a sinistra, accodamento a destra."""

    def __init__(self) -> None:
        self._elementi: deque = deque()

    def __len__(self) -> int:
        return len(self._elementi)

    def __repr__(self) -> str:
        return f"CodaDeque({list(self._elementi)!r})"

    def vuota(self) -> bool:
        """Restituisce True quando la coda non contiene elementi."""
        return not self._elementi

    def accoda(self, valore) -> None:
        """Colloca `valore` in coda, dopo tutti gli elementi pendenti."""
        self._elementi.append(valore)

    def estrai(self):
        """Rimuove e restituisce il valore al fronte; su vuoto solleva IndexError."""
        if not self._elementi:
            raise IndexError("estrazione da coda vuota")
        return self._elementi.popleft()

    def fronte(self):
        """Restituisce il valore al fronte conservando la coda; su vuoto solleva IndexError."""
        if not self._elementi:
            raise IndexError("fronte di coda vuota")
        return self._elementi[0]


class CodaConcatenata:
    """Coda FIFO costruita sulla lista concatenata, con accodamento in coda e rimozione in testa."""

    def __init__(self) -> None:
        self._elementi = ListaConcatenata()

    def __len__(self) -> int:
        return len(self._elementi)

    def __repr__(self) -> str:
        return f"CodaConcatenata({self._elementi.a_lista()!r})"

    def vuota(self) -> bool:
        """Restituisce True quando la coda non contiene elementi."""
        return len(self._elementi) == 0

    def accoda(self, valore) -> None:
        """Colloca `valore` in coda, dopo tutti gli elementi pendenti."""
        self._elementi.aggiungi_in_coda(valore)

    def estrai(self):
        """Rimuove e restituisce il valore al fronte; su vuoto solleva IndexError."""
        return self._elementi.rimuovi_primo()

    def fronte(self):
        """Restituisce il valore al fronte conservando la coda; su vuoto solleva IndexError."""
        return self._elementi.primo()


def client_comune(collaboratore, valori: list) -> list:
    """Accoda o inserisce `valori` in ordine, poi estrae finché la struttura è vuota.

    Il client accetta qualunque collaboratore compatibile con il contratto:
    per una pila usa `inserisci`, per una coda `accoda`. Le due famiglie
    restituiscono ordini di estrazione diversi dallo stesso ingresso.
    """
    inserisci = getattr(collaboratore, "inserisci", None) or collaboratore.accoda
    for valore in valori:
        inserisci(valore)
    estratti = []
    while not collaboratore.vuota():
        estratti.append(collaboratore.estrai())
    return estratti
