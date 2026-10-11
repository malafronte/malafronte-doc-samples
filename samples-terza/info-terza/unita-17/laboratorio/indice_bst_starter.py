"""Starter del laboratorio LAB-PY-U17 — indice BST di schede tecniche.

Il modulo è deliberatamente incompleto. Le classi, i contratti, i dati e
il client sono già disponibili; i metodi marcati con `TODO` costituiscono
il lavoro dello studente. La suite `test_pubblici.py` fallisce all'inizio
con `NotImplementedError`: gli errori attesi sono parte del percorso.

Ambiente: CPython sul computer, esecuzione con `uv run python
laboratorio/indice_bst_starter.py` dalla cartella `unita-17`.
"""

from __future__ import annotations

from dataclasses import dataclass

from dati_schede import Scheda


@dataclass
class _Nodo:
    """Nodo interno dell'indice: chiave, record associato e due figli."""

    chiave: int
    record: Scheda
    sinistro: _Nodo | None = None
    destro: _Nodo | None = None


class IndiceSchede:
    """Indice di ricerca per codice costruito come albero binario di ricerca.

    Il contenitore conserva `_radice` e `_dimensione`. L'API pubblica
    restituisce record e raccolte di risultati; i nodi `_Nodo` sono
    dettagli interni. Le chiavi sono intere e uniche; il dato associato
    è il record `Scheda` il cui campo `codice` coincide con la chiave.
    """

    def __init__(self):
        self._radice = None
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di record indicizzati."""
        return self._dimensione

    # --- operazioni già complete ------------------------------------
    def vuoto(self):
        """Restituisce `True` quando l'indice non contiene record."""
        return self._radice is None

    def codici_ordinati(self):
        """Restituisce i codici in ordine crescente come nuova lista."""
        risultato = []
        self._inordine_codici(self._radice, risultato)
        return risultato

    def _inordine_codici(self, nodo, risultato):
        if nodo is None:
            return
        self._inordine_codici(nodo.sinistro, risultato)
        risultato.append(nodo.chiave)
        self._inordine_codici(nodo.destro, risultato)

    def voci_ordinate(self):
        """Restituisce le coppie `(codice, record)` in ordine crescente."""
        risultato = []
        self._inordine_voci(self._radice, risultato)
        return risultato

    def _inordine_voci(self, nodo, risultato):
        if nodo is None:
            return
        self._inordine_voci(nodo.sinistro, risultato)
        risultato.append((nodo.chiave, nodo.record))
        self._inordine_voci(nodo.destro, risultato)

    # --- lavoro dello studente --------------------------------------
    def costruisci(self, schede):
        """Costruisce l'indice a partire dalla raccolta di `Scheda`.

        TODO: 1. azzerare lo stato precedente; 2. inserire ogni record
        con la chiave `record.codice`; 3. rilevare un codice ripetuto e
        sollevare `ValueError` senza consegnare una struttura parziale.
        """
        raise NotImplementedError("costruisci")

    def contiene(self, codice):
        """Restituisce `True` se il `codice` è indicizzato.

        TODO: percorrere i confronti fra chiavi fino al nodo richiesto
        oppure a un collegamento vuoto; convalidare il tipo del codice.
        """
        raise NotImplementedError("contiene")

    def record(self, codice):
        """Restituisce il record associato al `codice`.

        TODO: restituire il record; sollevare `KeyError` quando il codice
        è assente. Il record restituito conserva ogni proprio campo.
        """
        raise NotImplementedError("record")

    def intervallo(self, minimo, massimo):
        """Restituisce i record con codice nell'intervallo chiuso.

        TODO: usare la proprietà d'ordine per escludere i sottoalberi
        irrilevanti, produrre direttamente i record in ordine crescente,
        sollevare `ValueError` per estremi invertiti.
        """
        raise NotImplementedError("intervallo")

    def rimuovi(self, codice):
        """Elimina il record del `codice` e restituisce `True`.

        TODO: trattare i tre casi — foglia, un solo figlio, due figli con
        successore inordine — restituendo la nuova radice del sottoalbero
        e aggiornando la dimensione una sola volta.
        """
        raise NotImplementedError("rimuovi")

    def controlla_invarianti(self):
        """Verifica ordine, struttura e dimensione; solleva `AssertionError`.

        TODO: usare limiti inferiore e superiore ereditati, contare i nodi
        raggiungibili e confrontarli con `_dimensione`.
        """
        raise NotImplementedError("controlla_invarianti")


def client_dimostrazione(indice):
    """Esegue una consultazione completa sull'indice e restituisce gli esiti.

    Il client è già completo e non richiede modifiche: mostra costruzione,
    ricerca, vista ordinata, intervallo e rimozione sui dati canonici.
    """
    from dati_schede import schede_canoniche

    indice.costruisci(schede_canoniche())
    return {
        "dimensione": len(indice),
        "codici": indice.codici_ordinati(),
        "record_30": indice.record(30),
        "intervallo_25_55": [codice for codice, _ in indice.intervallo(25, 55)],
    }


if __name__ == "__main__":
    print(client_dimostrazione(IndiceSchede()))
