"""Lista semplicemente concatenata - riferimento didattico dell'Unità 16 (PY-30).

Il modulo contiene il nodo interno `_Nodo`, il contenitore `ListaConcatenata`
e la funzione autoriale `controlla_invarianti`, usata dalle prove per
verificare lo stato della struttura dopo ogni mutazione.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations


class _Nodo:
    """Nodo interno della catena: conserva un valore e il riferimento al successivo.

    Il trattino iniziale segue la convenzione già usata nel corso per gli
    elementi che appartengono all'implementazione e restano fuori dal
    contratto pubblico del contenitore.
    """

    def __init__(self, valore, successivo: _Nodo | None = None) -> None:
        self.valore = valore
        self.successivo = successivo


class ListaConcatenata:
    """Sequenza di valori conservati in nodi collegati da riferimenti.

    Contratto pubblico: `len`, `aggiungi_in_testa`, `aggiungi_in_coda`,
    `primo`, `rimuovi_primo`, `contiene`, `valore_in_posizione`, `rimuovi`,
    `a_lista`, `inverti`. L'uguaglianza dei valori usa `==`; l'identità dei
    nodi usa `is`.
    """

    def __init__(self) -> None:
        self._testa: _Nodo | None = None
        self._coda: _Nodo | None = None
        self._dimensione = 0

    def __len__(self) -> int:
        return self._dimensione

    def __repr__(self) -> str:
        return f"ListaConcatenata({self.a_lista()!r})"

    def aggiungi_in_testa(self, valore) -> None:
        """Colloca `valore` in prima posizione; la dimensione aumenta di uno."""
        nuovo = _Nodo(valore, self._testa)
        self._testa = nuovo
        if self._coda is None:  # la struttura era vuota
            self._coda = nuovo
        self._dimensione += 1

    def aggiungi_in_coda(self, valore) -> None:
        """Colloca `valore` in ultima posizione; la dimensione aumenta di uno."""
        nuovo = _Nodo(valore)
        if self._coda is None:  # la struttura era vuota
            self._testa = nuovo
            self._coda = nuovo
        else:
            self._coda.successivo = nuovo
            self._coda = nuovo
        self._dimensione += 1

    def primo(self):
        """Restituisce il primo valore conservando la struttura; su vuoto solleva IndexError."""
        if self._testa is None:
            raise IndexError("primo su lista vuota")
        return self._testa.valore

    def rimuovi_primo(self):
        """Restituisce il primo valore e rimuove il nodo; su vuoto solleva IndexError."""
        if self._testa is None:
            raise IndexError("rimozione del primo su lista vuota")
        valore = self._testa.valore
        self._testa = self._testa.successivo
        if self._testa is None:  # la catena è ora vuota
            self._coda = None
        self._dimensione -= 1
        return valore

    def contiene(self, valore) -> bool:
        """Restituisce True alla prima uguaglianza incontrata lungo la catena."""
        corrente = self._testa
        while corrente is not None:
            if corrente.valore == valore:
                return True
            corrente = corrente.successivo
        return False

    def valore_in_posizione(self, indice: int):
        """Restituisce il valore in posizione `indice`, contato dalla testa.

        Dominio: intero esatto (anche `bool`) con `0 <= indice < len(lista)`;
        tipo errato -> TypeError, indice fuori dominio -> IndexError.
        """
        if type(indice) is not int:
            raise TypeError("l'indice deve essere un intero")
        if not 0 <= indice < self._dimensione:
            raise IndexError(f"indice fuori dominio: {indice}")
        corrente = self._testa
        for _ in range(indice):
            corrente = corrente.successivo
        # Il ciclo precedente termina su un nodo esistente per il controllo del dominio.
        assert corrente is not None
        return corrente.valore

    def rimuovi(self, valore) -> bool:
        """Rimuove la prima occorrenza di `valore` e restituisce True.

        Su assenza restituisce False e conserva lo stato della struttura.
        """
        precedente: _Nodo | None = None
        corrente = self._testa
        while corrente is not None:
            if corrente.valore == valore:
                self._rimuovi_dopo(precedente, corrente)
                return True
            precedente = corrente
            corrente = corrente.successivo
        return False

    def _rimuovi_dopo(self, precedente: _Nodo | None, corrente: _Nodo) -> None:
        """Aggiorna i collegamenti per scollegare `corrente`, già individuato.

        Precondizione interna: `corrente` appartiene alla catena e `precedente`
        è il suo predecessore oppure None quando `corrente` è la testa.
        """
        if precedente is None:
            self._testa = corrente.successivo
        else:
            precedente.successivo = corrente.successivo
        if corrente is self._coda:
            self._coda = precedente
        self._dimensione -= 1

    def a_lista(self) -> list:
        """Restituisce un nuovo contenitore Python con i valori nell'ordine della catena."""
        risultato = []
        corrente = self._testa
        while corrente is not None:
            risultato.append(corrente.valore)
            corrente = corrente.successivo
        return risultato

    def inverti(self) -> None:
        """Inverte i collegamenti riusando gli stessi nodi; ordine dei valori capovolto."""
        precedente: _Nodo | None = None
        corrente = self._testa
        self._coda = self._testa
        while corrente is not None:
            successivo = corrente.successivo  # si conserva il suffisso da elaborare
            corrente.successivo = precedente
            precedente = corrente
            corrente = successivo
        self._testa = precedente


def controlla_invarianti(lista: ListaConcatenata) -> list[str]:
    """Restituisce le violazioni degli invarianti della struttura; lista vuota = stato coerente.

    La funzione è strumentazione di verifica: attraversa la catena e può
    costare O(n). I costi delle operazioni della struttura si analizzano a
    parte da questo controllo.
    """
    problemi: list[str] = []
    if lista._dimensione < 0:
        problemi.append("dimensione negativa")
    visti: set[int] = set()
    corrente = lista._testa
    conteggio = 0
    ultimo: _Nodo | None = None
    while corrente is not None:
        if id(corrente) in visti:
            problemi.append("nodo ripetuto o ciclo nella catena")
            break
        visti.add(id(corrente))
        conteggio += 1
        ultimo = corrente
        corrente = corrente.successivo
    if conteggio != lista._dimensione:
        problemi.append(f"nodi raggiungibili {conteggio} != dimensione {lista._dimensione}")
    if lista._dimensione == 0:
        if lista._testa is not None or lista._coda is not None:
            problemi.append("vuoto con estremi non None")
    else:
        if lista._testa is None or lista._coda is None:
            problemi.append("struttura popolata con estremo None")
        if ultimo is not lista._coda:
            problemi.append("l'ultimo nodo raggiunto non è la coda")
        elif lista._coda.successivo is not None:
            problemi.append("la coda ha un successivo")
    return problemi
