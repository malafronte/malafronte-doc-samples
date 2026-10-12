"""Simulazione dell'indirizzamento aperto con sondaggio lineare — Unità 18.

Il modulo offre la traccia della seconda strategia del capitolo: le
associazioni occupano direttamente le posizioni della tabella e la sequenza di
sondaggio `(h(chiave) + j) % m` seleziona le posizioni successive da esaminare
durante ricerca e inserimento. Ogni posizione è **vuota** (mai usata),
**occupata** oppure **cancellata** (marcatore che conserva la continuità del
percorso): la ricerca conclude al primo spazio mai usato e attraversa i
marcatori, così una chiave oltre una cancellazione resta raggiungibile.

La classe è uno strumento di simulazione delle tracce del capitolo, con chiavi
intere didattiche; l'implementazione integrale della seconda strategia è un
approfondimento con file e pagina distinti. Ogni sondaggio ha un limite
esplicito di `m` posizioni.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

#: Stati di una posizione della tabella a sondaggio.
VUOTA = "vuota"
OCCUPATA = "occupata"
CANCELLATA = "cancellata"


class SondaggioLineare:
    """Tabella a indirizzamento aperto con sondaggio lineare e marcatori.

    La funzione hash didattica è l'identità sugli interi; la sequenza di
    sondaggio somma il tentativo all'hash e riduce modulo la capacità. La
    politica ordinaria mantiene una capacità libera, così esiste sempre uno
    spazio mai usato di arresto.
    """

    def __init__(self, capacita=7):
        """Crea una tabella di `capacita` posizioni tutte mai usate."""
        if isinstance(capacita, bool) or not isinstance(capacita, int):
            raise TypeError(f"capacità attesa di tipo int, ricevuto {type(capacita).__name__}")
        if capacita < 1:
            raise ValueError(f"capacità minima 1, ricevuto {capacita}")
        self._stato = [VUOTA] * capacita
        self._chiavi = [None] * capacita
        self._valori = [None] * capacita
        self._attive = 0

    def __len__(self):
        """Restituisce il numero di associazioni attive (senza i marcatori)."""
        return self._attive

    @property
    def capacita(self):
        """Restituisce il numero delle posizioni."""
        return len(self._stato)

    @property
    def marcatori(self):
        """Restituisce il numero delle posizioni cancellate."""
        return sum(1 for stato in self._stato if stato == CANCELLATA)

    def occupazione_attiva(self):
        """Restituisce il rapporto fra associazioni attive e posizioni."""
        return self._attive / len(self._stato)

    def pressione_sondaggio(self):
        """Restituisce il rapporto fra posizioni usate e posizioni.

        Le posizioni usate comprendono le associazioni attive e i marcatori:
        entrambe le quantità influenzano la lunghezza delle sequenze e la
        scelta di ricostruzione.
        """
        usate = self._attive + self.marcatori
        return usate / len(self._stato)

    @staticmethod
    def _valida_chiave(chiave):
        if type(chiave) is not int:
            raise TypeError(f"chiave attesa di tipo int, ricevuto {type(chiave).__name__}")

    def sonde_per(self, chiave):
        """Restituisce la lista delle posizioni esaminate per `chiave`.

        La sequenza segue `(chiave + j) % m` fino a `m` posizioni: è lo
        strumento di traccia del capitolo, distinto dalle operazioni che
        decidono l'esito.
        """
        self._valida_chiave(chiave)
        capacita = len(self._stato)
        return [(chiave + tentativo) % capacita for tentativo in range(capacita)]

    def cerca(self, chiave):
        """Restituisce il valore associato a `chiave`.

        La ricerca attraversa posizioni occupate e marcatori e conclude al
        primo spazio mai usato oppure dopo `m` sonde; la chiave assente
        solleva `KeyError`.
        """
        self._valida_chiave(chiave)
        for posizione in self.sonde_per(chiave):
            stato = self._stato[posizione]
            if stato == VUOTA:
                break
            if stato == OCCUPATA and self._chiavi[posizione] == chiave:
                return self._valori[posizione]
        raise KeyError(chiave)

    def contiene(self, chiave):
        """Restituisce `True` se `chiave` è presente, `False` altrimenti."""
        try:
            self.cerca(chiave)
            return True
        except KeyError:
            return False

    def inserisci(self, chiave, valore):
        """Inserisce la chiave nuova oppure aggiorna la chiave presente.

        La ricerca prosegue oltre il primo marcatore per trovare un eventuale
        duplicato: una chiave già presente riceve il nuovo valore senza
        cambiare il numero di associazioni. Per una chiave nuova la prima
        posizione cancellata incontrata viene ricordata e, completata la
        verifica della presenza, riutilizzata. La tabella senza alcuno spazio
        libero solleva `OverflowError`.
        """
        self._valida_chiave(chiave)
        primo_marcatore = None
        for posizione in self.sonde_per(chiave):
            stato = self._stato[posizione]
            if stato == OCCUPATA and self._chiavi[posizione] == chiave:
                self._valori[posizione] = valore
                return
            if stato == CANCELLATA and primo_marcatore is None:
                primo_marcatore = posizione
            if stato == VUOTA:
                destinazione = primo_marcatore if primo_marcatore is not None else posizione
                self._stato[destinazione] = OCCUPATA
                self._chiavi[destinazione] = chiave
                self._valori[destinazione] = valore
                self._attive += 1
                return
        if primo_marcatore is not None:
            self._stato[primo_marcatore] = OCCUPATA
            self._chiavi[primo_marcatore] = chiave
            self._valori[primo_marcatore] = valore
            self._attive += 1
            return
        raise OverflowError("tabella a sondaggio senza posizioni libere")

    def rimuovi(self, chiave):
        """Elimina l'associazione e marca la posizione come cancellata.

        Il marcatore conserva la continuità del percorso: le ricerche delle
        chiavi oltre la posizione proseguono. La chiave assente solleva
        `KeyError` e conserva lo stato.
        """
        self._valida_chiave(chiave)
        for posizione in self.sonde_per(chiave):
            stato = self._stato[posizione]
            if stato == VUOTA:
                break
            if stato == OCCUPATA and self._chiavi[posizione] == chiave:
                valore = self._valori[posizione]
                self._stato[posizione] = CANCELLATA
                self._chiavi[posizione] = None
                self._valori[posizione] = None
                self._attive -= 1
                return valore
        raise KeyError(chiave)

    def fotografia(self):
        """Restituisce la lista delle posizioni come tuple `(stato, chiave, valore)`."""
        return list(zip(self._stato, self._chiavi, self._valori, strict=True))


def traccia_canonica():
    """Costruisce la traccia canonica del capitolo e la restituisce in un dizionario.

    La tabella ha `m = 7`; l'inserimento di `5, 12, 19` occupa le posizioni
    `5, 6, 0`. La rimozione di `12` marca la posizione 6; la ricerca e
    l'aggiornamento di `19` attraversano il marcatore e raggiungono la
    posizione 0. La ricerca di `26` esamina `5, 6, 0` e conclude alla posizione
    `1` mai usata.
    """
    tabella = SondaggioLineare(7)
    tabella.inserisci(5, "E5")
    tabella.inserisci(12, "E12")
    tabella.inserisci(19, "E19")
    dopo_inserimenti = tabella.fotografia()
    sonde_19 = []
    corrente = 19
    for posizione in tabella.sonde_per(corrente):
        sonde_19.append(posizione)
        if tabella._stato[posizione] == OCCUPATA and tabella._chiavi[posizione] == corrente:
            break
    tabella.rimuovi(12)
    dopo_cancellazione = tabella.fotografia()
    valore_19 = tabella.cerca(19)
    tabella.inserisci(19, "E19b")
    tabella.inserisci(26, "E26")
    return {
        "dopo_inserimenti": dopo_inserimenti,
        "sonde_19": sonde_19,
        "dopo_cancellazione": dopo_cancellazione,
        "valore_19_oltre_marcatore": valore_19,
        "valore_19_aggiornato": tabella.cerca(19),
        "posizione_26": tabella.sonde_per(26),
        "fotografia_finale": tabella.fotografia(),
    }
