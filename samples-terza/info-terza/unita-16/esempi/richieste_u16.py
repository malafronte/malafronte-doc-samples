"""Elaborazione di richieste in ordine di arrivo - Unità 16 (PY-31).

Problema svolto: richieste sintetiche con `codice` e durata intera in unità
convenzionali vengono elaborate in ordine FIFO da un servizio sequenziale. La
durata viene sommata su un orologio logico: le prove restano deterministiche e
non introducono attese reali. Il servizio riceve la coda come collaboratore,
così lo stesso client funziona con `CodaDeque` e `CodaConcatenata`.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations

from dataclasses import dataclass

from pile_code_u16 import CodaDeque


@dataclass(frozen=True)
class Richiesta:
    """Richiesta sintetica da elaborare: codice identificativo e durata positiva."""

    codice: str
    durata: int


@dataclass(frozen=True)
class Esito:
    """Risultato dell'elaborazione di una richiesta sull'orologio logico del servizio."""

    codice: str
    durata: int
    completata_a: int


class ServizioRichieste:
    """Servizio sequenziale che elabora le richieste nell'ordine di arrivo.

    Politica del vuoto: `elabora_prossima` su coda vuota restituisce None e
    conserva lo stato. Una richiesta invalida viene rifiutata prima
    dell'accodamento e non modifica la coda.
    """

    def __init__(self, coda) -> None:
        self._coda = coda
        self.tempo_trascorso = 0

    def __len__(self) -> int:
        return len(self._coda)

    def pendenti(self) -> list[str]:
        """Restituisce i codici delle richieste pendenti, dal fronte verso la coda.

        L'ispezione attraverso il collaboratore è uno strumento di verifica del
        servizio: il contratto pubblico della coda non espone la rappresentazione.
        """
        elementi = self._coda._elementi  # ispezione didattica della rappresentazione
        valori = elementi.a_lista() if hasattr(elementi, "a_lista") else list(elementi)
        return [richiesta.codice for richiesta in valori]

    def accoda_richiesta(self, richiesta: Richiesta) -> None:
        """Valida `richiesta` e la colloca in coda; invalida -> eccezione senza effetti.

        Tipo errato -> TypeError; campo fuori dominio -> ValueError. In entrambi
        i casi la coda e la sua dimensione restano inalterate.
        """
        if not isinstance(richiesta, Richiesta):
            raise TypeError("la richiesta deve essere un oggetto Richiesta")
        if not isinstance(richiesta.codice, str) or richiesta.codice == "":
            raise ValueError("il codice deve essere una stringa non vuota")
        if type(richiesta.durata) is not int:
            raise TypeError("la durata deve essere un intero")
        if richiesta.durata <= 0:
            raise ValueError("la durata deve essere positiva")
        self._coda.accoda(richiesta)

    def elabora_prossima(self) -> Esito | None:
        """Estrae la richiesta al fronte, somma la durata e restituisce l'esito.

        L'estrazione avviene dopo il calcolo dell'esito: se l'elaborazione
        fallisse, la richiesta resterebbe al fronte.
        """
        if self._coda.vuota():
            return None
        richiesta = self._coda.fronte()
        completata_a = self.tempo_trascorso + richiesta.durata
        self._coda.estrai()
        self.tempo_trascorso = completata_a
        return Esito(richiesta.codice, richiesta.durata, completata_a)

    def elabora_tutte(self) -> list[Esito]:
        """Elabora le richieste pendenti fino al vuoto, in ordine di arrivo."""
        esiti = []
        esito = self.elabora_prossima()
        while esito is not None:
            esiti.append(esito)
            esito = self.elabora_prossima()
        return esiti


if __name__ == "__main__":
    servizio = ServizioRichieste(CodaDeque())
    for codice, durata in [("R01", 2), ("R02", 1), ("R03", 3)]:
        servizio.accoda_richiesta(Richiesta(codice, durata))
    print("pendenti:", servizio.pendenti())
    # Un'estrazione e un nuovo inserimento verificano il significato FIFO.
    print("prima elaborazione:", servizio.elabora_prossima())
    servizio.accoda_richiesta(Richiesta("R04", 1))
    for esito in servizio.elabora_tutte():
        print("elaborata:", esito)
