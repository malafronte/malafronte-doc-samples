"""Starter del laboratorio LAB-PY-U16 - lista concatenata e coda (lavoro incompleto).

Il file contiene già il contratto pubblico, il dataset sintetico, la funzione
di controllo degli invarianti e i casi pubblici di accettazione. Le parti
marcate con `TODO` sono il lavoro da completare durante la sessione: gli
aggiornamenti dei collegamenti e il wrapper della coda.

Ambiente: CPython sul computer, cartella `unita-16` del repository degli esempi.
Esecuzione delle prove: `uv run pytest -q laboratorio/test_lista_coda_starter.py`.
"""

from __future__ import annotations

# Dataset sintetico del laboratorio: i duplicati sono voluti.
DATASET_LAB = [12, 7, 7, 19]


class Nodo:
    """Nodo della catena: conserva un valore e il riferimento al successivo."""

    def __init__(self, valore, successivo: Nodo | None = None) -> None:
        self.valore = valore
        self.successivo = successivo


class ListaConcatenataStarter:
    """Contenitore con testa, coda e dimensione mantenute coerenti.

    Contratto pubblico: `len`, `aggiungi_in_testa`, `aggiungi_in_coda`, `primo`,
    `rimuovi_primo`, `contiene`, `rimuovi`, `a_lista`. Su vuoto `primo` e
    `rimuovi_primo` sollevano `IndexError` e conservano lo stato.
    """

    def __init__(self) -> None:
        self._testa: Nodo | None = None
        self._coda: Nodo | None = None
        self._dimensione = 0

    def __len__(self) -> int:
        return self._dimensione

    def aggiungi_in_testa(self, valore) -> None:
        """Colloca `valore` in prima posizione; la dimensione aumenta di uno."""
        # TODO: collegare il nuovo nodo alla testa precedente, aggiornare la
        # testa, la coda nel caso iniziale vuoto e la dimensione.
        raise NotImplementedError("aggiunta in testa da completare")

    def aggiungi_in_coda(self, valore) -> None:
        """Colloca `valore` in ultima posizione; la dimensione aumenta di uno."""
        # TODO: usare il riferimento `_coda` per collegare il nuovo nodo senza
        # attraversare la catena; inizializzare entrambi gli estremi sul vuoto.
        raise NotImplementedError("aggiunta in coda da completare")

    def primo(self):
        """Restituisce il primo valore conservando la struttura; su vuoto solleva IndexError."""
        # TODO: restituire il valore della testa oppure sollevare IndexError.
        raise NotImplementedError("primo da completare")

    def rimuovi_primo(self):
        """Restituisce il primo valore e rimuove il nodo; su vuoto solleva IndexError."""
        # TODO: restituire il valore, far avanzare la testa, ripristinare la
        # coda quando la catena diventa vuota, decrementare la dimensione.
        raise NotImplementedError("rimozione del primo da completare")

    def contiene(self, valore) -> bool:
        """Restituisce True alla prima uguaglianza incontrata lungo la catena."""
        corrente = self._testa
        while corrente is not None:
            if corrente.valore == valore:
                return True
            corrente = corrente.successivo
        return False

    def rimuovi(self, valore) -> bool:
        """Rimuove la prima occorrenza di `valore` e restituisce True; su assenza False."""
        # TODO: tenere `precedente` e `corrente`, conservare il successore prima
        # degli aggiornamenti, mantenere coda e dimensione anche in coda e
        # quando la catena diventa vuota.
        raise NotImplementedError("cancellazione per valore da completare")

    def a_lista(self) -> list:
        """Restituisce un nuovo contenitore Python con i valori nell'ordine della catena."""
        raccolti = []
        corrente = self._testa
        while corrente is not None:
            raccolti.append(corrente.valore)
            corrente = corrente.successivo
        return raccolti


def controlla_invarianti(lista: ListaConcatenataStarter) -> list[str]:
    """Restituisce le violazioni degli invarianti; lista vuota = stato coerente.

    Funzione fornita dal laboratorio: si esegue dopo ogni operazione nelle
    prove. Il suo costo appartiene al controllo, non alle operazioni della
    struttura.
    """
    problemi: list[str] = []
    if lista._dimensione < 0:
        problemi.append("dimensione negativa")
    visti: set[int] = set()
    corrente = lista._testa
    conteggio = 0
    ultimo: Nodo | None = None
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


class CodaConcatenataStarter:
    """Coda FIFO sulla lista concatenata: il wrapper delega al contenitore.

    Contratto: `accoda`, `estrai`, `fronte`, `vuota`, `len`. Sul vuoto `estrai`
    e `fronte` sollevano `IndexError` e conservano lo stato.
    """

    def __init__(self) -> None:
        self._elementi = ListaConcatenataStarter()

    def __len__(self) -> int:
        return len(self._elementi)

    def vuota(self) -> bool:
        """Restituisce True quando la coda non contiene elementi."""
        return len(self._elementi) == 0

    def accoda(self, valore) -> None:
        """Colloca `valore` in coda, dopo tutti gli elementi pendenti."""
        # TODO: delegare all'operazione pertinente del contenitore.
        raise NotImplementedError("accodamento da completare")

    def estrai(self):
        """Rimuove e restituisce il valore al fronte; su vuoto solleva IndexError."""
        # TODO: delegare all'operazione pertinente del contenitore.
        raise NotImplementedError("estrazione da completare")

    def fronte(self):
        """Restituisce il valore al fronte conservando la coda; su vuoto solleva IndexError."""
        # TODO: delegare all'operazione pertinente del contenitore.
        raise NotImplementedError("fronte da completare")


def client_elaborazione(coda, valori: list) -> list:
    """Accoda `valori` in ordine ed estrae finché la coda è vuota; restituisce gli estratti.

    Il client è già completo e accetta qualunque collaboratore compatibile con
    il contratto della coda: lo stesso corpo di prova si applica a
    `CodaConcatenataStarter` e a `collections.deque` con wrapper adattato.
    """
    for valore in valori:
        coda.accoda(valore)
    estratti = []
    while not coda.vuota():
        estratti.append(coda.estrai())
    return estratti
