"""Sensore, attuatore e controllore simulati su CPython (OOP-04, sez. H; raccordo U14–U15).

Tre componenti **concreti e semplici**, senza ereditarietà applicativa e
senza Protocol: la collaborazione si legge dai costruttori e dalle chiamate.
Il controllore **riceve** il sensore e l'attuatore già costruiti dal
chiamante e chiama solo le loro operazioni pubbliche: non ispeziona i
dettagli interni, non tocca pin e non importa `machine`.

Contratto didattico (non una specifica di impianto reale):

- `SensoreSimulato` restituisce le letture di una sequenza fornita, una per
  chiamata; quando la sequenza è esaurita segnala l'esaurimento con
  `LetturaEsaurita`, un esito **dichiarato** e distinto da un errore di
  programma;
- `AttuatoreSimulato` conserva lo stato acceso/spento, osservabile;
- `Controllore` è costruito con una soglia (gradi Celsius) e mantiene lo
  **stato proprio**: il numero di passi compiuti. A ogni passo legge,
  decide e delega: l'attuatore viene **acceso per letture minori della
  soglia**, spento altrimenti. Con la sequenza 18, 20, 22 e soglia 20 gli
  stati dell'attuatore sono acceso, spento, spento.

L'ordine è sempre lettura → decisione → aggiornamento: un'esaurimento o
una lettura invalida **non** aggiorna l'attuatore prima della diagnosi. La
lettura invalida solleva `ValueError` e lo stato dell'attuatore resta
quello che era.

Nei test non esistono attese, casualità né accesso ai GPIO: la sequenza è
deterministica. L'intercambiabilità con sensore e attuatore reali, la
sostituzione strutturale e il lavoro su scheda proseguono nell'Unità 15 e
nel laboratorio ESP-06: qui conta il modello di esecuzione della delega.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


class LetturaEsaurita(Exception):
    """La sequenza di letture del sensore simulato è terminata."""


def _valida_lettura(valore):
    """Controlla una lettura: numero non booleano. Nessun risultato."""
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        raise ValueError(f"lettura: atteso un numero, ricevuto {type(valore).__name__}")
    return None


class SensoreSimulato:
    """Sensore che riproduce una sequenza fissata alla costruzione.

    `leggi()` restituisce il prossimo valore e lo consume; a sequenza
    esaurita solleva `LetturaEsaurita` a ogni chiamata successiva. Il
    sensore conserva il proprio indice: due sensori con la stessa sequenza
    sono indipendenti.
    """

    def __init__(self, sequenza):
        self._sequenza = list(sequenza)
        self._prossima = 0

    def leggi(self):
        """Restituisce la prossima lettura, oppure segnala l'esaurimento."""
        if self._prossima >= len(self._sequenza):
            raise LetturaEsaurita("nessuna lettura rimasta nella sequenza")
        valore = self._sequenza[self._prossima]
        self._prossima = self._prossima + 1
        _valida_lettura(valore)
        return valore


class AttuatoreSimulato:
    """Attuatore con stato acceso/spento, osservabile e modificabile dal controllore."""

    def __init__(self):
        self._acceso = False

    @property
    def acceso(self):
        """Stato corrente dell'attuatore. Sola lettura."""
        return self._acceso

    def accendi(self):
        """Porta l'attuatore allo stato acceso."""
        self._acceso = True
        return None

    def spegni(self):
        """Porta l'attuatore allo stato spento."""
        self._acceso = False
        return None


class Controllore:
    """Legge dal sensore, decide in base alla soglia e delega all'attuatore.

    Stato proprio: i passi compiuti. Collaboratori: il sensore e l'attuatore
    ricevuti dal costruttore, creati fuori e **non posseduti**: il
    controllore non ne gestisce il ciclo di vita.
    """

    def __init__(self, sensore, attuatore, soglia):
        if isinstance(soglia, bool) or not isinstance(soglia, (int, float)):
            raise ValueError(f"soglia: atteso un numero, ricevuto {type(soglia).__name__}")
        self._sensore = sensore
        self._attuatore = attuatore
        self._soglia = soglia
        self._passi = 0

    @property
    def passi(self):
        """Numero di passi compiuti. Sola lettura."""
        return self._passi

    def passo(self):
        """Esegue un passo: lettura, decisione e delega. `None` sul successo.

        Una lettura minore della soglia accende l'attuatore; maggiore o
        uguale lo spegne. Se la lettura non è disponibile o è invalida,
        l'attuatore **non** viene toccato e l'eccezione sale al chiamante.
        """
        lettura = self._sensore.leggi()
        if lettura < self._soglia:
            self._attuatore.accendi()
        else:
            self._attuatore.spegni()
        self._passi = self._passi + 1
        return None

    def esegui(self, numero_passi):
        """Esegue `numero_passi` passi, fermandosi alla prima eccezione.

        Il ciclo esterno ha un numero finito di passi: qui non esistono
        attese né cicli infiniti. Un'esaurimento interrompe l'esecuzione e
        sale al chiamante: decidere che cosa farne appartiene a chi usa il
        controllore, non al controllore stesso.
        """
        for _ in range(numero_passi):
            self.passo()
        return None


if __name__ == "__main__":
    sensore = SensoreSimulato([18, 20, 22])
    attuatore = AttuatoreSimulato()
    controllore = Controllore(sensore, attuatore, soglia=20)

    controllore.esegui(3)
    print("sequenza 18, 20, 22 con soglia 20:")
    print("attuatore acceso:", attuatore.acceso)
    print("passi compiuti:", controllore.passi)

    stati = []
    sensore2 = SensoreSimulato([18, 20, 22])
    attuatore2 = AttuatoreSimulato()
    controllore2 = Controllore(sensore2, attuatore2, soglia=20)
    for _ in range(3):
        controllore2.passo()
        stati.append(attuatore2.acceso)
    print("stati passo per passo:", stati)

    esaurito = SensoreSimulato([15])
    attuatore3 = AttuatoreSimulato()
    controllore3 = Controllore(esaurito, attuatore3, soglia=20)
    controllore3.passo()
    try:
        controllore3.passo()
    except LetturaEsaurita as errore:
        print("esaurimento:", errore)
    print("attuatore non toccato dopo l'esaurimento:", attuatore3.acceso)

    invalido = SensoreSimulato([True])
    controllore4 = Controllore(invalido, AttuatoreSimulato(), soglia=20)
    try:
        controllore4.passo()
    except ValueError as errore:
        print("lettura invalida:", errore)
