"""Indice hash di consultazione per codice del registro dei preventivi (U18).

Responsabilità del modulo: costruire, su una **fotografia** dei preventivi del
registro, un indice di consultazione per codice con ricerca esatta e
rispondere a più interrogazioni sulla stessa fotografia. La struttura è la
tabella hash con concatenamento del capitolo PY-34; il modulo la riproduce
per intero — funzione hash, nodo interno, inserimento in testa,
aggiornamento, rimozione, crescita per raddoppio — perché la fotografia della
raccolta resta autonoma e non importa moduli da fuori della cartella del
progetto.

**Variante dichiarata** rispetto alla tabella del capitolo, che ammette chiavi
di tipo esatto `int` oppure `str`: qui le chiavi sono i **codici stringa** del
registro e l'adattamento comporta quattro precisazioni.

- **Dominio delle chiavi**: stringhe non vuote. La validazione è quella
  **riusata** dal modello del registro: `valida_chiave` richiama
  `valida_dominio_record` sul campo `codice` dello schema, senza duplicare
  regole né diagnosi.
- **Funzione hash**: quella didattica del capitolo, con la variante testuale
  ad accumulatore. I codici conservano gli zeri significativi perché restano
  stringhe: `"007"` e `"7"` sono chiavi diverse.
- **Costo delle operazioni sulle chiavi**: un hash o un confronto fra codici
  costa in proporzione ai testi trattati, mentre nel capitolo il costo
  costante è assunto per interi di dimensione limitata. I conteggi dei
  confronti restano quelli del capitolo: contano le chiavi esaminate nella
  catena, non le operazioni sui caratteri.
- **Dati associati**: i valori `Preventivo` del modello U14, già validati e
  immutabili. La chiave di ogni voce coincide con il campo `codice` del
  record associato.

Contratto dell'indice (`IndiceHashU18`):

- **dati ammessi**: chiavi stringa non vuote e valori `Preventivo` il cui
  campo `codice` coincide con la chiave;
- **risultato**: `cerca` restituisce il record associato; `voci` e
  `fotografia_ordinata` restituiscono liste nuove, la seconda in ordine
  lessicografico crescente dei codici;
- **effetti**: le interrogazioni non modificano l'indice; `inserisci`,
  `aggiorna` e `rimuovi` modificano soltanto l'indice che le riceve;
- **errori**: chiave di tipo diverso da `str` → `TypeError`; stringa vuota →
  `ValueError`; record di tipo diverso da `Preventivo` o con codice diverso
  dalla chiave → `TypeError` oppure `ValueError`; duplicato in `inserisci` →
  `ValueError`; chiave assente in `cerca` e `aggiorna` → `KeyError`;
- **invarianti**: ogni codice compare una sola volta; ogni nodo appartiene al
  bucket `hash_didattico(codice) % m`; `_dimensione` coincide con il numero di
  nodi raggiungibili; ogni voce conserva l'associazione fra chiave e record;
  dopo un inserimento riuscito il carico rispetta la soglia 1.0.

Ciclo di vita dell'indice, dichiarato: la costruzione avviene **dopo il
caricamento** del registro, sulla proiezione pubblica `preventivi()`, e
l'indice così costruito risponde a più interrogazioni sulla stessa
fotografia. Una modifica del registro richiede una **nuova costruzione**
dell'indice: la vecchia fotografia continua a rappresentare i dati
precedenti, perché i valori `Preventivo` sono immutabili e l'indice non
condivide con il registro né contenitori mutabili né aggiornamenti.

L'indice hash soddisfa query esatte; l'indice BST della tappa U17 conserva il
proprio ruolo nelle query ordinate e d'intervallo.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""

from registro_dominio import DESTINAZIONI_AMMESSE, valida_dominio_record
from registro_modello_u14 import Preventivo

#: Soglia di crescita del modello del capitolo, con raddoppio della capacità.
SOGLIA_CARICO = 1.0


def hash_didattico(chiave):
    """Restituisce l'intero hash didattico della chiave stringa.

    L'accumulatore parte da 0 e per ogni carattere applica
    `h = (31 * h + ord(carattere)) % 65521`. Una chiave di tipo diverso da
    `str` solleva `TypeError`.
    """
    if type(chiave) is not str:
        raise TypeError(f"chiave attesa di tipo str, ricevuto {type(chiave).__name__}")
    accumulatore = 0
    for carattere in chiave:
        accumulatore = (31 * accumulatore + ord(carattere)) % 65521
    return accumulatore


def valida_chiave(codice) -> None:
    """Convalida la chiave dell'indice e non restituisce nulla.

    La validazione è quella **riusata** dal modello del registro: il codice
    deve superare il controllo del campo `codice` di `valida_dominio_record`,
    applicato a un record sintetico che lascia gli altri due campi nel dominio
    — la diagnosi pertinente è sempre quella del campo `codice`. Un valore che
    non è una stringa solleva `TypeError`; una stringa vuota solleva
    `ValueError`. Entrambi gli errori precedono ogni effetto e valgono anche
    sull'indice vuoto.
    """
    if not isinstance(codice, str):
        raise TypeError(f"chiave attesa di tipo str, ricevuto {type(codice).__name__}")
    errore = valida_dominio_record(
        {"codice": codice, "destinazione": DESTINAZIONI_AMMESSE[0], "totale_cent": 0}
    )
    if errore != "":
        raise ValueError(errore)


def _valida_record(codice, record) -> None:
    """Controlla il tipo del record e la corrispondenza con la chiave.

    Il record deve essere un valore `Preventivo` del modello U14 e il suo
    campo `codice` deve coincidere con la chiave dell'indice: questa
    corrispondenza è l'invariante che rende confrontabili chiavi e dati.
    """
    if not isinstance(record, Preventivo):
        raise TypeError("record atteso di tipo Preventivo")
    if record.codice != codice:
        raise ValueError(
            f"la chiave {codice!r} non coincide con il codice del record {record.codice!r}"
        )


def _valida_sorgente(sorgente) -> list:
    """Valida la fotografia di preventivi e restituisce la lista dei record.

    Controlli eseguiti prima di ogni costruzione: tipo dei record, validità
    delle chiavi e assenza di codici ripetuti. Un problema solleva
    l'eccezione dichiarata senza consegnare alcuna struttura parziale.
    """
    candidati = list(sorgente)
    codici_visti = []
    for record in candidati:
        if not isinstance(record, Preventivo):
            raise TypeError("la sorgente deve essere una sequenza di valori Preventivo")
        valida_chiave(record.codice)
        if record.codice in codici_visti:
            raise ValueError(f"codice ripetuto nella sorgente: {record.codice!r}")
        codici_visti.append(record.codice)
    return candidati


class _NodoIndice:
    """Nodo interno di una catena: codice, record associato e successivo."""

    __slots__ = ("codice", "record", "successivo")

    def __init__(self, codice, record, successivo=None):
        self.codice = codice
        self.record = record
        self.successivo = successivo


class IndiceHashU18:
    """Indice di consultazione per codice, costruito su tabella hash.

    Il contenitore conserva `_bucket` e `_dimensione`; i nodi `_NodoIndice`
    sono dettagli interni e non compaiono nei risultati pubblici. Ogni voce
    associa un codice a un valore `Preventivo` immutabile: condividere il
    record non espone stato modificabile.
    """

    def __init__(self, capacita=5):
        """Crea un indice vuoto con `capacita` bucket."""
        if isinstance(capacita, bool) or not isinstance(capacita, int):
            raise TypeError(
                f"capacità attesa di tipo int, ricevuto {type(capacita).__name__}"
            )
        if capacita < 1:
            raise ValueError(f"capacità minima 1, ricevuto {capacita}")
        self._bucket = [None] * capacita
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di codici presenti nell'indice."""
        return self._dimensione

    @property
    def capacita(self):
        """Restituisce il numero dei bucket; è sempre positivo."""
        return len(self._bucket)

    @property
    def fattore_carico(self):
        """Restituisce il rapporto fra voci indicizzate e bucket."""
        return self._dimensione / len(self._bucket)

    def _indice(self, codice):
        """Restituisce il bucket selezionato dal `codice`."""
        valida_chiave(codice)
        return hash_didattico(codice) % len(self._bucket)

    # ------------------------------------------------------------------
    # Ricerca
    # ------------------------------------------------------------------

    def contiene(self, codice):
        """Restituisce `True` se il codice è presente, `False` altrimenti.

        L'indice vuoto restituisce `False`; una chiave fuori dominio solleva
        `TypeError` oppure `ValueError` anche sull'indice vuoto.
        """
        valida_chiave(codice)
        corrente = self._bucket[hash_didattico(codice) % len(self._bucket)]
        while corrente is not None:
            if corrente.codice == codice:
                return True
            corrente = corrente.successivo
        return False

    def cerca(self, codice):
        """Restituisce il record associato al `codice`.

        Il codice assente solleva `KeyError`. La presenza è determinata dalla
        struttura e dal confronto del codice: il record associato è sempre un
        valore `Preventivo` completo, mai un indicatore di assenza.
        """
        valida_chiave(codice)
        corrente = self._bucket[hash_didattico(codice) % len(self._bucket)]
        while corrente is not None:
            if corrente.codice == codice:
                return corrente.record
            corrente = corrente.successivo
        raise KeyError(codice)

    def confronti_per(self, codice):
        """Restituisce il numero di confronti di uguaglianza di una ricerca."""
        valida_chiave(codice)
        confronti = 0
        corrente = self._bucket[hash_didattico(codice) % len(self._bucket)]
        while corrente is not None:
            confronti += 1
            if corrente.codice == codice:
                break
            corrente = corrente.successivo
        return confronti

    # ------------------------------------------------------------------
    # Inserimento e aggiornamento
    # ------------------------------------------------------------------

    def inserisci(self, codice, record):
        """Crea l'associazione `codice` → `record`.

        Un codice duplicato solleva `ValueError` e conserva voci e dimensione.
        Il superamento della soglia dopo un nuovo inserimento raddoppia la
        capacità e ricolloca ogni voce.
        """
        valida_chiave(codice)
        _valida_record(codice, record)
        posizione = hash_didattico(codice) % len(self._bucket)
        corrente = self._bucket[posizione]
        while corrente is not None:
            if corrente.codice == codice:
                raise ValueError(f"codice già presente: {codice!r}")
            corrente = corrente.successivo
        self._bucket[posizione] = _NodoIndice(codice, record, self._bucket[posizione])
        self._dimensione += 1
        if self._dimensione / len(self._bucket) > SOGLIA_CARICO:
            self._ridimensiona(2 * len(self._bucket))

    def aggiorna(self, codice, record):
        """Sostituisce il record associato al `codice` esistente.

        Il codice assente solleva `KeyError`. Forma e dimensione restano
        invariate: l'aggiornamento modifica soltanto il record.
        """
        valida_chiave(codice)
        _valida_record(codice, record)
        corrente = self._bucket[hash_didattico(codice) % len(self._bucket)]
        while corrente is not None:
            if corrente.codice == codice:
                corrente.record = record
                return
            corrente = corrente.successivo
        raise KeyError(codice)

    # ------------------------------------------------------------------
    # Cancellazione
    # ------------------------------------------------------------------

    def rimuovi(self, codice):
        """Elimina l'associazione del `codice` e restituisce `True`.

        Il codice assente restituisce `False` e conserva ogni voce.
        """
        valida_chiave(codice)
        posizione = hash_didattico(codice) % len(self._bucket)
        precedente = None
        corrente = self._bucket[posizione]
        while corrente is not None:
            if corrente.codice == codice:
                if precedente is None:
                    self._bucket[posizione] = corrente.successivo
                else:
                    precedente.successivo = corrente.successivo
                self._dimensione -= 1
                return True
            precedente = corrente
            corrente = corrente.successivo
        return False

    # ------------------------------------------------------------------
    # Viste e fotografia
    # ------------------------------------------------------------------

    def voci(self):
        """Restituisce una lista nuova di coppie `(codice, record)`.

        L'ordine segue i bucket e le catene ed è fuori dal contratto
        applicativo: la presentazione ordinata usa `fotografia_ordinata`.
        """
        risultato = []
        for testa in self._bucket:
            corrente = testa
            while corrente is not None:
                risultato.append((corrente.codice, corrente.record))
                corrente = corrente.successivo
        return risultato

    def fotografia_ordinata(self):
        """Restituisce le coppie `(codice, record)` in ordine lessicografico."""
        return sorted(self.voci(), key=lambda voce: voce[0])

    # ------------------------------------------------------------------
    # Crescita
    # ------------------------------------------------------------------

    def _ridimensiona(self, nuova_capacita):
        """Ricolloca ogni voce con la nuova capacità, con collocazione diretta."""
        nuovi_bucket = [None] * nuova_capacita
        for testa in self._bucket:
            corrente = testa
            while corrente is not None:
                seguente = corrente.successivo
                nuova_posizione = hash_didattico(corrente.codice) % nuova_capacita
                nuovi_bucket[nuova_posizione] = _NodoIndice(
                    corrente.codice, corrente.record, nuovi_bucket[nuova_posizione]
                )
                corrente = seguente
        self._bucket = nuovi_bucket

    # ------------------------------------------------------------------
    # Strumento diagnostico
    # ------------------------------------------------------------------

    def controlla_invarianti(self):
        """Verifica unicità, appartenenza ai bucket e dimensione.

        Lo strumento solleva `AssertionError` alla prima violazione e ha un
        costo proprio di scansione completa.
        """
        assert len(self._bucket) > 0, "capacità non positiva"
        visti = set()
        totale = 0
        for posizione, testa in enumerate(self._bucket):
            corrente = testa
            while corrente is not None:
                assert id(corrente) not in visti, "nodo raggiunto due volte"
                visti.add(id(corrente))
                valida_chiave(corrente.codice)
                atteso = hash_didattico(corrente.codice) % len(self._bucket)
                assert atteso == posizione, f"voce {corrente.codice!r} fuori bucket"
                assert isinstance(corrente.record, Preventivo), "record non Preventivo"
                assert corrente.record.codice == corrente.codice, (
                    "chiave e record non coincidenti"
                )
                totale += 1
                corrente = corrente.successivo
        assert totale == self._dimensione, (
            f"dimensione dichiarata {self._dimensione}, voci raggiungibili {totale}"
        )


def costruisci_indice(preventivi, capacita=5):
    """Costruisce l'indice completo sulla fotografia dei `preventivi`.

    La sorgente è validata prima di ogni inserimento: tipo dei record,
    validità dei codici e assenza di duplicati. Un problema solleva
    l'eccezione dichiarata senza consegnare una struttura parziale.
    """
    candidati = _valida_sorgente(preventivi)
    indice = IndiceHashU18(capacita)
    for record in candidati:
        indice.inserisci(record.codice, record)
    return indice


def misura_costruzione(codici):
    """Costruisce record sintetici e conta inserimenti e confronti simulati.

    Lo strumento conta un confronto per ogni voce già presente al momento di
    ciascun inserimento: è la misura dichiarata della pressione delle
    collisioni, distinta dal tempo del codice.
    """
    conteggi = 0
    presenti = 0
    for _codice in codici:
        conteggi += presenti
        presenti += 1
    return presenti, conteggi
