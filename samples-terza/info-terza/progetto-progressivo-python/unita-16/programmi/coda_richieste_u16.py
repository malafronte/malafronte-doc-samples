"""Coda di richieste di consultazione (U16).

Responsabilità del modulo: conservare le **richieste di consultazione**
nell'ordine di arrivo e restituire per ciascuna l'esito del criterio che
descrive. La coda è una struttura FIFO con due rappresentazioni intercambiabili
- `CodaDequeU16` su `collections.deque` e `CodaConcatenataU16` sulla catena di
nodi didattica - usate dal medesimo servizio senza modifiche.

Contratto della coda (`accoda`, `estrai`, `fronte`, `vuota`, `len`):

- **dati ammessi**: richieste `RichiestaConsultazione` valide;
- **risultato**: `accoda` restituisce `None`; `estrai` e `fronte` restituiscono
  la richiesta in attesa da più tempo;
- **effetti**: `estrai` riduce la dimensione di uno; `fronte` conserva lo stato;
- **errori**: su coda vuota `estrai` e `fronte` sollevano `IndexError`;
- **invarianti**: gli elementi escono nell'ordine di arrivo; la dimensione
  coincide con il numero di richieste pendenti.

Contratto della richiesta (`RichiestaConsultazione`):

- `codice` è una stringa non vuota che identifica la richiesta;
- `criterio` espone `ammette(preventivo) -> bool` e `descrizione() -> str`,
  lo stesso contratto dei criteri U15.

Politica di errore del servizio: una richiesta invalida viene rifiutata **prima**
dell'accodamento e non modifica la coda; durante l'elaborazione la richiesta
resta **al fronte** finché il calcolo non riesce - sequenza fronte, calcolo,
estrazione. Le richieste pendenti sono stato in memoria: la persistenza della
coda è un'estensione con schema separato.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""
from dataclasses import dataclass, field

from registro_consultazione_u15 import seleziona_codici


@dataclass(frozen=True)
class RichiestaConsultazione:
    """Richiesta di consultazione: codice identificativo e criterio da applicare."""

    codice: str
    criterio: object


@dataclass(frozen=True)
class EsitoConsultazione:
    """Esito dell'elaborazione di una richiesta sull'orologio logico del servizio."""

    codice: str
    criterio: str
    codici_ammessi: tuple = field(default_factory=tuple)


class CodaDequeU16:
    """Coda FIFO su `collections.deque`: fronte a sinistra, accodamento a destra."""

    def __init__(self):
        from collections import deque

        self._elementi = deque()

    def __len__(self):
        return len(self._elementi)

    def vuota(self):
        """Restituisce True quando la coda non contiene richieste."""
        return not self._elementi

    def accoda(self, richiesta):
        """Colloca la richiesta dopo tutte quelle pendenti."""
        self._elementi.append(richiesta)

    def estrai(self):
        """Rimuove e restituisce la richiesta al fronte; su vuota solleva IndexError."""
        if not self._elementi:
            raise IndexError("estrazione da coda vuota")
        return self._elementi.popleft()

    def fronte(self):
        """Restituisce la richiesta al fronte conservando la coda; su vuota IndexError."""
        if not self._elementi:
            raise IndexError("fronte di coda vuota")
        return self._elementi[0]


class _NodoCoda:
    """Nodo della catena didattica: richiesta e riferimento al successivo."""

    def __init__(self, richiesta, successivo=None):
        self.richiesta = richiesta
        self.successivo = successivo


class CodaConcatenataU16:
    """Coda FIFO sulla catena di nodi: accodamento in coda, rimozione in testa.

    Il contenitore mantiene `testa`, `coda` e `dimensione`: il fronte è la
    testa della catena e ogni accodamento è locale grazie al riferimento alla
    coda, come nel capitolo PY-23 dell'Unità 16.
    """

    def __init__(self):
        self._testa = None
        self._coda = None
        self._dimensione = 0

    def __len__(self):
        return self._dimensione

    def vuota(self):
        """Restituisce True quando la coda non contiene richieste."""
        return self._dimensione == 0

    def accoda(self, richiesta):
        """Colloca la richiesta dopo tutte quelle pendenti."""
        nuovo = _NodoCoda(richiesta)
        if self._coda is None:
            self._testa = nuovo
            self._coda = nuovo
        else:
            self._coda.successivo = nuovo
            self._coda = nuovo
        self._dimensione += 1

    def estrai(self):
        """Rimuove e restituisce la richiesta al fronte; su vuota solleva IndexError."""
        if self._testa is None:
            raise IndexError("estrazione da coda vuota")
        richiesta = self._testa.richiesta
        self._testa = self._testa.successivo
        if self._testa is None:
            self._coda = None
        self._dimensione -= 1
        return richiesta

    def fronte(self):
        """Restituisce la richiesta al fronte conservando la coda; su vuota IndexError."""
        if self._testa is None:
            raise IndexError("fronte di coda vuota")
        return self._testa.richiesta

    def per_lista(self):
        """Restituisce le richieste pendenti nell'ordine di arrivo (ispezione di prova)."""
        raccolte = []
        corrente = self._testa
        while corrente is not None:
            raccolte.append(corrente.richiesta)
            corrente = corrente.successivo
        return raccolte


class ServizioConsultazione:
    """Servizio che elabora le richieste di consultazione nell'ordine di arrivo.

    Il servizio riceve la coda come collaboratore e prende i dati del registro
    **nel momento dell'elaborazione**: la stessa richiesta può essere elaborata
    su registri diversi senza essere modificata.
    """

    def __init__(self, coda):
        self._coda = coda
        self._elaborate = 0

    def __len__(self):
        return len(self._coda)

    @property
    def elaborate(self):
        """Numero di richieste elaborate dall'avvio del servizio."""
        return self._elaborate

    def pendenti(self):
        """Restituisce i codici delle richieste pendenti, dal fronte verso la coda."""
        if hasattr(self._coda, "per_lista"):
            return [r.codice for r in self._coda.per_lista()]
        elementi = list(self._coda._elementi)  # ispezione didattica della rappresentazione
        return [r.codice for r in elementi]

    def accoda_richiesta(self, richiesta):
        """Valida la richiesta e la colloca in coda; invalida -> eccezione senza effetti."""
        if not isinstance(richiesta, RichiestaConsultazione):
            raise TypeError("la richiesta deve essere un oggetto RichiestaConsultazione")
        if not isinstance(richiesta.codice, str) or richiesta.codice == "":
            raise ValueError("il codice deve essere una stringa non vuota")
        criterio = richiesta.criterio
        if not callable(getattr(criterio, "ammette", None)):
            raise TypeError("il criterio deve esporre ammette(preventivo) -> bool")
        if not callable(getattr(criterio, "descrizione", None)):
            raise TypeError("il criterio deve esporre descrizione() -> str")
        self._coda.accoda(richiesta)

    def elabora_prossima(self, registro):
        """Elabora la richiesta al fronte e restituisce il proprio esito.

        Sequenza dichiarata: fronte, calcolo, estrazione. Se il calcolo
        solleva un'eccezione, la richiesta resta al fronte e l'eccezione si
        propaga al chiamante; con coda vuota restituisce `None`.
        """
        if self._coda.vuota():
            return None
        richiesta = self._coda.fronte()
        codici = tuple(seleziona_codici(registro, richiesta.criterio))
        self._coda.estrai()
        self._elaborate += 1
        return EsitoConsultazione(
            richiesta.codice, richiesta.criterio.descrizione(), codici
        )

    def elabora_tutte(self, registro):
        """Elabora le richieste pendenti fino al vuoto, nell'ordine di arrivo."""
        esiti = []
        esito = self.elabora_prossima(registro)
        while esito is not None:
            esiti.append(esito)
            esito = self.elabora_prossima(registro)
        return esiti
