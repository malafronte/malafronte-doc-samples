"""Modello robusto del registro: valori immutabili e raccolta responsabile (U14).

Responsabilità del modulo: rappresentare il singolo preventivo come **valore**
validato e immutabile, e la sessione come **raccolta** responsabile degli
invarianti d'insieme — unicità dei codici, ordine, aggiornamenti controllati.
Le regole dei valori restano quelle già verificate: la costruzione di
`Preventivo` richiama `valida_dominio_record`, così dominio e diagnosi non si
duplicano.

Strumenti dell'Unità 14 usati dove rispondono a un requisito:

- **dataclass frozen** per il valore: campi dichiarati, uguaglianza per
  contenuto, `repr` leggibile, impossibilità di aggiornare i campi — il
  valore non ha un ciclo di vita mutabile;
- **eccezioni di dominio** per i rifiuti della raccolta: `DatoNonAmmesso`,
  `CodiceDuplicato`, `CodiceAssente` — esiti dichiarati nei contratti e
  presentati dalla CLI al proprio confine;
- **proprietà derivate** `numero` e `totale_complessivo_cent`: calcolate dai
  record già validati, mai memorizzate come campi duplicati;
- **proiezioni esplicite** `per_lista()` e `sostituisci_da_lista()` per CSV e
  JSON: nessuna esportazione opaca degli attributi, nessun `pickle`.

Effetti sugli alias, dichiarati: `aggiorna` sostituisce l'intero valore nella
posizione del codice; chi conserva un riferimento al valore precedente continua
a osservarlo, senza legare le sorti dei due oggetti. Gli snapshot sono tuple di
valori frozen: nessuna mutazione esterna nascosta dello stato interno.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""
from dataclasses import dataclass

from registro_dominio import (
    DESTINAZIONI_AMMESSE,
    riepilogo_per_destinazione,
    valida_dominio_record,
)


class DatoNonAmmesso(ValueError):
    """Un campo del candidato non rispetta il dominio del preventivo."""


class CodiceDuplicato(ValueError):
    """La raccolta contiene già un preventivo con lo stesso codice esatto."""


class CodiceAssente(ValueError):
    """La raccolta non contiene alcun preventivo con il codice richiesto."""


@dataclass(frozen=True)
class Preventivo:
    """Valore immutabile di un preventivo: codice, destinazione e totale.

    La costruzione valida il candidato completo e solleva `DatoNonAmmesso`
    senza consegnare un valore parziale. L'uguaglianza è per contenuto sui tre
    campi: due valori costruiti con gli stessi dati sono uguali, ma restano
    oggetti distinti — `is` e `==` rispondono a domande diverse.
    """

    codice: str
    destinazione: str
    totale_cent: int

    def __post_init__(self):
        errore = valida_dominio_record(
            {
                "codice": self.codice,
                "destinazione": self.destinazione,
                "totale_cent": self.totale_cent,
            }
        )
        if errore != "":
            raise DatoNonAmmesso(errore)


def preventivo_da_record(record: dict) -> Preventivo:
    """Conversione esplicita dal record dello schema al valore del modello.

    La validazione è quella della costruzione: un record non ammesso solleva
    `DatoNonAmmesso` prima di produrre alcun valore.
    """
    return Preventivo(record["codice"], record["destinazione"], record["totale_cent"])


def record_da_preventivo(preventivo: Preventivo) -> dict:
    """Conversione esplicita dal valore del modello al record dello schema.

    Restituisce un dizionario nuovo: la proiezione non condivide oggetti con
    il modello ed è il formato atteso da `registro_persistenza`.
    """
    return {
        "codice": preventivo.codice,
        "destinazione": preventivo.destinazione,
        "totale_cent": preventivo.totale_cent,
    }


class RegistroPreventivi:
    """Raccolta responsabile: unicità dei codici, ordine e snapshot protetti.

    Lo stato è la sequenza ordinata dei valori `Preventivo`. Gli aggiornamenti
    sostituiscono l'intero valore nella posizione del codice: non esistono
    modifiche parziali di un record. I rifiuti sono eccezioni di dominio,
    dichiarate dai contratti dei metodi.
    """

    def __init__(self):
        self._preventivi = []

    @property
    def numero(self):
        """Numero dei preventivi della raccolta, derivato dallo stato."""
        return len(self._preventivi)

    @property
    def totale_complessivo_cent(self):
        """Somma dei totali in centesimi, derivata dai valori già validati."""
        somma = 0
        for preventivo in self._preventivi:
            somma = somma + preventivo.totale_cent
        return somma

    def inserisci(self, codice, destinazione, totale_cent) -> Preventivo:
        """Aggiunge il preventivo in coda e restituisce il valore creato.

        Solleva `DatoNonAmmesso` per i dati fuori dominio e `CodiceDuplicato`
        per un codice già presente: in entrambi i casi nessun effetto, la
        raccolta resta com'era.
        """
        nuovo = Preventivo(codice, destinazione, totale_cent)
        if self.per_codice(nuovo.codice) is not None:
            raise CodiceDuplicato(f"codice duplicato: {nuovo.codice!r}")
        self._preventivi.append(nuovo)
        return nuovo

    def aggiorna(self, codice, destinazione, totale_cent) -> Preventivo:
        """Sostituisce il valore del codice e restituisce il valore nuovo.

        Il candidato viene costruito e validato per intero prima di ogni
        effetto: con un campo non ammesso ordine e valori precedenti restano
        invariati. Un codice assente solleva `CodiceAssente`.
        """
        nuovo = Preventivo(codice, destinazione, totale_cent)
        for posizione in range(len(self._preventivi)):
            if self._preventivi[posizione].codice == nuovo.codice:
                self._preventivi[posizione] = nuovo
                return nuovo
        raise CodiceAssente(f"codice assente: {nuovo.codice!r}")

    def elimina(self, codice) -> None:
        """Elimina il preventivo del codice; solleva `CodiceAssente` se manca."""
        for posizione in range(len(self._preventivi)):
            if self._preventivi[posizione].codice == codice:
                del self._preventivi[posizione]
                return None
        raise CodiceAssente(f"codice assente: {codice!r}")

    def per_codice(self, codice):
        """Restituisce il valore del codice, oppure None se è assente.

        Il confronto dei codici è esatto: `"007"` e `"7"` sono distinti.
        """
        for preventivo in self._preventivi:
            if preventivo.codice == codice:
                return preventivo
        return None

    def per_destinazione(self, destinazione) -> tuple:
        """Restituisce la tupla dei preventivi della destinazione richiesta.

        Modifica breve documentata in `documentazione/unita-14/prove-e-revisione.md`:
        la destinazione viene validata prima della ricerca e il risultato è
        una tupla protetta, nell'ordine della raccolta.
        """
        if destinazione not in DESTINAZIONI_AMMESSE:
            raise DatoNonAmmesso(f"dominio: destinazione non ammessa: {destinazione!r}")
        selezionati = []
        for preventivo in self._preventivi:
            if preventivo.destinazione == destinazione:
                selezionati.append(preventivo)
        return tuple(selezionati)

    def preventivi(self) -> tuple:
        """Snapshot protetto della raccolta: tupla dei valori nell'ordine.

        Il contenitore è immutabile e i valori sono frozen: nessuna
        mutazione esterna dello stato interno è possibile.
        """
        return tuple(self._preventivi)

    def per_lista(self) -> list:
        """Proiezione esplicita verso i record dello schema, con copie.

        È il formato atteso da `registro_persistenza` per salvataggio, CSV e
        dalle funzioni storiche per riepiloghi e viste.
        """
        lista = []
        for preventivo in self._preventivi:
            lista.append(record_da_preventivo(preventivo))
        return lista

    def sostituisci_da_lista(self, registro) -> None:
        """Sostituisce l'intera raccolta con i record ricevuti.

        Tutti i candidati vengono costruiti, validati e controllati per
        duplicati **prima** di ogni effetto: con un solo problema la raccolta
        resta quella precedente e vengono sollevate le eccezioni di dominio
        corrispondenti.
        """
        nuovi = []
        codici_visti = []
        for record in registro:
            preventivo = preventivo_da_record(record)
            if preventivo.codice in codici_visti:
                raise CodiceDuplicato(f"codice duplicato: {preventivo.codice!r}")
            codici_visti.append(preventivo.codice)
            nuovi.append(preventivo)
        self._preventivi = nuovi

    def riepilogo_per_destinazione(self) -> dict:
        """Riepilogo storico per destinazione, sulla proiezione esplicita."""
        return riepilogo_per_destinazione(self.per_lista())
