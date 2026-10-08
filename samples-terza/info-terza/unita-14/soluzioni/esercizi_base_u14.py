"""Soluzioni formative della raccolta di base dell'Unità 14.

Riferimenti eseguibili per le schede della raccolta
`unita-14-oggetti-robusti-composizione` il cui prodotto è codice. Le
spiegazioni complete — ragionamento, verifica ed errore da evitare — sono
nelle soluzioni pubblicate sulla pagina; qui vivono le versioni eseguibili,
con un docstring che richiama l'esercizio.

Le classi deliberatamente difettose sono marcate nel nome e nella
docstring: servono da confronto, non da modello.

Ambiente: CPython sul computer. Dipende dai moduli in `esempi/` dove la
consegna lo richiede.
"""

from dataclasses import dataclass, field

from articolo_proprieta_u14 import Articolo as ArticoloProprieta
from articolo_proprieta_u14 import DatiArticolo
from intervalli_u14 import Intervallo
from persistenza_magazzino_u14 import dati_a_riga, riga_a_dati
from prenotazioni_u14 import Prenotazione, RegistroPrenotazioni

# --- PY-U14-E01: il setter che riassegna alla proprietà stessa -------------


class LimitiRicorsivo:
    """DELIBERATAMENTE DIFETTOSO (PY-U14-E01): il setter richiama se stesso.

    `self.minimo = valore` dentro il setter di `minimo` fa ripartire il
    setter, ancora e ancora, fino al limite di ricorsione.
    """

    def __init__(self, minimo, massimo):
        self._massimo = massimo
        self._minimo = minimo

    @property
    def minimo(self):
        return self._minimo

    @minimo.setter
    def minimo(self, valore):
        if valore > self._massimo:
            raise ValueError(f"minimo {valore} supera il massimo {self._massimo}")
        self.minimo = valore  # difetto: riassegna la proprietà, non il campo

    @property
    def massimo(self):
        return self._massimo


class LimitiCorretto:
    """Versione corretta di PY-U14-E01: il setter scrive il dettaglio interno."""

    def __init__(self, minimo, massimo):
        if minimo > massimo:
            raise ValueError(f"atteso minimo <= massimo, ricevuti ({minimo}, {massimo})")
        self._minimo = minimo
        self._massimo = massimo

    @property
    def minimo(self):
        return self._minimo

    @minimo.setter
    def minimo(self, valore):
        if valore > self._massimo:
            raise ValueError(f"minimo {valore} supera il massimo {self._massimo}")
        self._minimo = valore  # dopo il controllo, si scrive il campo interno

    @property
    def massimo(self):
        return self._massimo


# --- PY-U14-E02: la modifica di tre campi che fallisce a metà --------------


class AttivitaParziale:
    """DELIBERATAMENTE DIFETTOSA (PY-U14-E02): tre scritture separate.

    La terza validazione fallisce **dopo** le prime due scritture: lo stato
    resta a metà fra il vecchio e il nuovo valore.
    """

    def __init__(self, giorno, ora, aula):
        self._giorno = giorno
        self._ora = ora
        self._aula = aula

    def sposta(self, giorno, ora, aula):
        self._giorno = giorno
        self._ora = ora
        if not isinstance(aula, str) or aula == "":
            raise ValueError("campo 'aula': testo non vuoto")
        self._aula = aula

    def dati(self):
        return (self._giorno, self._ora, self._aula)


class Attivita:
    """Versione corretta di PY-U14-E02: il candidato completo prima delle scritture."""

    def __init__(self, giorno, ora, aula):
        self._valida(giorno, ora, aula)
        self._giorno = giorno
        self._ora = ora
        self._aula = aula

    @staticmethod
    def _valida(giorno, ora, aula):
        if isinstance(giorno, bool) or not isinstance(giorno, int) or not 1 <= giorno <= 5:
            raise ValueError(f"campo 'giorno': atteso un intero fra 1 e 5, ricevuto {giorno!r}")
        if isinstance(ora, bool) or not isinstance(ora, int) or not 8 <= ora <= 17:
            raise ValueError(f"campo 'ora': atteso un intero fra 8 e 17, ricevuto {ora!r}")
        if not isinstance(aula, str) or aula == "" or aula != aula.strip():
            raise ValueError("campo 'aula': atteso testo non vuoto senza spazi agli estremi")

    def sposta(self, giorno, ora, aula):
        """Aggiorna i tre campi interamente oppure non li tocca."""
        self._valida(giorno, ora, aula)
        self._giorno = giorno
        self._ora = ora
        self._aula = aula
        return None

    def dati(self):
        return (self._giorno, self._ora, self._aula)


# --- PY-U14-E03: il contenitore condiviso sulla classe ---------------------


class RegistroVisiteErrato:
    """DELIBERATAMENTE DIFETTOSO (PY-U14-E03): la lista vive sulla classe."""

    visite = []

    def __init__(self, nome):
        self.nome = nome

    def registra(self, visita):
        self.visite.append(visita)
        return None


class RegistroVisite:
    """Versione corretta di PY-U14-E03: ogni istanza crea la propria lista."""

    def __init__(self, nome):
        self.nome = nome
        self.visite = []

    def registra(self, visita):
        self.visite.append(visita)
        return None


# --- PY-U14-E04: __eq__ che guarda solo il codice --------------------------


class BigliettoPerCodice:
    """DELIBERATAMENTE DIFETTOSO (PY-U14-E04): l'uguaglianza guarda un solo campo.

    Due biglietti con lo stesso codice ma fila e posto diversi risultano
    uguali: il contratto di valore dichiarato riguarda tutti i campi.
    """

    def __init__(self, codice, fila, posto):
        self._codice = codice
        self._fila = fila
        self._posto = posto

    def __eq__(self, altro):
        if not isinstance(altro, BigliettoPerCodice):
            return NotImplemented
        return self._codice == altro._codice


class Biglietto:
    """Versione corretta di PY-U14-E04: tutti i campi pertinenti e il tipo."""

    def __init__(self, codice, fila, posto):
        self._codice = codice
        self._fila = fila
        self._posto = posto

    def dati(self):
        return (self._codice, self._fila, self._posto)

    def __eq__(self, altro):
        if not isinstance(altro, Biglietto):
            return NotImplemented
        return self.dati() == altro.dati()


# --- PY-U14-E05: l'annotazione scambiata per validazione -------------------


@dataclass
class PuntoSenzaControlli:
    """DELIBERATAMENTE DIFETTOSO (PY-U14-E05): l'annotazione non è un controllo.

    `x: int` dichiara l'intenzione, ma non rifiuta né il testo né il
    booleano né il valore fuori dominio.
    """

    x: int
    y: int


@dataclass(frozen=True)
class Punto:
    """Versione corretta di PY-U14-E05: controllo scritto e frozen motivato.

    `__post_init__` valida alla costruzione; `frozen=True` impedisce di
    riassegnare i campi, quindi la validazione iniziale resta significativa
    per tutta la durata del valore.
    """

    x: int
    y: int

    def __post_init__(self):
        for valore, nome in ((self.x, "x"), (self.y, "y")):
            if isinstance(valore, bool) or not isinstance(valore, int):
                raise ValueError(
                    f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
                )
            if not 0 <= valore <= 100:
                raise ValueError(f"campo '{nome}': atteso un valore fra 0 e 100, ricevuto {valore}")


# --- PY-U14-T01: proprietà di lettura, scrittura controllata e ampiezza ----


class Finestra:
    """PY-U14-T01: come i `Limiti` del capitolo, in un dominio proprio."""

    def __init__(self, inizio, fine):
        self.imposta(inizio, fine)

    @property
    def inizio(self):
        return self._inizio

    @inizio.setter
    def inizio(self, valore):
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise ValueError(f"campo 'inizio': atteso un intero, ricevuto {type(valore).__name__}")
        if valore > self._fine:
            raise ValueError(f"campo 'inizio': {valore} supera la fine corrente {self._fine}")
        self._inizio = valore

    @property
    def fine(self):
        return self._fine

    @fine.setter
    def fine(self, valore):
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise ValueError(f"campo 'fine': atteso un intero, ricevuto {type(valore).__name__}")
        if valore < self._inizio:
            raise ValueError(f"campo 'fine': {valore} è sotto l'inizio corrente {self._inizio}")
        self._fine = valore

    @property
    def ampiezza(self):
        """Derivata: non esiste alcun campo `_ampiezza`."""
        return self._fine - self._inizio

    def imposta(self, inizio, fine):
        if isinstance(inizio, bool) or not isinstance(inizio, int):
            raise ValueError(f"campo 'inizio': atteso un intero, ricevuto {type(inizio).__name__}")
        if isinstance(fine, bool) or not isinstance(fine, int):
            raise ValueError(f"campo 'fine': atteso un intero, ricevuto {type(fine).__name__}")
        if inizio > fine:
            raise ValueError(f"atteso inizio <= fine, ricevuti ({inizio}, {fine})")
        self._inizio = inizio
        self._fine = fine
        return None


# --- PY-U14-T02: aggiornamento atomico della coppia ------------------------


class Segmento:
    """PY-U14-T02: `sposta` sostituisce la coppia interamente o non la tocca."""

    def __init__(self, inizio, fine):
        self.imposta(inizio, fine)

    def imposta(self, inizio, fine):
        for valore, nome in ((inizio, "inizio"), (fine, "fine")):
            if isinstance(valore, bool) or not isinstance(valore, int):
                raise ValueError(
                    f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
                )
        if inizio > fine:
            raise ValueError(f"atteso inizio <= fine, ricevuti ({inizio}, {fine})")
        self._inizio = inizio
        self._fine = fine
        return None

    def dati(self):
        return (self._inizio, self._fine)


# --- PY-U14-T03: factory, validatore statico e funzione di modulo ----------


def secondi_validi_modulo(secondi):
    """PY-U14-T03: funzione esterna, identica al metodo statico."""
    return isinstance(secondi, int) and not isinstance(secondi, bool) and secondi >= 0


@dataclass(frozen=True)
class DurataT3:
    """PY-U14-T03: durata con factory da ore e minuti e validatore statico."""

    secondi: int

    def __post_init__(self):
        if not secondi_validi_modulo(self.secondi):
            raise ValueError(
                f"campo 'secondi': intero non negativo atteso, ricevuto {self.secondi!r}"
            )

    @classmethod
    def da_minuti(cls, minuti):
        if isinstance(minuti, bool) or not isinstance(minuti, int) or minuti < 0:
            raise ValueError(f"campo 'minuti': intero non negativo atteso, ricevuto {minuti!r}")
        return cls(minuti * 60)

    @staticmethod
    def secondi_validi(secondi):
        """Regola del tipo, senza istanza né classe: per questo sta qui."""
        return secondi_validi_modulo(secondi)


# --- PY-U14-T04: str e repr con unità dichiarate ---------------------------


class Peso:
    """PY-U14-T04: str per chi legge, repr per la diagnostica."""

    def __init__(self, codice, grammi):
        if not isinstance(codice, str) or codice == "" or codice != codice.strip():
            raise ValueError("campo 'codice': testo non vuoto senza spazi agli estremi")
        if isinstance(grammi, bool) or not isinstance(grammi, int) or grammi < 0:
            raise ValueError(f"campo 'grammi': intero non negativo atteso, ricevuto {grammi!r}")
        self._codice = codice
        self._grammi = grammi

    def __str__(self):
        return f"{self._codice}: {self._grammi} g"

    def __repr__(self):
        return f"Peso(codice={self._codice!r}, grammi={self._grammi})"


# --- PY-U14-T05: da classe di valore a dataclass ---------------------------


@dataclass(frozen=True)
class PesoDataclass:
    """PY-U14-T05: stesso contratto di `Peso`, con eq e repr generati."""

    codice: str
    grammi: int

    def __post_init__(self):
        if (
            not isinstance(self.codice, str)
            or self.codice == ""
            or self.codice != self.codice.strip()
        ):
            raise ValueError("campo 'codice': testo non vuoto senza spazi agli estremi")
        if isinstance(self.grammi, bool) or not isinstance(self.grammi, int) or self.grammi < 0:
            raise ValueError(
                f"campo 'grammi': intero non negativo atteso, ricevuto {self.grammi!r}"
            )


# --- PY-U14-T06: dataclass con contenitore per istanza ---------------------


@dataclass
class Squadra:
    """PY-U14-T06: `field(default_factory=list)` costruisce una lista per istanza."""

    nome: str
    componenti: list = field(default_factory=list)


# --- PY-U14-T07: eccezione di dominio e gestione nel chiamante -------------


class SaldoInsufficiente(Exception):
    """PY-U14-T07: richiesta valida ma impossibile per lo stato."""


def preleva(saldo, importo):
    """PY-U14-T07: sottrae se il saldo basta; niente `print`, niente mutazioni oscure."""
    for valore, nome in ((saldo, "saldo"), (importo, "importo")):
        if isinstance(valore, bool) or not isinstance(valore, int) or valore < 0:
            raise ValueError(f"campo '{nome}': intero non negativo atteso, ricevuto {valore!r}")
    if importo > saldo:
        raise SaldoInsufficiente(f"richiesti {importo} centesimi, saldo {saldo}")
    return saldo - importo


def chiama_prelievo(saldo, importo):
    """PY-U14-T07: il chiamante presenta l'esito; il saldo resta sui rifiuti."""
    try:
        saldo = preleva(saldo, importo)
    except SaldoInsufficiente as errore:
        return (saldo, f"prelievo rifiutato: {errore}")
    return (saldo, "prelievo riuscito")


# --- PY-U14-T08: conversioni CSV dell'Articolo con proprietà ---------------


def round_trip_articolo(articolo):
    """PY-U14-T08: proietta in riga CSV, ricostruisce e confronta i dati.

    Restituisce `(riga, dati_ricostruiti)`: la riga è quella dello schema
    storico, i dati ricostruiti sono equivalenti per valore ma sono una
    nuova istanza di `DatiArticolo`, non l'articolo di partenza.
    """
    riga = dati_a_riga(articolo.dati())
    dati = riga_a_dati(riga, "round-trip")
    return (riga, DatiArticolo(*dati))


# --- PY-U14-X01: mutabile validato contro frozen, con contenuto mutabile ---


@dataclass
class Accumulatori:
    """PY-U14-X01: dataclass mutabile con lista: la validazione è solo iniziale."""

    valore: int = 0
    note: list = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.valore, bool) or not isinstance(self.valore, int) or self.valore < 0:
            raise ValueError(
                f"campo 'valore': intero non negativo atteso, ricevuto {self.valore!r}"
            )


@dataclass(frozen=True)
class SquadraFrozen:
    """PY-U14-X01: frozen **con** lista interna: gli assegnamenti sono bloccati,
    le mutazioni dei contenuti no."""

    nome: str
    componenti: list = field(default_factory=list)


# --- PY-U14-X02: mutare l'articolo o sostituire nel registro ---------------


def confronto_aggiornamento():
    """PY-U14-X02: restituisce le osservazioni dei due contratti di aggiornamento.

    L'`Articolo` mutabile viene aggiornato **sul posto**: l'alias dell'istanza
    osserva il cambiamento. La `Prenotazione` frozen viene **sostituita**
    nel registro: l'alias del valore precedente conserva il valore
    precedente. Le proiezioni finali del registro riflettono il nuovo stato.
    """
    articolo = ArticoloProprieta("007", "Vite, lunga", 4, 25)
    alias_articolo = articolo
    articolo.aggiorna("Vite, lunga", 6, 25)
    osservazione_articolo = alias_articolo.quantita == 6

    registro = registro_per_confronto()
    alias_prenotazione = registro.cerca("PR-01")
    registro.modifica("PR-01", "Lab A", Intervallo(600, 660), 20)
    osservazione_prenotazione = alias_prenotazione.intervallo.inizio_min == 540
    nuova = registro.cerca("PR-01")
    proiezione_aggiornata = nuova.intervallo.inizio_min == 600

    return {
        "alias_articolo_segue_la_mutazione": osservazione_articolo,
        "alias_prenotazione_conserva_il_valore": osservazione_prenotazione,
        "registro_punta_al_nuovo_valore": proiezione_aggiornata,
    }


def registro_per_confronto():
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    return registro


# --- PY-U14-X03: tre snapshot con politiche diverse ------------------------


def tre_snapshot(registro):
    """PY-U14-X03: lista interna (qui simulata), copia superficiale, nuovi record.

    Restituisce `(lista_riferimenti, copia_superficiale, record_primitivi)`:
    la prima espone gli **elementi** del registro (mutarli cambia lo stato
    quando sono mutabili), la seconda condivide gli elementi ma ha un
    contenitore proprio, la terza non tocca il registro in alcun modo.
    """
    valori = list(registro.prenotazioni())
    copia_superficiale = list(valori)
    record_primitivi = [dict(record) for record in registro.riepilogo()["prenotazioni"]]
    return (valori, copia_superficiale, record_primitivi)


# --- PY-U14-X04: controllore con memoria delle decisioni -------------------


class ControlloreConMemoria:
    """PY-U14-X04: stesso modello del controllore, con cronologia delle decisioni.

    Riceve sensore e attuatore già costruiti e registra, per ogni passo
    riuscito, la coppia `(lettura, azione)`. Nessun GPIO, nessuna attesa:
    la cronologia è deterministica quanto la sequenza del sensore.
    """

    def __init__(self, sensore, attuatore, soglia):
        if isinstance(soglia, bool) or not isinstance(soglia, (int, float)):
            raise ValueError(f"soglia: atteso un numero, ricevuto {type(soglia).__name__}")
        self._sensore = sensore
        self._attuatore = attuatore
        self._soglia = soglia
        self._cronologia = []

    def cronologia(self):
        """Copia della cronologia: modificarla non tocca il controllore."""
        return list(self._cronologia)

    def passo(self):
        lettura = self._sensore.leggi()
        if lettura < self._soglia:
            self._attuatore.accendi()
            azione = "acceso"
        else:
            self._attuatore.spegni()
            azione = "spento"
        self._cronologia.append((lettura, azione))
        return None


if __name__ == "__main__":
    # Dimostrazione compatta: un controllo per ogni soluzione principale.
    limite = LimitiCorretto(0, 10)
    limite.minimo = 5
    print("E01:", (limite.minimo, limite.massimo))

    attivita = Attivita(1, 8, "Lab A")
    try:
        attivita.sposta(2, 9, "")
    except ValueError as errore:
        print("E02:", errore, "->", attivita.dati())

    biglietto_a = Biglietto("B01", "A", 12)
    biglietto_b = Biglietto("B01", "A", 12)
    biglietto_c = Biglietto("B01", "B", 12)
    print("E04:", biglietto_a == biglietto_b, biglietto_a == biglietto_c)

    difettoso = PuntoSenzaControlli("otto", 10)
    print("E05 (annotazione senza controllo): la costruzione è riuscita comunque ->", difettoso.x)
    try:
        Punto("otto", 10)
    except ValueError as errore:
        print("E05:", errore)

    finestra = Finestra(0, 10)
    print("T01:", finestra.ampiezza)
    try:
        finestra.inizio = 20
    except ValueError as errore:
        print("T01 rifiuto:", errore)

    print("T03:", DurataT3.da_minuti(3).secondi, DurataT3.secondi_validi(-1))
    peso = Peso("007", 0)
    print("T04:", str(peso), "|", repr(peso))
    print("T05:", PesoDataclass("007", 12) == PesoDataclass("007", 12))
    squadra_a = Squadra("alfa")
    squadra_b = Squadra("beta")
    squadra_a.componenti.append("G01")
    print("T06:", len(squadra_a.componenti), len(squadra_b.componenti))
    print("T07:", chiama_prelievo(500, 600))
    articolo = ArticoloProprieta("007", "Vite, lunga", 4, 25)
    riga, dati = round_trip_articolo(articolo)
    print("T08:", riga, "|", dati == articolo.dati(), dati is articolo.dati())
    print("X02:", confronto_aggiornamento())
