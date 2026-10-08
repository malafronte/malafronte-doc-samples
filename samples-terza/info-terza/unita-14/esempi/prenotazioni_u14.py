"""Prenotazioni di aule: valori, registro ed eccezioni di dominio (OOP-04, sez. E).

Questo modulo realizza il modello introdotto concettualmente in OOP-01, sez.
E: i cinque dati di quella scheda — `codice`, `aula`, `inizio`, `fine`,
`partecipanti` — trovano qui la loro rappresentazione. Inizio e fine non
sono due campi piatti: si raccolgono nel valore composito `Intervallo`
(frozen, semiaperto, validato alla costruzione in `intervalli_u14`).

Le responsabilità sono separate:

- **`Prenotazione`** — dataclass frozen: valida i propri dati, offre il
  confronto `sovrapposta_a` che combina aula e intervallo e la stringa di
  riepilogo `testo_riepilogo`, senza stampare;
- **`RegistroPrenotazioni`** — la raccolta: crea il proprio contenitore,
  mantiene codici univoci sull'intero registro e nessun conflitto nella
  stessa aula, ed espone registra, registrazione a lotto, ricerca,
  annullamento, modifica e riepilogo.

Contratto della `Prenotazione`:

| Campo | Regola |
|---|---|
| `codice` | testo non vuoto, senza spazi agli estremi, confronto esatto |
| `aula` | testo non vuoto, senza spazi agli estremi, confronto esatto |
| `intervallo` | un `Intervallo` valido |
| `partecipanti` | intero non booleano positivo |

Contratto del registro — ordine dei controlli: validazione dei dati
candidati; presenza/unicità del codice; conflitto; scrittura finale. Ogni
rifiuto lascia l'elenco esattamente com'era. Il duplicato è segnalato prima
del conflitto quando più cause coesistono.

- `registra(prenotazione)` — `None` sul successo; duplicato →
  `CodiceDuplicato`; conflitto → `ConflittoPrenotazione`; candidato non
  `Prenotazione` → `ValueError`;
- `registra_lotto(prenotazioni)` — `None` se tutto il lotto è accettabile;
  al primo rifiuto l'eccezione pertinente e **nessuna** modifica; il
  registro mantiene la propria identità;
- `cerca(codice)` — la `Prenotazione` oppure `None`; codice malformato →
  `ValueError`;
- `annulla(codice)` — `True` se rimosso, `False` se assente; codice
  malformato → `ValueError`;
- `modifica(codice, aula, intervallo, partecipanti)` — `True` se
  sostituito, `False` se il codice valido è assente; dati invalidi →
  `ValueError`; conflitto → `ConflittoPrenotazione`;
- `prenotazioni()` — tupla dei valori nell'ordine di registrazione; il
  contenitore non è modificabile con `append`/`remove`;
- `riepilogo()` — nuovo dizionario con `numero_prenotazioni`,
  `durata_totale_min`, `partecipanti_totali` e `prenotazioni` (nuova lista
  di nuovi record primitivi).

Nella `modifica` il confronto esclude la prenotazione che si sostituisce:
una richiesta identica all'attuale non è un conflitto con se stessa. La
sostituzione crea un **nuovo** valore frozen: gli alias della prenotazione
precedente conservano il valore precedente, il registro punta al nuovo.

`durata_totale_min` somma le occupazioni delle aule, non la durata
dell'unione temporale della giornata; `partecipanti_totali` somma le
partecipazioni delle richieste, non persone distinte.

Scelta degli algoritmi: la lista rende visibile la scansione e conserva
l'ordine di registrazione. Ricerca, verifica di duplicato e controllo di
una richiesta costano O(n) sul numero di prenotazioni; il riepilogo è O(n).
Non esistono indici o cache aggiuntive: nessun requisito li chiede e
dovrebbero mantenere invarianti propri.

Ambiente: CPython sul computer. Dipende soltanto da `Intervallo`.
"""

from dataclasses import dataclass

from intervalli_u14 import Intervallo


class CodiceDuplicato(Exception):
    """Registrazione rifiutata: il codice esiste già nel registro."""


class ConflittoPrenotazione(Exception):
    """Registrazione rifiutata: l'aula è già occupata in quei minuti."""


def _valida_testo(valore, nome):
    """Controlla un campo testuale: non vuoto, senza spazi agli estremi."""
    if not isinstance(valore, str):
        raise ValueError(f"campo '{nome}': atteso testo, ricevuto {type(valore).__name__}")
    if valore == "":
        raise ValueError(f"campo '{nome}': non può essere vuoto")
    if valore != valore.strip():
        raise ValueError(
            f"campo '{nome}': spazi iniziali o finali non ammessi, ricevuto {valore!r}"
        )
    return None


def _valida_partecipanti(valore):
    """Controlla i partecipanti: intero non booleano positivo."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(
            f"campo 'partecipanti': atteso un intero, ricevuto {type(valore).__name__}"
        )
    if valore <= 0:
        raise ValueError(f"campo 'partecipanti': atteso un valore positivo, ricevuto {valore}")
    return None


@dataclass(frozen=True)
class Prenotazione:
    """Una richiesta di aula: valore frozen con validazione alla costruzione.

    L'invariante individuale è fissato alla costruzione e non può cambiare:
    per aggiornare una prenotazione il registro costruisce un **nuovo**
    candidato e, solo dopo i controlli, sostituisce il vecchio.
    """

    codice: str
    aula: str
    intervallo: Intervallo
    partecipanti: int

    def __post_init__(self):
        _valida_testo(self.codice, "codice")
        _valida_testo(self.aula, "aula")
        if not isinstance(self.intervallo, Intervallo):
            raise ValueError(
                "campo 'intervallo': atteso un Intervallo, "
                f"ricevuto {type(self.intervallo).__name__}"
            )
        _valida_partecipanti(self.partecipanti)

    def sovrapposta_a(self, altra):
        """`True` se le due prenotazioni occupano la stessa aula in minuti comuni.

        Combina il confronto dell'aula, esatto, con il confronto degli
        intervalli delegato a `Intervallo.sovrapposto_a`: il registro non
        ispeziona i minuti. Il confronto è simmetrico.
        """
        return self.aula == altra.aula and self.intervallo.sovrapposto_a(altra.intervallo)

    def testo_riepilogo(self):
        """Restituisce una riga di riepilogo in minuti. Non stampa.

        La formattazione `HH:MM` appartiene al confine di acquisizione e
        presentazione (CLI), non al dominio: qui i minuti restano minuti.
        """
        return (
            f"{self.codice}, aula {self.aula}, "
            f"{self.intervallo.inizio_min}-{self.intervallo.fine_min}, "
            f"{self.partecipanti} partecipanti"
        )


class RegistroPrenotazioni:
    """Raccolta di prenotazioni con regole dell'insieme.

    Invarianti della raccolta: ogni elemento è una `Prenotazione` valida, i
    codici sono univoci nell'intero registro e nessuna coppia occupa la
    stessa aula in minuti comuni. Ogni istanza crea il **proprio**
    contenitore: due registri non condividono nulla.
    """

    def __init__(self):
        self._prenotazioni = []

    def _indice_di(self, codice):
        """Indice della prenotazione con quel codice, oppure `None`."""
        for indice, prenotazione in enumerate(self._prenotazioni):
            if prenotazione.codice == codice:
                return indice
        return None

    def _conflitto(self, candidato, escludi_indice):
        """Restituisce la prenotazione in conflitto con `candidato`, o `None`.

        `escludi_indice` esclude dal confronto la prenotazione che sta per
        essere sostituita: una modifica identica all'attuale non è un
        conflitto con se stessa.
        """
        for indice, presente in enumerate(self._prenotazioni):
            if indice != escludi_indice and candidato.sovrapposta_a(presente):
                return presente
        return None

    def registra(self, prenotazione):
        """Aggiunge una prenotazione dopo i controlli. `None` sul successo.

        Un candidato che non è una `Prenotazione` solleva `ValueError`; un
        codice già presente solleva `CodiceDuplicato`; l'occupazione di
        minuti già presi nella stessa aula solleva `ConflittoPrenotazione`.
        Ogni rifiuto lascia l'elenco invariato.
        """
        if not isinstance(prenotazione, Prenotazione):
            raise ValueError(
                f"candidato: attesa una Prenotazione, ricevuto {type(prenotazione).__name__}"
            )
        if self._indice_di(prenotazione.codice) is not None:
            raise CodiceDuplicato(f"il codice {prenotazione.codice!r} è già registrato")
        in_conflitto = self._conflitto(prenotazione, escludi_indice=-1)
        if in_conflitto is not None:
            raise ConflittoPrenotazione(
                f"{prenotazione.codice!r} si sovrappone a {in_conflitto.codice!r} "
                f"in aula {prenotazione.aula}"
            )
        self._prenotazioni.append(prenotazione)
        return None

    def registra_lotto(self, prenotazioni):
        """Applica un lotto per intero oppure non applica nulla.

        Costruisce un registro candidato con i valori correnti e gli
        sottopone le nuove prenotazioni con `registra`: al primo rifiuto
        l'eccezione pertinente sale al chiamante e questo registro resta
        intatto. Al successo completo la raccolta interna viene sostituita:
        il registro ricevente **mantiene la propria identità**, quindi menu
        e importazione che lo usano continuano a osservare lo stesso stato.
        """
        candidato = RegistroPrenotazioni()
        for presente in self._prenotazioni:
            candidato.registra(presente)
        for nuova in prenotazioni:
            candidato.registra(nuova)
        self._prenotazioni = candidato._prenotazioni
        return None

    def cerca(self, codice):
        """Restituisce la prenotazione con quel codice, oppure `None`."""
        _valida_testo(codice, "codice")
        indice = self._indice_di(codice)
        if indice is None:
            return None
        return self._prenotazioni[indice]

    def annulla(self, codice):
        """Rimuove la prenotazione con quel codice.

        `True` se rimossa, `False` se assente: l'assenza è un esito ordinario
        di questa operazione, distinto dal codice malformato (`ValueError`).
        """
        _valida_testo(codice, "codice")
        indice = self._indice_di(codice)
        if indice is None:
            return False
        del self._prenotazioni[indice]
        return True

    def modifica(self, codice, aula, intervallo, partecipanti):
        """Sostituisce i dati di una prenotazione, con codice stabile.

        Prima si valida il candidato completo (`ValueError` su dati
        invalidi, anche quando il codice è assente), poi si cerca il codice
        (`False` se assente), poi il conflitto escludendo la prenotazione
        sostituita, infine si scrive. L'alias del valore precedente conserva
        il valore precedente: la sostituzione non muta i frozen.
        """
        _valida_testo(codice, "codice")
        candidato = Prenotazione(codice, aula, intervallo, partecipanti)
        indice = self._indice_di(codice)
        if indice is None:
            return False
        in_conflitto = self._conflitto(candidato, escludi_indice=indice)
        if in_conflitto is not None:
            raise ConflittoPrenotazione(
                f"{codice!r} si sovrappone a {in_conflitto.codice!r} in aula {candidato.aula}"
            )
        self._prenotazioni[indice] = candidato
        return True

    def prenotazioni(self):
        """Tupla dei valori frozen, nell'ordine di registrazione.

        La tupla impedisce `append` e `remove` sul contenitore restituito;
        gli elementi sono già valori frozen. Non è una promessa di
        immutabilità profonda generica: i campi primitivi non sono
        modificabili, e questo è tutto ciò che il contratto dichiara.
        """
        return tuple(self._prenotazioni)

    def riepilogo(self):
        """Nuovo dizionario con i totali e una nuova lista di nuovi record.

        `durata_totale_min` somma le occupazioni delle aule;
        `partecipanti_totali` somma le partecipazioni delle richieste. La
        lista `prenotazioni` contiene **nuovi** dizionari con campi
        primitivi: modificarli non tocca il registro.
        """
        durata_totale_min = 0
        partecipanti_totali = 0
        righe = []
        for prenotazione in self._prenotazioni:
            durata_totale_min = durata_totale_min + prenotazione.intervallo.durata_min
            partecipanti_totali = partecipanti_totali + prenotazione.partecipanti
            righe.append(
                {
                    "codice": prenotazione.codice,
                    "aula": prenotazione.aula,
                    "inizio_min": prenotazione.intervallo.inizio_min,
                    "fine_min": prenotazione.intervallo.fine_min,
                    "partecipanti": prenotazione.partecipanti,
                }
            )
        return {
            "numero_prenotazioni": len(self._prenotazioni),
            "durata_totale_min": durata_totale_min,
            "partecipanti_totali": partecipanti_totali,
            "prenotazioni": righe,
        }


if __name__ == "__main__":
    registro = RegistroPrenotazioni()
    print("vuoto:", registro.riepilogo())

    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    registro.registra(Prenotazione("PR-02", "Lab A", Intervallo(600, 660), 18))
    try:
        registro.registra(Prenotazione("PR-03", "Lab A", Intervallo(570, 630), 15))
    except ConflittoPrenotazione as errore:
        print("PR-03 rifiutata:", errore)
    registro.registra(Prenotazione("PR-04", "Lab B", Intervallo(570, 630), 12))

    totale = registro.riepilogo()
    print(
        "atteso 3 prenotazioni, 180 minuti, 50 partecipazioni:",
        totale["numero_prenotazioni"],
        totale["durata_totale_min"],
        totale["partecipanti_totali"],
    )

    try:
        registro.registra(Prenotazione("PR-01", "Lab C", Intervallo(540, 600), 9))
    except CodiceDuplicato as errore:
        print("duplicato prima del conflitto:", errore)

    print("cerca PR-02:", registro.cerca("PR-02").testo_riepilogo())
    print("cerca PR-99:", registro.cerca("PR-99"))
    print("annulla PR-99:", registro.annulla("PR-99"))

    try:
        registro.modifica("PR-02", "Lab A", Intervallo(585, 645), 18)
    except ConflittoPrenotazione as errore:
        print("modifica in conflitto:", errore)
    print("dopo il rifiuto, PR-02:", registro.cerca("PR-02").testo_riepilogo())

    print(
        "modifica identica:",
        registro.modifica("PR-02", "Lab A", Intervallo(600, 660), 18),
    )

    vecchia = registro.cerca("PR-02")
    print("sposta PR-02 alle 11:", registro.modifica("PR-02", "Lab A", Intervallo(660, 720), 18))
    print("alias precedente:", vecchia.testo_riepilogo())
    print("nuovo valore:", registro.cerca("PR-02").testo_riepilogo())

    snapshot = registro.riepilogo()
    snapshot["prenotazioni"][0]["aula"] = "manomessa"
    print("snapshot modificato, registro intatto:", registro.riepilogo()["prenotazioni"][0]["aula"])

    try:
        registro.prenotazioni().append(Prenotazione("PR-09", "Lab C", Intervallo(0, 60), 5))
    except AttributeError as errore:
        print("tupla non modificabile:", errore)

    altro = RegistroPrenotazioni()
    altro.registra(Prenotazione("PX-01", "Lab A", Intervallo(0, 60), 5))
    lotto = [
        Prenotazione("PR-05", "Lab A", Intervallo(660, 720), 10),
        Prenotazione("PR-06", "Lab A", Intervallo(690, 750), 10),
    ]
    try:
        registro.registra_lotto(lotto)
    except ConflittoPrenotazione as errore:
        print("lotto rifiutato per intero:", errore)
    print("dopo il lotto rifiutato:", registro.riepilogo()["numero_prenotazioni"])

    lotto_valido = [
        Prenotazione("PR-05", "Lab A", Intervallo(720, 780), 10),
        Prenotazione("PR-06", "Lab B", Intervallo(690, 750), 10),
    ]
    registro.registra_lotto(lotto_valido)
    print("dopo il lotto valido:", registro.riepilogo()["numero_prenotazioni"])
    altro_totale = altro.riepilogo()["numero_prenotazioni"]
    print("l'altro registro resta indipendente:", altro_totale)
