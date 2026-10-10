"""Modello a oggetti del registro dei preventivi: classe di sessione (U13).

Responsabilità del modulo: raccogliere in una classe lo stato di una sessione
del registro — i preventivi inseriti o caricati durante la sessione — e
offrire le operazioni già verificate come metodi. I record restano dizionari
dello schema adottato dalle tappe precedenti e gli algoritmi restano
riconoscibili: `registro_dominio.py` continua a validare e a compiere le
operazioni sulle liste, questa classe conserva lo stato della sessione e
decide come osservarlo e come sostituirlo.

Costrutti usati: classe, inizializzatore, attributi di istanza, `self` e
metodi — i contenuti dell'Unità 13. Il singolo preventivo non diventa una
classe: il record resta un dizionario e la scelta è motivata in
`documentazione/unita-13/modello.md`.

Conversioni esplicite fra stato interno e rappresentazione esterna:
`per_lista()` produce la lista di record attesa da `registro_persistenza` e
dalle funzioni storiche; `sostituisci_da_lista()` accetta una lista valida e
la sostituisce interamente — tutto valido oppure nessun effetto. Le
osservazioni `cerca()` e `per_lista()` restituiscono copie: nessun alias del
chiamante raggiunge i contenitori interni della sessione.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""
from registro_dominio import (
    aggiorna_record,
    cerca_preventivo,
    elimina_record,
    inserisci_record,
    riepilogo_per_destinazione,
    valida_registro,
)


class RegistroPreventivi:
    """Registro di una sessione: stato proprio e operazioni sui preventivi.

    Ogni istanza nasce vuota e conserva la propria lista di record: due
    sessioni non condividono contenitori nemmeno quando sono costruite nello
    stesso punto del programma. Gli esiti dei rifiuti sono booleani
    dichiarati dai contratti dei metodi: `False` indica che nessuna modifica
    è avvenuta e lo stato precedente resta interamente conservato.
    """

    def __init__(self):
        self._preventivi = []

    def numero(self):
        """Restituisce quanti preventivi contiene la sessione."""
        return len(self._preventivi)

    def inserisci(self, codice, destinazione, totale_cent):
        """Aggiunge il preventivo in coda e restituisce True, oppure False.

        Rifiuta senza effetti — esito False e stato conservato — i dati fuori
        dominio e i codici già presenti. Il controllo è quello già verificato
        di `inserisci_record`, eseguito sulla lista interna della sessione.
        """
        return inserisci_record(self._preventivi, codice, destinazione, totale_cent)

    def aggiorna(self, codice, destinazione, totale_cent):
        """Aggiorna il preventivo del codice e restituisce True, oppure False.

        Con codice assente o dati fuori dominio nessun campo viene toccato:
        la validazione completa del candidato precede ogni scrittura.
        """
        return aggiorna_record(self._preventivi, codice, destinazione, totale_cent)

    def elimina(self, codice):
        """Elimina il preventivo del codice; False se il codice è assente."""
        return elimina_record(self._preventivi, codice)

    def cerca(self, codice):
        """Restituisce una copia del record del codice, oppure None.

        Il risultato è un dizionario nuovo: modificarlo non cambia la
        sessione. L'assenza del codice ha esito None, distinto da un record
        presente con importo zero.
        """
        record = cerca_preventivo(self._preventivi, codice)
        if record is None:
            return None
        return dict(record)

    def per_lista(self):
        """Conversione esplicita verso la rappresentazione esterna.

        Restituisce la lista dei record dello schema, nell'ordine della
        sessione, con lista e dizionari nuovi: è il formato atteso da
        `registro_persistenza` per salvataggio, esportazione CSV e dalle
        funzioni storiche per riepiloghi e viste. La politica di copia è
        dichiarata: nessun contenitore è condiviso con lo stato interno.
        """
        copia = []
        for record in self._preventivi:
            copia.append(dict(record))
        return copia

    def sostituisci_da_lista(self, registro):
        """Sostituisce lo stato con la lista ricevuta; False se non valida.

        Controlla l'intera lista prima di ogni effetto: con un solo record non
        ammesso la sessione resta quella precedente. I record ricevuti vengono
        copiati, quindi la lista del chiamante e la sessione restano
        indipendenti anche dopo la sostituzione.
        """
        if valida_registro(registro) != "":
            return False
        nuova = []
        for record in registro:
            nuova.append(dict(record))
        self._preventivi = nuova
        return True

    def riepilogo_per_destinazione(self):
        """Restituisce il riepilogo già verificato sulla lista interna.

        È il contratto storico di `riepilogo_per_destinazione`, applicato
        allo stato della sessione senza esporlo.
        """
        return riepilogo_per_destinazione(self._preventivi)

    def totale_complessivo_cent(self):
        """Restituisce la somma dei totali della sessione in centesimi.

        Operazione aggiunta dalla modifica breve documentata in
        `documentazione/unita-13/prove.md`: deriva dai record già validati,
        non conserva un campo duplicato e lascia invariato lo stato.
        """
        somma = 0
        for record in self._preventivi:
            somma = somma + record["totale_cent"]
        return somma
