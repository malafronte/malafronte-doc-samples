"""Albero binario di ricerca (BST) con chiavi intere e dati associati — Unità 17.

Il modulo realizza la classe `AlberoBST` con i contratti del cap. PY-33:
chiavi intere uniche (il tipo `bool` è escluso dal dominio), dato
associato di qualunque tipo, rifiuto dei duplicati, rimozione nei tre
casi, query su intervallo chiuso e verifica degli invarianti.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

_ALTEZZA_VUOTO = -1


class _Nodo:
    """Nodo interno dell'albero: chiave, dato associato e due figli."""

    __slots__ = ("chiave", "dato", "sinistro", "destro")

    def __init__(self, chiave, dato, sinistro=None, destro=None):
        self.chiave = chiave
        self.dato = dato
        self.sinistro = sinistro
        self.destro = destro


def _valida_chiave(chiave):
    """Convalida la chiave contro il dominio dichiarato.

    Il dominio è `int` con `bool` escluso: `True` e `False` sono istanze
    di `bool`, che Python considera sottoinsieme di `int`, e qui restano
    fuori dominio per evitare confronti ambigui con 0 e 1.
    """
    if isinstance(chiave, bool) or not isinstance(chiave, int):
        raise TypeError(f"chiave attesa di tipo int, ricevuto {type(chiave).__name__}")


class AlberoBST:
    """Albero binario di ricerca con chiavi intere uniche.

    Il contenitore conserva `_radice` e `_dimensione`; i nodi `_Nodo`
    sono dettagli interni e non compaiono nei risultati pubblici.
    """

    def __init__(self):
        self._radice = None
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di chiavi presenti."""
        return self._dimensione

    # ------------------------------------------------------------------
    # Ricerca
    # ------------------------------------------------------------------

    def contiene(self, chiave):
        """Restituisce `True` se `chiave` è presente, `False` altrimenti.

        L'albero vuoto restituisce `False`; una chiave fuori dominio
        solleva `TypeError` anche sull'albero vuoto.
        """
        _valida_chiave(chiave)
        return self._nodo_per_chiave(chiave) is not None

    def cerca(self, chiave):
        """Restituisce il dato associato a `chiave`.

        La chiave assente solleva `KeyError`. La presenza è determinata
        dalla struttura e dal confronto della chiave: il dato associato
        può valere `None`, `0`, `False` o `""` e resta un dato valido.
        """
        nodo = self._nodo_per_chiave(chiave)
        if nodo is None:
            raise KeyError(chiave)
        return nodo.dato

    def _nodo_per_chiave(self, chiave):
        """Restituisce il nodo con la chiave richiesta, oppure `None`."""
        _valida_chiave(chiave)
        corrente = self._radice
        while corrente is not None:
            if chiave == corrente.chiave:
                return corrente
            if chiave < corrente.chiave:
                corrente = corrente.sinistro
            else:
                corrente = corrente.destro
        return None

    # ------------------------------------------------------------------
    # Inserimento e aggiornamento
    # ------------------------------------------------------------------

    def inserisci(self, chiave, dato):
        """Crea l'associazione `chiave` → `dato`.

        Una chiave duplicata solleva `ValueError` e conserva sia la
        forma dell'albero sia il dato precedentemente associato.
        """
        _valida_chiave(chiave)
        nuova_radice, inserito = self._inserisci(self._radice, chiave, dato)
        if not inserito:
            raise ValueError(f"chiave già presente: {chiave}")
        self._radice = nuova_radice
        self._dimensione += 1

    def _inserisci(self, nodo, chiave, dato):
        """Inserisce nel sottoalbero e restituisce la nuova radice e l'esito.

        Contratto della funzione ausiliaria: riceve la radice attuale del
        sottoalbero e restituisce la radice dopo la modifica, insieme al
        valore booleano che distingue l'inserimento dal rifiuto.
        """
        if nodo is None:
            return _Nodo(chiave, dato), True
        if chiave == nodo.chiave:
            return nodo, False
        if chiave < nodo.chiave:
            nodo.sinistro, inserito = self._inserisci(nodo.sinistro, chiave, dato)
        else:
            nodo.destro, inserito = self._inserisci(nodo.destro, chiave, dato)
        return nodo, inserito

    def aggiorna(self, chiave, dato):
        """Sostituisce il dato associato alla `chiave` esistente.

        La chiave assente solleva `KeyError`. Forma e dimensione restano
        invariate: l'aggiornamento modifica soltanto il dato.
        """
        nodo = self._nodo_per_chiave(chiave)
        if nodo is None:
            raise KeyError(chiave)
        nodo.dato = dato

    # ------------------------------------------------------------------
    # Estremi
    # ------------------------------------------------------------------

    def minimo(self):
        """Restituisce la chiave minima; l'albero vuoto solleva `IndexError`."""
        if self._radice is None:
            raise IndexError("albero vuoto: minimo non definito")
        corrente = self._radice
        while corrente.sinistro is not None:
            corrente = corrente.sinistro
        return corrente.chiave

    def massimo(self):
        """Restituisce la chiave massima; l'albero vuoto solleva `IndexError`."""
        if self._radice is None:
            raise IndexError("albero vuoto: massimo non definito")
        corrente = self._radice
        while corrente.destro is not None:
            corrente = corrente.destro
        return corrente.chiave

    # ------------------------------------------------------------------
    # Visite
    # ------------------------------------------------------------------

    def preordine(self):
        """Restituisce una nuova lista delle chiavi in ordine preordine."""
        risultato = []
        self._preordine(self._radice, risultato)
        return risultato

    def _preordine(self, nodo, risultato):
        if nodo is None:
            return
        risultato.append(nodo.chiave)
        self._preordine(nodo.sinistro, risultato)
        self._preordine(nodo.destro, risultato)

    def inordine(self):
        """Restituisce una nuova lista delle chiavi in ordine inordine."""
        risultato = []
        self._inordine(self._radice, risultato)
        return risultato

    def _inordine(self, nodo, risultato):
        if nodo is None:
            return
        self._inordine(nodo.sinistro, risultato)
        risultato.append(nodo.chiave)
        self._inordine(nodo.destro, risultato)

    def postordine(self):
        """Restituisce una nuova lista delle chiavi in ordine postordine."""
        risultato = []
        self._postordine(self._radice, risultato)
        return risultato

    def _postordine(self, nodo, risultato):
        if nodo is None:
            return
        self._postordine(nodo.sinistro, risultato)
        self._postordine(nodo.destro, risultato)
        risultato.append(nodo.chiave)

    def voci_ordinate(self):
        """Restituisce una nuova lista di coppie `(chiave, dato)` in ordine crescente.

        La raccolta diretta delle coppie in una sola visita evita una
        ricerca per ciascuna chiave già incontrata.
        """
        risultato = []
        self._voci(self._radice, risultato)
        return risultato

    def _voci(self, nodo, risultato):
        if nodo is None:
            return
        self._voci(nodo.sinistro, risultato)
        risultato.append((nodo.chiave, nodo.dato))
        self._voci(nodo.destro, risultato)

    # ------------------------------------------------------------------
    # Altezza e query
    # ------------------------------------------------------------------

    def altezza(self):
        """Restituisce l'altezza in archi; il sottoalbero vuoto vale -1."""
        return self._altezza(self._radice)

    def _altezza(self, nodo):
        if nodo is None:
            return _ALTEZZA_VUOTO
        return 1 + max(self._altezza(nodo.sinistro), self._altezza(nodo.destro))

    def intervallo(self, minimo, massimo):
        """Restituisce le coppie con chiave nell'intervallo chiuso `[minimo, massimo]`.

        Il risultato è ordinato in modo crescente e include entrambi gli
        estremi. L'albero vuoto e l'assenza di corrispondenze producono
        la lista vuota; `minimo > massimo` solleva `ValueError`.
        """
        _valida_chiave(minimo)
        _valida_chiave(massimo)
        if minimo > massimo:
            raise ValueError("l'estremo minimo non può superare l'estremo massimo")
        risultato = []
        self._intervallo(self._radice, minimo, massimo, risultato)
        return risultato

    def _intervallo(self, nodo, minimo, massimo, risultato):
        if nodo is None:
            return
        # Il sottoalbero sinistro contiene solo chiavi minori della corrente:
        # viene visitato soltanto se può contenere chiavi >= minimo.
        if minimo < nodo.chiave:
            self._intervallo(nodo.sinistro, minimo, massimo, risultato)
        if minimo <= nodo.chiave <= massimo:
            risultato.append((nodo.chiave, nodo.dato))
        # Il sottoalbero destro contiene solo chiavi maggiori della corrente:
        # viene visitato soltanto se può contenere chiavi <= massimo.
        if nodo.chiave < massimo:
            self._intervallo(nodo.destro, minimo, massimo, risultato)

    # ------------------------------------------------------------------
    # Cancellazione
    # ------------------------------------------------------------------

    def rimuovi(self, chiave):
        """Elimina l'associazione di `chiave` e restituisce `True`.

        La chiave assente restituisce `False` e conserva ogni dato.
        """
        _valida_chiave(chiave)
        nuova_radice, rimosso = self._rimuovi(self._radice, chiave)
        if rimosso:
            self._radice = nuova_radice
            self._dimensione -= 1
        return rimosso

    def _rimuovi(self, nodo, chiave):
        """Rimuove dal sottoalbero e restituisce la nuova radice e l'esito.

        La funzione gestisce i collegamenti e comunica l'esito; il
        contatore del contenitore viene aggiornato una sola volta dal
        metodo pubblico `rimuovi`.
        """
        if nodo is None:
            return None, False
        if chiave < nodo.chiave:
            nodo.sinistro, rimosso = self._rimuovi(nodo.sinistro, chiave)
            return nodo, rimosso
        if chiave > nodo.chiave:
            nodo.destro, rimosso = self._rimuovi(nodo.destro, chiave)
            return nodo, rimosso

        # La chiave coincide: il nodo corrente va eliminato.
        if nodo.sinistro is None:
            # Nessun figlio oppure solo il figlio destro.
            return nodo.destro, True
        if nodo.destro is None:
            # Solo il figlio sinistro.
            return nodo.sinistro, True

        # Due figli: il successore inordine è il minimo del sottoalbero
        # destro. Chiave e dato del successore sostituiscono quelli del
        # nodo corrente; il nodo del successore viene poi eliminato con
        # una rimozione che ricade nei casi già trattati.
        successore = nodo.destro
        while successore.sinistro is not None:
            successore = successore.sinistro
        nodo.chiave = successore.chiave
        nodo.dato = successore.dato
        nodo.destro, _ = self._rimuovi(nodo.destro, successore.chiave)
        return nodo, True

    # ------------------------------------------------------------------
    # Strumento diagnostico
    # ------------------------------------------------------------------

    def controlla_invarianti(self):
        """Verifica struttura, ordine e dimensione; solleva `AssertionError`.

        Lo strumento ha un costo proprio e non viene richiamato dalle
        operazioni: la sua scansione completa dentro ogni metodo
        modificherebbe i costi osservati.
        """
        visti = set()
        totale = self._visita_struttura(self._radice, None, None, visti)
        assert totale == self._dimensione, (
            f"dimensione dichiarata {self._dimensione}, nodi raggiungibili {totale}"
        )
        if self._radice is None:
            assert self._dimensione == 0, "radice vuota con dimensione diversa da 0"

    def _visita_struttura(self, nodo, limite_inferiore, limite_superiore, visti):
        if nodo is None:
            return 0
        identita = id(nodo)
        assert identita not in visti, f"nodo raggiunto due volte con chiave {nodo.chiave}"
        visti.add(identita)
        _valida_chiave(nodo.chiave)
        if limite_inferiore is not None:
            assert nodo.chiave > limite_inferiore, (
                f"chiave {nodo.chiave} non superiore al limite {limite_inferiore}"
            )
        if limite_superiore is not None:
            assert nodo.chiave < limite_superiore, (
                f"chiave {nodo.chiave} non inferiore al limite {limite_superiore}"
            )
        sinistro = self._visita_struttura(nodo.sinistro, limite_inferiore, nodo.chiave, visti)
        destro = self._visita_struttura(nodo.destro, nodo.chiave, limite_superiore, visti)
        return 1 + sinistro + destro


def costruisci_da_inserimenti(sequenza, dati=None):
    """Costruisce un `AlberoBST` inserendo le `sequenza` di chiavi.

    Quando `dati` è `None` il dato associato coincide con la chiave. La
    funzione serve agli esempi sulle forme indotte dall'ordine di
    inserimento.
    """
    albero = AlberoBST()
    for posizione, chiave in enumerate(sequenza):
        dato = chiave if dati is None else dati[posizione]
        albero.inserisci(chiave, dato)
    return albero
