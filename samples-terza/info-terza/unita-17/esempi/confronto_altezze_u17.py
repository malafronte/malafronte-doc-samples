"""Strumentazione di misura dei nodi esaminati — Unità 17, cap. PY-33.

Il modulo aggiunge al BST del capitolo un contatore dei nodi esaminati,
distinto dai confronti primitivi fra chiavi. Un nodo si considera
esaminato quando la sua chiave viene letta per decidere un'operazione:
l'inserimento della prima radice ne esamina 0, mentre una visita a
`None` appartiene alla traccia di controllo e non viene contata.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from bst_u17 import AlberoBST, _Nodo, _valida_chiave


class AlberoBSTContatore(AlberoBST):
    """`AlberoBST` con contatore dei nodi esaminati in ricerca e inserimento.

    Il contatore è uno strumento di misura con un costo proprio: le
    operazioni del capitolo restano quelle di `AlberoBST` e i valori
    osservati descrivono il numero di nodi la cui chiave è stata letta.
    """

    def __init__(self):
        super().__init__()
        self.nodi_esaminati = 0

    def azzera_contatore(self):
        """Azzera il contatore prima di una misura indipendente."""
        self.nodi_esaminati = 0

    def _nodo_per_chiave(self, chiave):
        _valida_chiave(chiave)
        corrente = self._radice
        while corrente is not None:
            self.nodi_esaminati += 1
            if chiave == corrente.chiave:
                return corrente
            if chiave < corrente.chiave:
                corrente = corrente.sinistro
            else:
                corrente = corrente.destro
        return None

    def _inserisci(self, nodo, chiave, dato):
        if nodo is None:
            return _Nodo(chiave, dato), True
        self.nodi_esaminati += 1
        if chiave == nodo.chiave:
            return nodo, False
        if chiave < nodo.chiave:
            nodo.sinistro, inserito = self._inserisci(nodo.sinistro, chiave, dato)
        else:
            nodo.destro, inserito = self._inserisci(nodo.destro, chiave, dato)
        return nodo, inserito

    def ricerca_con_traccia(self, chiave):
        """Restituisce `(trovato, chiavi_esaminate)` per una ricerca.

        La lista `chiavi_esaminate` contiene le chiavi dei soli nodi
        esistenti letti durante il percorso, nell'ordine di visita.
        """
        _valida_chiave(chiave)
        chiavi_esaminate = []
        corrente = self._radice
        while corrente is not None:
            chiavi_esaminate.append(corrente.chiave)
            self.nodi_esaminati += 1
            if chiave == corrente.chiave:
                return True, chiavi_esaminate
            if chiave < corrente.chiave:
                corrente = corrente.sinistro
            else:
                corrente = corrente.destro
        return False, chiavi_esaminate


def misura_costruzione(sequenza):
    """Costruisce un albero dalla `sequenza` e restituisce la misura.

    Il risultato è la tupla `(albero, nodi_esaminati, altezza)`, dove
    `nodi_esaminati` è la somma dei nodi letti durante tutti gli
    inserimenti, compreso il valore 0 per la prima radice.
    """
    albero = AlberoBSTContatore()
    albero.azzera_contatore()
    for chiave in sequenza:
        albero.inserisci(chiave, chiave)
    return albero, albero.nodi_esaminati, albero.altezza()


def misura_ricerca(albero, chiave):
    """Restituisce i nodi esaminati da una ricerca su `albero`.

    L'argomento è un `AlberoBSTContatore`; il contatore viene azzerato
    prima della misura, così il valore si riferisce alla sola ricerca.
    """
    albero.azzera_contatore()
    albero.contiene(chiave)
    return albero.nodi_esaminati
