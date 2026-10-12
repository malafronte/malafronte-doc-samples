"""Starter del laboratorio LAB-PY-U18 — indice hash di materiali.

Il modulo è deliberatamente incompleto. La funzione hash, la validazione, il
nodo, il contenitore con capacità e indici, i dati e il client sono già
disponibili; i metodi marcati con `TODO` costituiscono il lavoro dello
studente. La suite `test_pubblici.py` fallisce all'inizio con
`NotImplementedError`: gli errori attesi sono parte del percorso e scompaiono
con il completamento delle fasi L2–L5.

Contratto della tabella: chiavi di tipo esatto `int` oppure `str`, valori di
qualunque tipo, `KeyError` per la chiave assente, dimensione incrementata
soltanto per una chiave nuova, crescita per raddoppio oltre la soglia 1.0.

Contratto dell'indice: codici testuali non vuoti con zeri significativi,
costruzione che rifiuta i duplicati con `ValueError` senza consegnare una
struttura parziale, query che preservano la raccolta principale.

Ambiente: CPython sul computer, esecuzione con `uv run python
laboratorio/indice_hash_starter.py` dalla cartella `unita-18`.
"""

from __future__ import annotations

from dati_catalogo import voci_canoniche

SOGLIA_CARICO = 1.0


def hash_didattico(chiave):
    """Restituisce l'intero hash didattico: l'intero stesso o l'accumulo testuale."""
    if type(chiave) is int:
        return chiave
    if type(chiave) is str:
        accumulatore = 0
        for carattere in chiave:
            accumulatore = (31 * accumulatore + ord(carattere)) % 65521
        return accumulatore
    raise TypeError(f"chiave attesa di tipo int o str, ricevuto {type(chiave).__name__}")


def _valida_chiave(chiave):
    """Convalida la chiave contro il dominio di tipo esatto `int` o `str`."""
    if type(chiave) not in (int, str):
        raise TypeError(f"chiave attesa di tipo int o str, ricevuto {type(chiave).__name__}")


class _NodoHash:
    """Nodo interno di una catena: chiave, valore e riferimento al successivo."""

    __slots__ = ("chiave", "valore", "successivo")

    def __init__(self, chiave, valore, successivo=None):
        self.chiave = chiave
        self.valore = valore
        self.successivo = successivo


class TabellaHashConcatenata:
    """Dizionario didattico con bucket, catene, carico e redistribuzione."""

    def __init__(self, capacita=5):
        if isinstance(capacita, bool) or not isinstance(capacita, int):
            raise TypeError(f"capacità attesa di tipo int, ricevuto {type(capacita).__name__}")
        if capacita < 1:
            raise ValueError(f"capacità minima 1, ricevuto {capacita}")
        self._bucket = [None] * capacita
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di associazioni presenti."""
        return self._dimensione

    @property
    def capacita(self):
        """Restituisce il numero dei bucket."""
        return len(self._bucket)

    @property
    def fattore_carico(self):
        """Restituisce il rapporto fra associazioni e bucket."""
        return self._dimensione / len(self._bucket)

    def _indice(self, chiave):
        """Restituisce il bucket selezionato dalla `chiave`."""
        _valida_chiave(chiave)
        return hash_didattico(chiave) % len(self._bucket)

    # --- lavoro dello studente: consultazione (fase L2) -----------------
    def cerca(self, chiave):
        """TODO (L2): restituisce il valore associato o solleva `KeyError`."""
        raise NotImplementedError("cerca da completare nella fase L2")

    def contiene(self, chiave):
        """TODO (L2): restituisce `True` se la chiave è presente."""
        raise NotImplementedError("contiene da completare nella fase L2")

    # --- lavoro dello studente: modifiche (fase L3) ---------------------
    def assegna(self, chiave, valore):
        """TODO (L3): inserisce la chiave nuova o aggiorna la presente."""
        raise NotImplementedError("assegna da completare nella fase L3")

    def rimuovi(self, chiave):
        """TODO (L3): elimina l'associazione e restituisce il valore rimosso."""
        raise NotImplementedError("rimuovi da completare nella fase L3")

    # --- lavoro dello studente: crescita (fase L4) ----------------------
    def _ridimensiona(self, nuova_capacita):
        """TODO (L4): ricolloca ogni associazione con la nuova capacità."""
        raise NotImplementedError("_ridimensiona da completare nella fase L4")

    # --- operazioni già complete ----------------------------------------
    def coppie(self):
        """Restituisce una lista nuova di tuple `(chiave, valore)`."""
        risultato = []
        for testa in self._bucket:
            corrente = testa
            while corrente is not None:
                risultato.append((corrente.chiave, corrente.valore))
                corrente = corrente.successivo
        return risultato

    def controlla_invarianti(self):
        """Verifica capacità, appartenenza, unicità, termine e dimensione."""
        assert len(self._bucket) > 0, "capacità non positiva"
        visti = set()
        totale = 0
        for posizione, testa in enumerate(self._bucket):
            corrente = testa
            while corrente is not None:
                assert id(corrente) not in visti, "nodo raggiunto due volte"
                visti.add(id(corrente))
                _valida_chiave(corrente.chiave)
                assert hash_didattico(corrente.chiave) % len(self._bucket) == posizione
                totale += 1
                corrente = corrente.successivo
        assert totale == self._dimensione, "dimensione e nodi non coincidenti"


def valida_codice(codice):
    """Convalida il codice del dominio applicativo: stringa non vuota."""
    if type(codice) is not str:
        raise TypeError(f"codice atteso di tipo str, ricevuto {type(codice).__name__}")
    if codice == "":
        raise ValueError("codice non vuoto richiesto dal dominio applicativo")


class IndiceMateriali:
    """Indice di consultazione dei materiali costruito sulla tabella hash."""

    def __init__(self, capacita=5):
        self._tabella = TabellaHashConcatenata(capacita)

    def __len__(self):
        """Restituisce il numero di voci indicizzate."""
        return len(self._tabella)

    @property
    def capacita(self):
        """Restituisce la capacità della tabella interna."""
        return self._tabella.capacita

    # --- lavoro dello studente: indice di record (fase L5) --------------
    def costruisci(self, voci):
        """TODO (L5): valida, verifica l'unicità e costruisce l'indice completo."""
        raise NotImplementedError("costruisci da completare nella fase L5")

    def consulta(self, codice):
        """TODO (L5): restituisce la voce associata al codice."""
        raise NotImplementedError("consulta da completare nella fase L5")

    def fotografia(self):
        """TODO (L5): restituisce le coppie ordinate per codice."""
        raise NotImplementedError("fotografia da completare nella fase L5")


def client_dimostrazione():
    """Costruisce l'indice canonico e ne restituisce dimensione e fotografia.

    La funzione è già completa e non richiede modifiche: usa soltanto l'API
    pubblica dell'indice.
    """
    indice = IndiceMateriali()
    indice.costruisci(voci_canoniche())
    return len(indice), indice.fotografia()


if __name__ == "__main__":
    dimensione, foto = client_dimostrazione()
    print(f"voci indicizzate: {dimensione}")
    for codice, voce in foto:
        print(f"  {codice}: {voce.descrizione}, quantita = {voce.quantita}")
