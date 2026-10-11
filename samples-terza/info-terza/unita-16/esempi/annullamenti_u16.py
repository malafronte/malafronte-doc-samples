"""Annullamento di aggiornamenti con una pila di stati precedenti - Unità 16 (PY-24).

Problema svolto: un contatore sintetico parte da 5; ogni aggiornamento valido
conserva sulla pila il valore precedente e cambia il contatore. Con +3 e +4 lo
stato diventa 8 e poi 12; due annullamenti riportano 8 e 5. La cronologia
vuota è gestita dalla politica dichiarata: `annulla` restituisce False e
conserva il contatore.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations


class ContatoreAnnullabile:
    """Contatore intero con cronologia degli stati precedenti gestita come pila.

    Dominio degli aggiornamenti: delta intero non booleano; il risultato deve
    essere un intero non negativo. Un aggiornamento invalido solleva TypeError
    o ValueError secondo la causa e conserva sia il contatore sia la cronologia.
    """

    def __init__(self, valore_iniziale: int = 0) -> None:
        if type(valore_iniziale) is not int:
            raise TypeError("il valore iniziale deve essere un intero")
        if valore_iniziale < 0:
            raise ValueError("il valore iniziale deve essere non negativo")
        self.valore = valore_iniziale
        self._cronologia: list[int] = []

    def __repr__(self) -> str:
        return f"ContatoreAnnullabile(valore={self.valore}, annullabili={len(self._cronologia)})"

    def __len__(self) -> int:
        """Numero di annullamenti ancora disponibili."""
        return len(self._cronologia)

    def aggiorna(self, delta: int) -> None:
        """Applica `delta` al contatore dopo aver validato il nuovo risultato.

        Il valore precedente viene registrato sulla cronologia soltanto quando
        l'aggiornamento è riuscito.
        """
        if type(delta) is not int:
            raise TypeError("il delta deve essere un intero")
        nuovo = self.valore + delta
        if nuovo < 0:
            raise ValueError("il risultato dell'aggiornamento non sarebbe negativo")
        self._cronologia.append(self.valore)
        self.valore = nuovo

    def annulla(self) -> bool:
        """Ripristina il valore precedente e restituisce True.

        Con cronologia vuota restituisce False e conserva il contatore.
        """
        if not self._cronologia:
            return False
        self.valore = self._cronologia.pop()
        return True


if __name__ == "__main__":
    contatore = ContatoreAnnullabile(5)
    print("partenza:", contatore)
    contatore.aggiorna(3)
    print("dopo +3:", contatore)
    contatore.aggiorna(4)
    print("dopo +4:", contatore)
    print("annulla ->", contatore.annulla(), "stato:", contatore.valore)
    print("annulla ->", contatore.annulla(), "stato:", contatore.valore)
    print("annulla ->", contatore.annulla(), "stato:", contatore.valore)
