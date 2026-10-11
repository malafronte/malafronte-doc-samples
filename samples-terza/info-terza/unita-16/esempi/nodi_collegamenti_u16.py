"""Valori, nodi e collegamenti - primo esempio autonomo dell'Unità 16 (PY-23).

Il modulo costruisce a mano una piccola catena di nodi e la attraversa, senza
ancora introdurre il contenitore `ListaConcatenata`. Il nodo qui si chiama
`Nodo` ed è un oggetto didattico completo: nella lista concatenata lo stesso
ruolo sarà svolto dal nodo interno `_Nodo`, con i due attributi già spiegati.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations


class Nodo:
    """Nodo di una catena: conserva un valore e il riferimento al nodo successivo."""

    def __init__(self, valore, successivo: Nodo | None = None) -> None:
        self.valore = valore
        self.successivo = successivo

    def __repr__(self) -> str:
        return f"Nodo({self.valore!r})"


def catena_tre_valori() -> Nodo:
    """Costruisce la catena 12 -> 7 -> 19 e restituisce il riferimento alla testa.

    I tre nodi sono creati dal successivo al primo, così ogni costruttore
    riceve già il riferimento al nodo che seguirà nella catena.
    """
    nodo_c = Nodo(19)  # successivo omesso: il valore predefinito è None
    nodo_b = Nodo(7, nodo_c)
    nodo_a = Nodo(12, nodo_b)
    return nodo_a


def valori_della_catena(testa: Nodo | None) -> list:
    """Attraversa la catena e restituisce i valori nell'ordine di visita."""
    raccolti = []
    corrente = testa
    while corrente is not None:
        raccolti.append(corrente.valore)
        corrente = corrente.successivo
    return raccolti


def cerca_valore(testa: Nodo | None, valore) -> Nodo | None:
    """Restituisce il primo nodo il cui valore è uguale a `valore`, oppure None.

    Il controllo della presenza del nodo usa `is None`; il confronto fra valori
    usa `==`. I due controlli hanno ruoli distinti.
    """
    corrente = testa
    while corrente is not None:
        if corrente.valore == valore:
            return corrente
        corrente = corrente.successivo
    return None


def nodo_in_posizione(testa: Nodo | None, indice: int) -> Nodo | None:
    """Restituisce il nodo in posizione `indice` contato dalla testa, oppure None.

    L'avanzamento conta i passi già compiuti: la posizione chiesta viene
    raggiunta dopo `indice` spostamenti dal primo nodo.
    """
    corrente = testa
    passi = 0
    while corrente is not None:
        if passi == indice:
            return corrente
        corrente = corrente.successivo
        passi += 1
    return None


if __name__ == "__main__":
    testa = catena_tre_valori()
    print("valori della catena:", valori_della_catena(testa))
    trovato = cerca_valore(testa, 7)
    print("nodo con valore 7:", trovato, "-> successivo:", trovato.successivo)
    print("terzo nodo:", nodo_in_posizione(testa, 2))
    print("ricerca di 99:", cerca_valore(testa, 99))
    print("catena vuota:", valori_della_catena(None))
