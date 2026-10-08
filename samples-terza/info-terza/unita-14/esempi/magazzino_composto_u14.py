"""Il magazzino composto: la raccolta con le regole dell'insieme (OOP-03, sez. K; OOP-04).

Confronto circoscritto con la versione U13: lì ricerca, unicità e
operazioni erano **funzioni esterne** che ricevevano la lista; qui la
raccolta diventa una classe `Magazzino` che possiede il proprio contenitore
e ne mantiene gli invarianti. Lo schema dei dati, i centesimi, i menu e le
politiche di persistenza **non cambiano**.

Responsabilità della raccolta:

- codici **univoci** nell'intero magazzino (vincolo dell'insieme, non del
  singolo articolo);
- in inserimento l'articolo viene **ricostruito dai dati validi**: nessun
  alias esterno di un candidato può poi mutare lo stato interno;
- ricerca e riepilogo restituiscono **proiezioni** `DatiArticolo` frozen o
  record primitivi, mai riferimenti mutabili interni;
- la modifica per codice **conserva l'identità** dell'istanza esistente e
  chiama `aggiorna`: i tre campi vengono verificati insieme, un rifiuto
  non produce aggiornamenti parziali.

Esiti dichiarati, gli stessi della versione U13: `inserisci` restituisce
`None` e solleva `ValueError` su duplicato o dati invalidi; `cerca` restituisce
lo snapshot oppure `None`; `modifica` restituisce `False` se assente, `True`
se applicato, `ValueError` su candidato invalido; `elimina` restituisce
`False` se assente, `True` se eliminato e non pone domande all'utente; il
`riepilogo` sul vuoto produce tre zeri. La ricerca interna usa **indici**:
la prima posizione è `0` e non viene confusa con l'assenza.

Nessun metodo apre file, stampa o legge input: dominio e confini restano
separati.

Ambiente: CPython sul computer. Dipende da `Articolo` e `DatiArticolo`.
"""

from articolo_proprieta_u14 import Articolo, valida_dati_articolo


class Magazzino:
    """Raccolta di articoli con codici univoci e proiezioni protette.

    Invarianti: ogni elemento è un `Articolo` valido e i codici sono unici
    nell'intera raccolta. Ogni istanza crea il **proprio** contenitore: due
    magazzini non condividono nulla.
    """

    def __init__(self):
        self._articoli = []

    def _indice_di(self, codice):
        """Indice dell'articolo con quel codice, oppure `None`.

        Ricerca lineare senza mutazione. L'indice `0` è una posizione
        valida e valida quanto le altre: l'assenza si esprime solo con
        `None`, mai con un valore di ritorno "falso".
        """
        for indice, articolo in enumerate(self._articoli):
            if articolo.ha_codice(codice):
                return indice
        return None

    def inserisci(self, codice, descrizione, quantita, prezzo_centesimi):
        """Aggiunge un articolo ricostruito dai dati validi. `None` sul successo.

        L'articolo viene costruito **qui**, dai quattro valori: un alias
        esterno di un eventuale candidato non può mutare lo stato interno.
        `ValueError` su dati invalidi o codice duplicato; nessuna modifica
        su rifiuto.
        """
        valida_dati_articolo(codice, descrizione, quantita, prezzo_centesimi)
        if self._indice_di(codice) is not None:
            raise ValueError(f"codice {codice!r}: già presente nel magazzino")
        self._articoli.append(Articolo(codice, descrizione, quantita, prezzo_centesimi))
        return None

    def cerca(self, codice):
        """Restituisce lo snapshot `DatiArticolo` oppure `None`. Nessuna mutazione."""
        indice = self._indice_di(codice)
        if indice is None:
            return None
        return self._articoli[indice].dati()

    def modifica(self, codice, descrizione, quantita, prezzo_centesimi):
        """Aggiorna l'articolo esistente, conservandone l'identità.

        `False` se il codice è assente, `True` se applicato; `ValueError` su
        candidato invalido, **senza** modifica. L'aggiornamento avviene con
        `aggiorna` sull'istanza presente nella raccolta: gli alias di
        quell'istanza osservano il cambiamento, come nella versione U13.
        """
        indice = self._indice_di(codice)
        if indice is None:
            return False
        self._articoli[indice].aggiorna(descrizione, quantita, prezzo_centesimi)
        return True

    def elimina(self, codice):
        """Rimuove l'articolo con quel codice. `True` se eliminato, `False` se assente."""
        indice = self._indice_di(codice)
        if indice is None:
            return False
        del self._articoli[indice]
        return True

    def articoli(self):
        """Tupla degli snapshot `DatiArticolo`, nell'ordine di inserimento.

        Contenitore non modificabile e proiezioni frozen: né `append` sulla
        tupla né scritture sugli snapshot toccano il magazzino.
        """
        return tuple(articolo.dati() for articolo in self._articoli)

    def riepilogo(self):
        """Nuovo dizionario con `articoli`, `quantita_totale`, `valore_centesimi`.

        Il calcolo delega il valore all'articolo (`valore_centesimi`) e non
        ispeziona i suoi dettagli interni. La lista vuota produce tre zeri.
        """
        numero_articoli = 0
        quantita_totale = 0
        valore_totale = 0
        for articolo in self._articoli:
            numero_articoli = numero_articoli + 1
            quantita_totale = quantita_totale + articolo.quantita
            valore_totale = valore_totale + articolo.valore_centesimi
        return {
            "articoli": numero_articoli,
            "quantita_totale": quantita_totale,
            "valore_centesimi": valore_totale,
        }


if __name__ == "__main__":
    magazzino = Magazzino()
    print("vuoto:", magazzino.riepilogo())

    magazzino.inserisci("007", "Vite, lunga", 4, 25)
    magazzino.inserisci("012", 'Caffè "A"', 2, 350)
    print("canonico:", magazzino.riepilogo())

    try:
        magazzino.inserisci("007", "duplicato", 1, 1)
    except ValueError as errore:
        print("inserimento rifiutato:", errore)

    print("cerca 007:", magazzino.cerca("007"))
    print("cerca 7:", magazzino.cerca("7"))

    print("modifica assente:", magazzino.modifica("999", "x", 1, 1))
    print("modifica valida:", magazzino.modifica("007", "Vite, lunga", 6, 25))
    try:
        magazzino.modifica("012", 'Caffè "A"', -2, 350)
    except ValueError as errore:
        print("modifica rifiutata:", errore)
    print("dopo il rifiuto:", magazzino.cerca("012"))
    print("riepilogo aggiornato:", magazzino.riepilogo())

    snapshot = magazzino.cerca("007")
    print("elimina 012:", magazzino.elimina("012"))
    print("elimina di nuovo:", magazzino.elimina("012"))
    print("alias dello snapshot sopravvissuto:", snapshot)

    proiezioni = magazzino.articoli()
    print("proiezioni:", proiezioni)
    altro = Magazzino()
    altro.inserisci("100", "Isolato", 1, 1)
    print("due magazzini indipendenti:", magazzino.riepilogo(), altro.riepilogo())
