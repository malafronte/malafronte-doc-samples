"""Consultazione del registro con politiche intercambiabili (U15).

Responsabilità del modulo: definire una famiglia di **criteri di
consultazione** con un contratto comune e un **client stabile** che li usa
senza conoscere l'implementazione concreta. La variazione scelta per la tappa
è quella delle politiche di consultazione: due criteri decidono quali
preventivi ammettere — per destinazione o per soglia di importo — e il client
`seleziona_codici` resta identico al variare del criterio.

Contratto del criterio (`ammette`):

- **dati ammessi**: un valore `Preventivo` del modello U14;
- **risultato**: esattamente un `bool` — `True` ammette, `False` esclude;
- **effetti**: nessuno; la decisione non modifica il preventivo né la
  raccolta ed è deterministica per la stessa configurazione;
- **errori**: la configurazione non ammessa solleva `ErroreConfigurazione`
  alla costruzione, prima di ogni uso; un dato fuori dominio del preventivo
  è intercettato dal modello alla costruzione del valore;
- **invarianti**: la configurazione del criterio non cambia dopo la
  costruzione.

Promesse del client `seleziona_codici(registro, criterio)`:

- restituisce una **lista nuova** di codici, nell'ordine della raccolta;
- conserva l'**identità di dominio** dei codici: `"007"` resta `"007"`;
- non modifica il registro: la proiezione `per_lista()` è invariata;
- con raccolta vuota restituisce `[]` senza chiamare il criterio;
- un risultato che non è esattamente un `bool` solleva `TypeError` prima di
  aggiungere qualsiasi elemento.

Organizzazione scelta: componenti autonomi con **duck typing** documentato e
**composizione** — il client riceve il criterio dal punto di avvio. Le
alternative — famiglia per ereditarietà, dichiarazione con ABC o `Protocol` —
sono confrontate in `documentazione/unita-15/contratti-e-scelte.md`. La
variante breve `PoliticaSogliaEsclusiva` mostra l'estensione della famiglia
senza modificare il client.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""
from registro_dominio import DESTINAZIONI_AMMESSE


class ErroreConfigurazione(ValueError):
    """La configurazione del criterio non è ammessa dal proprio contratto."""


class PoliticaDestinazione:
    """Criterio che ammette i preventivi di una destinazione scelta."""

    def __init__(self, destinazione):
        if destinazione not in DESTINAZIONI_AMMESSE:
            raise ErroreConfigurazione(
                f"configurazione: destinazione non ammessa: {destinazione!r}"
            )
        self._destinazione = destinazione

    def descrizione(self):
        """Restituisce il testo della configurazione scelta."""
        return f"destinazione = {self._destinazione}"

    def ammette(self, preventivo):
        """Restituisce True se il preventivo ha la destinazione configurata."""
        return preventivo.destinazione == self._destinazione


class PoliticaSoglia:
    """Criterio che ammette i preventivi con totale maggiore o uguale alla soglia."""

    def __init__(self, minimo_cent):
        if isinstance(minimo_cent, bool) or not isinstance(minimo_cent, int):
            raise ErroreConfigurazione(
                f"configurazione: soglia attesa come intero: {minimo_cent!r}"
            )
        if minimo_cent < 0:
            raise ErroreConfigurazione(
                f"configurazione: soglia negativa non ammessa: {minimo_cent}"
            )
        self._minimo_cent = minimo_cent

    def descrizione(self):
        """Restituisce il testo della configurazione scelta."""
        return f"soglia >= {self._minimo_cent} centesimi"

    def ammette(self, preventivo):
        """Restituisce True se il totale raggiunge la soglia configurata."""
        return preventivo.totale_cent >= self._minimo_cent


class PoliticaSogliaEsclusiva:
    """Variante breve: ammette i preventivi con totale strettamente oltre la soglia.

    Integra una terza implementazione senza modificare il client: mostra
    l'estensione della famiglia descritta nel caso PU15-08 e il confine
    diverso rispetto a `PoliticaSoglia` sulla stessa soglia.
    """

    def __init__(self, minimo_cent):
        if isinstance(minimo_cent, bool) or not isinstance(minimo_cent, int):
            raise ErroreConfigurazione(
                f"configurazione: soglia attesa come intero: {minimo_cent!r}"
            )
        if minimo_cent < 0:
            raise ErroreConfigurazione(
                f"configurazione: soglia negativa non ammessa: {minimo_cent}"
            )
        self._minimo_cent = minimo_cent

    def descrizione(self):
        """Restituisce il testo della configurazione scelta."""
        return f"soglia > {self._minimo_cent} centesimi"

    def ammette(self, preventivo):
        """Restituisce True se il totale supera strettamente la soglia."""
        return preventivo.totale_cent > self._minimo_cent


def seleziona_codici(registro, criterio) -> list:
    """Restituisce i codici dei preventivi ammessi dal criterio.

    Il client è comune a ogni criterio compatibile: chiama `ammette` su ogni
    preventivo della raccolta, nell'ordine, e raccoglie i codici ammessi in
    una lista nuova. Il registro non viene modificato. Un risultato di
    `ammette` che non è esattamente un `bool` solleva `TypeError` senza
    consegnare risultati parziali.
    """
    if registro.numero == 0:
        return []
    risultato = []
    for preventivo in registro.preventivi():
        ammesso = criterio.ammette(preventivo)
        if type(ammesso) is not bool:
            raise TypeError("ammette: atteso esattamente bool")
        if ammesso:
            risultato.append(preventivo.codice)
    return risultato
