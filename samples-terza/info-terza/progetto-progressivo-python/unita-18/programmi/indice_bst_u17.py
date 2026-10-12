"""Indice BST di consultazione per codice del registro dei preventivi (U17).

Responsabilità del modulo: costruire, su una **fotografia** dei preventivi del
registro, un indice di consultazione ordinato per codice e rispondere a
ricerche esatte e a intervalli chiusi di codici. La struttura è un albero
binario di ricerca; il modulo la riproduce per intero — nodo interno,
inserimento, cancellazione nei tre casi, visita inordine — perché la
fotografia della raccolta resta autonoma e non importa moduli da fuori della
cartella del progetto.

**Variante dichiarata** rispetto al BST del capitolo PY-33, che usa chiavi
interi: qui le chiavi sono i **codici stringa** del registro e l'adattamento
comporta quattro precisazioni.

- **Dominio delle chiavi**: stringhe non vuote. La validazione è quella
  **riusata** dal modello del registro: `valida_chiave` richiama
  `valida_dominio_record` sul campo `codice` dello schema, senza duplicare
  regole né diagnosi.
- **Ordine**: l'ordine lessicografico che Python applica alle stringhe con
  `==`, `<` e `>`. `"003"` precede `"007"`, che precede `"012"`; `"007"` e
  `"7"` sono chiavi diverse e `"007"` precede `"7"`. L'equivalenza con un
  ordine numerico richiede che tutti i codici abbiano la stessa lunghezza.
- **Costo dei confronti**: un confronto fra chiavi stringa costa in
  proporzione ai testi confrontati, mentre nel capitolo PY-33 il confronto fra
  interi ha costo costante. I conteggi dei nodi esaminati restano quelli del
  capitolo: contano le chiavi lette, non le operazioni sui caratteri.
- **Dati associati**: i valori `Preventivo` del modello U14, già validati e
  immutabili. La chiave di ogni voce coincide con il campo `codice` del
  record associato.

Contratto dell'indice (`IndiceBSTU17`):

- **dati ammessi**: chiavi stringa non vuote e valori `Preventivo` il cui
  campo `codice` coincide con la chiave;
- **risultato**: `cerca` restituisce il record associato; `inordine`,
  `voci_ordinate` e `intervallo` restituiscono liste nuove, in ordine
  lessicografico crescente, con gli estremi dell'intervallo inclusi;
- **effetti**: le interrogazioni non modificano l'indice; `inserisci`,
  `aggiorna` e `rimuovi` modificano soltanto l'indice che le riceve;
- **errori**: chiave di tipo diverso da `str` → `TypeError`; stringa vuota →
  `ValueError`; record di tipo diverso da `Preventivo` o con codice diverso
  dalla chiave → `TypeError` oppure `ValueError`; duplicato in `inserisci` →
  `ValueError`; chiave assente in `cerca` e `aggiorna` → `KeyError`; estremi
  invertiti in `intervallo` → `ValueError`; indice vuoto in `minimo` e
  `massimo` → `IndexError`;
- **invarianti**: ogni codice compare una sola volta; la proprietà d'ordine
  stretta vale per tutti i nodi; `_dimensione` coincide con il numero di nodi
  raggiungibili; ogni voce conserva l'associazione fra chiave e record.

Ciclo di vita dell'indice, dichiarato: la costruzione avviene **dopo il
caricamento** del registro, sulla proiezione pubblica `preventivi()`, e
l'indice così costruito risponde a più interrogazioni sulla stessa
fotografia. Una modifica del registro richiede una **nuova costruzione**
dell'indice: la vecchia fotografia continua a rappresentare i dati
precedenti, perché i valori `Preventivo` sono immutabili e l'indice non
condivide con il registro né contenitori mutabili né aggiornamenti.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""
from registro_dominio import DESTINAZIONI_AMMESSE, valida_dominio_record
from registro_modello_u14 import Preventivo

_ALTEZZA_VUOTO = -1


class _NodoIndice:
    """Nodo interno dell'albero: codice, record associato e due figli."""

    __slots__ = ("codice", "record", "sinistro", "destro")

    def __init__(self, codice, record, sinistro=None, destro=None):
        self.codice = codice
        self.record = record
        self.sinistro = sinistro
        self.destro = destro


class _ContatoreNodi:
    """Contatore dei nodi esaminati: strumento di misura dichiarato.

    Un nodo risulta esaminato quando la sua chiave viene letta per decidere
    un'operazione; la visita di un collegamento vuoto appartiene alla traccia
    di controllo e non viene contata. La radice inserita per prima esamina
    0 nodi.
    """

    __slots__ = ("nodi_esaminati",)

    def __init__(self):
        self.nodi_esaminati = 0

    def registra(self):
        """Aggiunge uno al contatore dei nodi esaminati."""
        self.nodi_esaminati += 1


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


class IndiceBSTU17:
    """Indice di consultazione per codice, costruito su un BST a chiavi stringa.

    Il contenitore conserva `_radice` e `_dimensione`; i nodi `_NodoIndice`
    sono dettagli interni e non compaiono nei risultati pubblici. Ogni voce
    associa un codice a un valore `Preventivo` immutabile: condividere il
    record non espone stato modificabile.
    """

    def __init__(self):
        self._radice = None
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di codici presenti nell'indice."""
        return self._dimensione

    # ------------------------------------------------------------------
    # Ricerca
    # ------------------------------------------------------------------

    def contiene(self, codice):
        """Restituisce `True` se il codice è presente, `False` altrimenti.

        L'indice vuoto restituisce `False`; una chiave fuori dominio solleva
        `TypeError` oppure `ValueError` anche sull'indice vuoto.
        """
        valida_chiave(codice)
        return self._nodo_per_codice(codice, _ContatoreNodi()) is not None

    def cerca(self, codice):
        """Restituisce il record associato al codice.

        Il codice assente solleva `KeyError`. La presenza è determinata dalla
        struttura e dal confronto della chiave: il record associato resta un
        valore `Preventivo`, con i propri campi intatti.
        """
        valida_chiave(codice)
        nodo = self._nodo_per_codice(codice, _ContatoreNodi())
        if nodo is None:
            raise KeyError(codice)
        return nodo.record

    def misura_ricerca(self, codice):
        """Restituisce `(nodi_esaminati, record_o_None)` per la ricerca del codice.

        La discesa coincide con quella di `cerca` e di `contiene`; il secondo
        elemento è il record oppure `None` per il codice assente, che qui non
        solleva eccezioni perché il risultato della misura è il conteggio.
        """
        valida_chiave(codice)
        contatore = _ContatoreNodi()
        nodo = self._nodo_per_codice(codice, contatore)
        record = None if nodo is None else nodo.record
        return contatore.nodi_esaminati, record

    def _nodo_per_codice(self, codice, contatore):
        """Restituisce il nodo del codice, oppure `None`; conta i nodi letti."""
        corrente = self._radice
        while corrente is not None:
            contatore.registra()
            if codice == corrente.codice:
                return corrente
            if codice < corrente.codice:
                corrente = corrente.sinistro
            else:
                corrente = corrente.destro
        return None

    # ------------------------------------------------------------------
    # Inserimento, aggiornamento e cancellazione
    # ------------------------------------------------------------------

    def inserisci(self, codice, record) -> None:
        """Crea l'associazione `codice` → `record`.

        Un codice già presente solleva `ValueError` e conserva sia la forma
        dell'indice sia il record precedentemente associato.
        """
        self._inserisci_validato(codice, record, _ContatoreNodi())

    def _inserisci_validato(self, codice, record, contatore) -> None:
        """Valida e inserisce, contando i nodi esaminati nel contatore ricevuto."""
        valida_chiave(codice)
        _valida_record(codice, record)
        nuova_radice, inserito = self._inserisci(self._radice, codice, record, contatore)
        if not inserito:
            raise ValueError(f"codice già presente: {codice}")
        self._radice = nuova_radice
        self._dimensione += 1

    def _inserisci(self, nodo, codice, record, contatore):
        """Inserisce nel sottoalbero e restituisce la nuova radice e l'esito.

        Contratto della procedura ausiliaria: riceve la radice attuale del
        sottoalbero e restituisce la radice dopo la modifica, insieme al
        valore booleano che distingue l'inserimento dal rifiuto. Ogni nodo
        esistente visitato viene contato una volta.
        """
        if nodo is None:
            return _NodoIndice(codice, record), True
        contatore.registra()
        if codice == nodo.codice:
            return nodo, False
        if codice < nodo.codice:
            nodo.sinistro, inserito = self._inserisci(
                nodo.sinistro, codice, record, contatore
            )
        else:
            nodo.destro, inserito = self._inserisci(
                nodo.destro, codice, record, contatore
            )
        return nodo, inserito

    def aggiorna(self, codice, record) -> None:
        """Sostituisce il record associato al codice esistente.

        Il codice assente solleva `KeyError`. Forma e dimensione restano
        invariate: l'aggiornamento modifica soltanto il record.
        """
        valida_chiave(codice)
        _valida_record(codice, record)
        nodo = self._nodo_per_codice(codice, _ContatoreNodi())
        if nodo is None:
            raise KeyError(codice)
        nodo.record = record

    def rimuovi(self, codice):
        """Elimina l'associazione del codice e restituisce `True`.

        Il codice assente restituisce `False` e conserva ogni record. Le
        associazioni dei codici mantenuti non cambiano, compreso il caso con
        due figli in cui chiave e record del successore inordine occupano la
        posizione del nodo eliminato.
        """
        valida_chiave(codice)
        nuova_radice, rimosso = self._rimuovi(self._radice, codice)
        if rimosso:
            self._radice = nuova_radice
            self._dimensione -= 1
        return rimosso

    def _rimuovi(self, nodo, codice):
        """Rimuove dal sottoalbero e restituisce la nuova radice e l'esito.

        La procedura gestisce i collegamenti e comunica l'esito; il contatore
        del contenitore viene aggiornato una sola volta dal metodo pubblico
        `rimuovi`.
        """
        if nodo is None:
            return None, False
        if codice < nodo.codice:
            nodo.sinistro, rimosso = self._rimuovi(nodo.sinistro, codice)
            return nodo, rimosso
        if codice > nodo.codice:
            nodo.destro, rimosso = self._rimuovi(nodo.destro, codice)
            return nodo, rimosso

        # Il codice coincide: il nodo corrente va eliminato.
        if nodo.sinistro is None:
            # Nessun figlio oppure solo il figlio destro.
            return nodo.destro, True
        if nodo.destro is None:
            # Solo il figlio sinistro.
            return nodo.sinistro, True

        # Due figli: il successore inordine è il minimo del sottoalbero
        # destro. Codice e record del successore sostituiscono quelli del
        # nodo corrente; il nodo del successore viene poi eliminato con una
        # rimozione che ricade nei casi già trattati.
        successore = nodo.destro
        while successore.sinistro is not None:
            successore = successore.sinistro
        nodo.codice = successore.codice
        nodo.record = successore.record
        nodo.destro, _ = self._rimuovi(nodo.destro, successore.codice)
        return nodo, True

    # ------------------------------------------------------------------
    # Estremi e vista ordinata
    # ------------------------------------------------------------------

    def minimo(self):
        """Restituisce il codice minimo; l'indice vuoto solleva `IndexError`."""
        if self._radice is None:
            raise IndexError("indice vuoto: minimo non definito")
        corrente = self._radice
        while corrente.sinistro is not None:
            corrente = corrente.sinistro
        return corrente.codice

    def massimo(self):
        """Restituisce il codice massimo; l'indice vuoto solleva `IndexError`."""
        if self._radice is None:
            raise IndexError("indice vuoto: massimo non definito")
        corrente = self._radice
        while corrente.destro is not None:
            corrente = corrente.destro
        return corrente.codice

    def inordine(self):
        """Restituisce una nuova lista dei codici in ordine lessicografico.

        La lista è la **vista ordinata** dell'indice: non è la raccolta del
        registro, che conserva il proprio ordine di inserimento.
        """
        risultato = []
        self._inordine(self._radice, risultato)
        return risultato

    def _inordine(self, nodo, risultato):
        if nodo is None:
            return
        self._inordine(nodo.sinistro, risultato)
        risultato.append(nodo.codice)
        self._inordine(nodo.destro, risultato)

    def voci_ordinate(self):
        """Restituisce una nuova lista di coppie `(codice, record)` in ordine crescente.

        La raccolta diretta delle coppie in una sola visita evita una ricerca
        per ciascun codice già incontrato.
        """
        risultato = []
        self._voci(self._radice, risultato)
        return risultato

    def _voci(self, nodo, risultato):
        if nodo is None:
            return
        self._voci(nodo.sinistro, risultato)
        risultato.append((nodo.codice, nodo.record))
        self._voci(nodo.destro, risultato)

    # ------------------------------------------------------------------
    # Altezza e intervalli
    # ------------------------------------------------------------------

    def altezza(self):
        """Restituisce l'altezza in archi; il sottoalbero vuoto vale -1."""
        return self._altezza(self._radice)

    def _altezza(self, nodo):
        if nodo is None:
            return _ALTEZZA_VUOTO
        return 1 + max(self._altezza(nodo.sinistro), self._altezza(nodo.destro))

    def intervallo(self, minimo, massimo):
        """Restituisce le coppie con codice nell'intervallo chiuso `[minimo, massimo]`.

        Il risultato è ordinato in modo crescente e include entrambi gli
        estremi. L'indice vuoto e l'assenza di corrispondenze producono la
        lista vuota; `minimo > massimo` solleva `ValueError`.
        """
        valida_chiave(minimo)
        valida_chiave(massimo)
        if minimo > massimo:
            raise ValueError("l'estremo minimo non può superare l'estremo massimo")
        risultato = []
        self._intervallo(self._radice, minimo, massimo, risultato)
        return risultato

    def _intervallo(self, nodo, minimo, massimo, risultato):
        if nodo is None:
            return
        # Il sottoalbero sinistro contiene solo codici minori del corrente:
        # viene visitato soltanto se può contenere codici >= minimo.
        if minimo < nodo.codice:
            self._intervallo(nodo.sinistro, minimo, massimo, risultato)
        if minimo <= nodo.codice <= massimo:
            risultato.append((nodo.codice, nodo.record))
        # Il sottoalbero destro contiene solo codici maggiori del corrente:
        # viene visitato soltanto se può contenere codici <= massimo.
        if nodo.codice < massimo:
            self._intervallo(nodo.destro, minimo, massimo, risultato)

    # ------------------------------------------------------------------
    # Strumento diagnostico
    # ------------------------------------------------------------------

    def controlla_invarianti(self) -> None:
        """Verifica struttura, ordine, dimensione e associazioni.

        Una violazione solleva `AssertionError`. Lo strumento ha un costo
        proprio e non viene richiamato dalle operazioni: la sua scansione
        completa dentro ogni metodo modificherebbe i costi osservati.
        """
        visti = set()
        totale = self._visita_struttura(self._radice, None, None, visti)
        assert totale == self._dimensione, (
            f"dimensione dichiarata {self._dimensione}, nodi raggiungibili {totale}"
        )
        if self._radice is None:
            assert self._dimensione == 0, "radice vuota con dimensione diversa da 0"

    def _visita_struttura(self, nodo, limite_inferiore, limite_superiore, visti):
        if nodo is None:
            return 0
        identita = id(nodo)
        assert identita not in visti, f"nodo raggiunto due volte con codice {nodo.codice}"
        visti.add(identita)
        valida_chiave(nodo.codice)
        _valida_record(nodo.codice, nodo.record)
        if limite_inferiore is not None:
            assert nodo.codice > limite_inferiore, (
                f"codice {nodo.codice} non superiore al limite {limite_inferiore}"
            )
        if limite_superiore is not None:
            assert nodo.codice < limite_superiore, (
                f"codice {nodo.codice} non inferiore al limite {limite_superiore}"
            )
        sinistro = self._visita_struttura(
            nodo.sinistro, limite_inferiore, nodo.codice, visti
        )
        destro = self._visita_struttura(nodo.destro, nodo.codice, limite_superiore, visti)
        return 1 + sinistro + destro


def costruisci_indice(sorgente):
    """Restituisce l'indice costruito sulla fotografia `sorgente` dei preventivi.

    La sorgente è una sequenza di valori `Preventivo`, come la tupla
    restituita dalla proiezione pubblica `registro.preventivi()`. Tutti i
    controlli precedono la costruzione: tipo dei record, validità delle chiavi
    e assenza di codici ripetuti. Un problema solleva l'eccezione dichiarata
    **prima** che qualsiasi struttura venga consegnata: il cliente non riceve
    mai un indice parziale.
    """
    return _costruisci(sorgente, _ContatoreNodi())


def misura_costruzione(sorgente):
    """Restituisce `(indice, nodi_esaminati)` per la costruzione da `sorgente`.

    Il costo di costruzione resta **separato** da quello delle interrogazioni:
    il valore contato riguarda i nodi esaminati dagli inserimenti dell'intera
    sorgente, con la regola dichiarata da `_ContatoreNodi`. Controlli ed esiti
    coincidono con quelli di `costruisci_indice`.
    """
    contatore = _ContatoreNodi()
    indice = _costruisci(sorgente, contatore)
    return indice, contatore.nodi_esaminati


def _costruisci(sorgente, contatore):
    """Valida la sorgente e costruisce l'indice contando i nodi esaminati."""
    candidati = _valida_sorgente(sorgente)
    indice = IndiceBSTU17()
    for record in candidati:
        indice._inserisci_validato(record.codice, record, contatore)
    return indice
