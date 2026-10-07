"""Soluzioni eseguibili della famiglia algoritmica U13 — Oggetti, stato e invarianti.

Raccoglie il codice dei problemi che richiedono una realizzazione completa:
PY-U13-T07 (`Deposito`), PY-U13-T08 (`Risorsa`), PY-U13-T09 (`elabora`),
PY-U13-T10 (`elabora_movimenti`), PY-U13-T11 (`Statistiche`), PY-U13-T12
(`riepilogo_inventario` e `da_riordinare`), PY-U13-X04 (`trasferisci`) e
PY-U13-X05 (`confronta`).

Ogni sezione è autonoma e dichiara il proprio contratto. Ambiente: CPython
sul computer; dipende soltanto dal linguaggio, eccetto dove indicato.
"""


def _valida_intero(valore, nome, minimo):
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < minimo:
        raise ValueError(f"{nome}: atteso un valore >= {minimo}, ricevuto {valore}")


def _valida_identificatore(identificatore):
    if not isinstance(identificatore, str) or identificatore.strip() == "":
        raise ValueError("identificatore: atteso testo non vuoto")


# --- PY-U13-T07: Deposito con capacità ------------------------------------


class Deposito:
    """Unità contenute in un deposito a capacità fissata.

    Invariante: `0 <= contenuto <= capacita`. Il contenuto è conservato, lo
    spazio libero è derivato.
    """

    def __init__(self, capacita, contenuto=0):
        _valida_intero(capacita, "capacita", 0)
        _valida_intero(contenuto, "contenuto", 0)
        if contenuto > capacita:
            raise ValueError(f"contenuto: {contenuto} supera la capacita {capacita}")
        self._capacita = capacita
        self._contenuto = contenuto

    def carica(self, unita):
        _valida_intero(unita, "unita", 0)
        if self._contenuto + unita > self._capacita:
            return False
        self._contenuto = self._contenuto + unita
        return True

    def preleva(self, unita):
        _valida_intero(unita, "unita", 0)
        if unita > self._contenuto:
            return False
        self._contenuto = self._contenuto - unita
        return True

    def spazio_libero(self):
        return self._capacita - self._contenuto

    def stato(self):
        return {"capacita": self._capacita, "contenuto": self._contenuto}


# --- PY-U13-T08: Prenotazioni di unità disponibili -------------------------


class Risorsa:
    """Unità disponibili con prenotazioni identificate.

    Invariante: `occupato + disponibile == capacita`, con nessuno dei due
    valori negativo. `disponibile` è derivato, non conservato.
    """

    def __init__(self, capacita):
        _valida_intero(capacita, "capacita", 0)
        self._capacita = capacita
        self._occupato = 0
        self._prenotazioni = {}

    def prenota(self, identificatore, quantita):
        _valida_identificatore(identificatore)
        _valida_intero(quantita, "quantita", 1)
        if identificatore in self._prenotazioni:
            return "duplicato"
        if quantita > self._capacita - self._occupato:
            return "indisponibile"
        self._prenotazioni[identificatore] = quantita
        self._occupato = self._occupato + quantita
        return "accettata"

    def annulla(self, identificatore):
        _valida_identificatore(identificatore)
        if identificatore not in self._prenotazioni:
            return "assente"
        self._occupato = self._occupato - self._prenotazioni.pop(identificatore)
        return "accettata"

    def disponibile(self):
        return self._capacita - self._occupato

    def stato(self):
        return {
            "capacita": self._capacita,
            "occupato": self._occupato,
            "disponibile": self.disponibile(),
        }


# --- PY-U13-T09: sequenza di richieste ------------------------------------


def elabora(risorsa, richieste):
    """Applica le richieste nell'ordine e restituisce il riepilogo.

    Politica sequenziale: ogni richiesta è valutata sullo stato prodotto dalle
    precedenti. I rifiuti sono locali e non interrompono la sequenza. Ogni
    richiesta è una coppia `(identificatore, quantita)` — prenotazione — oppure
    una tupla `(identificatore,)` — annullamento.
    """
    esiti = []
    accettate = 0
    rifiutate = 0
    for richiesta in richieste:
        if len(richiesta) == 2:
            identificatore, quantita = richiesta
            esito = risorsa.prenota(identificatore, quantita)
        elif len(richiesta) == 1:
            (identificatore,) = richiesta
            esito = risorsa.annulla(identificatore)
        else:
            raise ValueError(
                f"richiesta: attesa una coppia (identificatore, quantita) "
                f"o una tupla (identificatore,), ricevuta {richiesta!r}"
            )
        if esito == "accettata":
            accettate = accettate + 1
        else:
            rifiutate = rifiutate + 1
        esiti.append((richiesta, esito))
    return {
        "ricevute": len(richieste),
        "accettate": accettate,
        "rifiutate": rifiutate,
        "esiti": esiti,
        "stato_finale": risorsa.stato(),
    }


# --- PY-U13-T10: inventario e movimenti -----------------------------------


def cerca(inventario, codice):
    """Indice dell'articolo con questo codice, oppure `None`. L'indice 0 è valido."""
    for indice, articolo in enumerate(inventario):
        if articolo["codice"] == codice:
            return indice
    return None


def elabora_movimenti(inventario, movimenti):
    """Applica movimenti firmati a una copia dell'inventario.

    Errore di formato e rifiuto per indisponibilità sono distinti. I dati
    ricevuti non vengono modificati. Il risultato comprende il riepilogo per
    articolo — coppie `(codice, quantita)` ordinate per codice — e il totale
    complessivo delle quantità.
    """
    lavoro = [dict(articolo) for articolo in inventario]
    esiti = []
    for codice, variazione in movimenti:
        indice = cerca(lavoro, codice)
        if indice is None:
            esiti.append((codice, variazione, "errore: codice assente"))
            continue
        if isinstance(variazione, bool) or not isinstance(variazione, int):
            esiti.append((codice, variazione, "errore: variazione non intera"))
            continue
        nuovo = lavoro[indice]["quantita"] + variazione
        if nuovo < 0:
            esiti.append((codice, variazione, "rifiuto: disponibilità insufficiente"))
            continue
        lavoro[indice]["quantita"] = nuovo
        esiti.append((codice, variazione, "accettato"))
    per_articolo = []
    totale_quantita = 0
    for articolo in lavoro:
        per_articolo.append((articolo["codice"], articolo["quantita"]))
        totale_quantita = totale_quantita + articolo["quantita"]
    riepilogo = sorted(per_articolo)
    return {
        "articoli": lavoro,
        "esiti": esiti,
        "riepilogo": riepilogo,
        "totale_quantita": totale_quantita,
    }


# --- PY-U13-T11: statistiche incrementali ---------------------------------


class Statistiche:
    """Numero, media ed estremi di una sequenza senza conservarla.

    Stato minimo: conteggio, somma, minimo, massimo. Prima di qualunque misura
    numero è 0 e media, minimo e massimo sono `None`: non disponibili.
    """

    def __init__(self):
        self._conteggio = 0
        self._somma = 0
        self._minimo = None
        self._massimo = None

    def acquisisci(self, misura):
        if isinstance(misura, bool) or not isinstance(misura, int):
            raise ValueError(f"misura: atteso un intero, ricevuto {type(misura).__name__}")
        self._somma = self._somma + misura
        self._conteggio = self._conteggio + 1
        if self._minimo is None or misura < self._minimo:
            self._minimo = misura
        if self._massimo is None or misura > self._massimo:
            self._massimo = misura
        return None

    def risultati(self):
        return {
            "numero": self._conteggio,
            "media": None if self._conteggio == 0 else self._somma / self._conteggio,
            "minimo": self._minimo,
            "massimo": self._massimo,
        }


# --- PY-U13-T12: riepilogo e soglia di riordino ---------------------------


def riepilogo_inventario(articoli):
    """Riepilogo in una sola scansione. Parità del massimo: primo incontrato.

    Precondizione: gli elementi hanno `codice`, `quantita` e `valore_centesimi()`.
    """
    numero = 0
    quantita_totale = 0
    valore_totale = 0
    codice_massimo = None
    valore_massimo = -1
    for articolo in articoli:
        dati = articolo.dati()
        numero = numero + 1
        quantita_totale = quantita_totale + dati["quantita"]
        valore = articolo.valore_centesimi()
        valore_totale = valore_totale + valore
        if valore > valore_massimo:
            valore_massimo = valore
            codice_massimo = dati["codice"]
    return {
        "articoli": numero,
        "quantita_totale": quantita_totale,
        "valore_centesimi": valore_totale,
        "codice_maggiore_valore": codice_massimo,
    }


def da_riordinare(articoli, soglia):
    """Proiezioni degli articoli con quantità minore o uguale alla soglia.

    L'ordine è quello originale; nessun ordinamento viene applicato.
    """
    _valida_intero(soglia, "soglia", 0)
    selezionati = []
    for articolo in articoli:
        dati = articolo.dati()
        if dati["quantita"] <= soglia:
            selezionati.append(dati)
    return selezionati


# --- PY-U13-X04: trasferimento fra due depositi ---------------------------


def trasferisci(sorgente, destinazione, unita):
    """Trasferisce unità da un deposito all'altro. `True` se applicato.

    Tutte le condizioni sono controllate prima di ogni modifica. L'argomento è
    validato per primo, anche quando i due depositi coincidono: un argomento non
    ammesso è un errore in ogni situazione. Sorgente e destinazione coincidenti
    sono invece rifiutate: il contratto parla di due entità.
    """
    _valida_intero(unita, "unita", 0)
    if sorgente is destinazione:
        return False
    if unita > sorgente.stato()["contenuto"]:
        return False
    if unita > destinazione.spazio_libero():
        return False
    sorgente.preleva(unita)
    destinazione.carica(unita)
    return True


# --- PY-U13-X05: confronto per sequenze -----------------------------------


def traccia(sequenza, esegui):
    """Restituisce la lista dei passi, ciascuno con operazione, esito e stato."""
    return [esegui(operazione) for operazione in sequenza]


def confronta(sequenza, esegui_procedurale, esegui_oggetti):
    """Restituisce il primo passo divergente oppure `None`.

    Il confronto usa le proiezioni dei dati, non gli oggetti: le due versioni
    sono di tipi diversi e non condividono né `==` né `is`. Copre fino al passo
    più lungo, così una traccia troncata non risulta equivalente a una completa.
    """
    traccia_a = traccia(sequenza, esegui_procedurale)
    traccia_b = traccia(sequenza, esegui_oggetti)
    passi = max(len(traccia_a), len(traccia_b))
    for posizione in range(passi):
        if posizione < len(traccia_a):
            passo_a = traccia_a[posizione]
        else:
            passo_a = "passo mancante"
        if posizione < len(traccia_b):
            passo_b = traccia_b[posizione]
        else:
            passo_b = "passo mancante"
        if passo_a != passo_b:
            return {"passo": posizione + 1, "procedurale": passo_a, "oggetti": passo_b}
    return None


if __name__ == "__main__":
    deposito = Deposito(5, 0)
    print("T07 carica(3):", deposito.carica(3), deposito.stato())
    risorsa = Risorsa(4)
    print("T08 prenota:", risorsa.prenota("A", 3), risorsa.stato())
    print("T09 elabora:", elabora(risorsa, [("B", 2)])["rifiutate"])
    inventario = [{"codice": "A", "descrizione": "x", "quantita": 5}]
    movimenti = elabora_movimenti(inventario, [("A", -6)])
    print("T10 movimenti:", movimenti["esiti"])
    print("T10 riepilogo:", movimenti["riepilogo"], "totale", movimenti["totale_quantita"])
    statistiche = Statistiche()
    statistiche.acquisisci(2)
    statistiche.acquisisci(8)
    print("T11 risultati:", statistiche.risultati())
    print("T12 vuoto:", riepilogo_inventario([]))
    print("X04 trasferisci:", trasferisci(Deposito(5, 5), Deposito(5, 0), 3))
