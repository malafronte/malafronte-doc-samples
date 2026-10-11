"""Array dinamico nel modello a raddoppio - Unità 16 (PY-23), sezioni B-C.

Il modulo simula un array dinamico di riferimenti con la politica didattica
dichiarata: capacità iniziale 2, raddoppio quando lo spazio è completo, copia
dei riferimenti presenti, poi scrittura del nuovo elemento. Il conteggio separa
le copie dei riferimenti occupati dalle scritture dei nuovi valori.

Il modello è una scelta didattica: CPython usa una propria politica di
sovrallocazione, da verificare sulla versione adottata.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ArrayDinamicoModello:
    """Array dinamico di riferimenti con ridimensionamento a raddoppio dichiarato.

    L'array `riferimenti` riserva `capacita` posti; i primi `dimensione` sono
    occupati dagli elementi presenti, gli altri restano disponibili per le
    aggiunte successive.
    """

    capacita_iniziale: int = 2
    riferimenti: list = field(init=False)
    capacita: int = field(init=False)
    copie_riferimenti: int = field(default=0, init=False)
    scritture_valore: int = field(default=0, init=False)
    _dimensione: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if type(self.capacita_iniziale) is not int or self.capacita_iniziale < 1:
            raise ValueError("la capacità iniziale deve essere un intero almeno 1")
        self.capacita = self.capacita_iniziale
        self.riferimenti = [None] * self.capacita

    @property
    def dimensione(self) -> int:
        """Lunghezza logica: numero di elementi presenti."""
        return self._dimensione

    def posti_riservati(self) -> int:
        """Posti dell'array attualmente disponibili, occupati e non."""
        return self.capacita

    def a_lista(self) -> list:
        """Restituisce i valori presenti nell'ordine dell'array."""
        return self.riferimenti[: self._dimensione]

    def appendi(self, valore) -> None:
        """Aggiunge `valore` in coda; ridimensiona prima quando lo spazio è completo."""
        if self._dimensione == self.capacita:
            self._ridimensiona(self.capacita * 2)
        self.riferimenti[self._dimensione] = valore
        self.scritture_valore += 1
        self._dimensione += 1

    def _ridimensiona(self, nuova_capacita: int) -> None:
        """Alloca lo spazio nuovo e copia i riferimenti occupati."""
        nuovo_array = [None] * nuova_capacita
        for indice in range(self._dimensione):
            nuovo_array[indice] = self.riferimenti[indice]
            self.copie_riferimenti += 1
        self.riferimenti = nuovo_array
        self.capacita = nuova_capacita

    def totale_unita_di_lavoro(self) -> int:
        """Somma del modello: copie dei riferimenti più scritture dei nuovi valori."""
        return self.copie_riferimenti + self.scritture_valore


def traccia_accodamenti(quanti: int = 10, capacita_iniziale: int = 2) -> list[dict]:
    """Esegue `quanti` accodamenti e restituisce una riga di traccia per operazione.

    Ogni riga registra: numero dell'operazione, lunghezza e capacità prima,
    riferimenti copiati e scrittura del nuovo valore durante l'operazione,
    lunghezza e capacità dopo.
    """
    array = ArrayDinamicoModello(capacita_iniziale=capacita_iniziale)
    traccia = []
    for numero in range(1, quanti + 1):
        lunghezza_prima = array.dimensione
        capacita_prima = array.capacita
        copie_prima = array.copie_riferimenti
        array.appendi(numero * 10)  # valori sintetici: 10, 20, 30, ...
        traccia.append(
            {
                "operazione": numero,
                "lunghezza_prima": lunghezza_prima,
                "capacita_prima": capacita_prima,
                "copiate": array.copie_riferimenti - copie_prima,
                "scritture": 1,
                "lunghezza_dopo": array.dimensione,
                "capacita_dopo": array.capacita,
            }
        )
    return traccia


if __name__ == "__main__":
    righe = traccia_accodamenti(10)
    intestazione = (
        f"{'op':>3} {'len<':>4} {'cap<':>4} {'copie':>5} {'scr':>3} {'len>':>4} {'cap>':>4}"
    )
    print(intestazione)
    for riga in righe:
        print(
            f"{riga['operazione']:>3} {riga['lunghezza_prima']:>4} {riga['capacita_prima']:>4}"
            f" {riga['copiate']:>5} {riga['scritture']:>3}"
            f" {riga['lunghezza_dopo']:>4} {riga['capacita_dopo']:>4}"
        )
    copie = sum(riga["copiate"] for riga in righe)
    scritture = sum(riga["scritture"] for riga in righe)
    print(f"copie totali: {copie}, scritture totali: {scritture}, somma: {copie + scritture}")
