"""Indice B-tree di consultazione per codice del registro dei preventivi (U19).

Responsabilità del modulo: costruire, su una **fotografia** dei preventivi
del registro, un indice di consultazione per codice con ricerca esatta,
viste ordinate e intervalli, e rispondere a più interrogazioni sulla stessa
fotografia. La struttura è il B-tree didattico del capitolo PY-35 con grado
minimo 2; il modulo la riproduce per intero — nodi con voci e figli,
inserimento con divisioni dal basso, ricerca con conteggi, visita ordinata —
perché la fotografia della raccolta resta autonoma e non importa moduli da
fuori della cartella del progetto.

**Variante dichiarata** rispetto al B-tree del capitolo, che ammette chiavi
di tipo esatto `int` oppure `str`: qui le chiavi sono i **codici stringa**
del registro e l'adattamento comporta tre precisazioni.

- **Dominio delle chiavi**: stringhe non vuote. La validazione è quella
  **riusata** dal modello del registro: `valida_chiave` richiama
  `valida_dominio_record` sul campo `codice` dello schema, senza duplicare
  regole né diagnosi. I codici conservano gli zeri significativi perché
  restano stringhe: `"007"` e `"7"` sono chiavi diverse e il confronto è
  lessicografico.
- **Dati associati**: i valori `Preventivo` del modello U14, già validati e
  immutabili. La chiave di ogni voce coincide con il campo `codice` del
  record associato; ogni voce trasferisce la coppia completa.
- **Modifiche disponibili**: inserimento con divisioni dal basso e
  consultazione. Le cancellazioni dinamiche del B-tree nel dossier sono
  simulazioni o ricostruzioni: una modifica del registro richiede una
  **nuova costruzione** dell'indice, come nelle tappe precedenti.

Contratto dell'indice (`IndiceBTreeU19`):

- **dati ammessi**: chiavi stringa non vuote e valori `Preventivo` il cui
  campo `codice` coincide con la chiave;
- **risultato**: `cerca` restituisce il record associato; `voci_ordinate` e
  `fotografia_ordinata` restituiscono liste nuove in ordine lessicografico
  crescente dei codici, comprese le voci dei nodi interni; `intervallo`
  restituisce le coppie con codice fra gli estremi inclusi;
- **effetti**: le interrogazioni non modificano l'indice; `inserisci`
  modifica soltanto l'indice che lo riceve;
- **errori**: chiave di tipo diverso da `str` → `TypeError`; stringa vuota →
  `ValueError`; record di tipo diverso da `Preventivo` o con codice diverso
  dalla chiave → `TypeError` oppure `ValueError`; duplicato in `inserisci` →
  `ValueError`; chiave assente in `cerca` → `KeyError`; intervallo invertito
  in `intervallo` → `ValueError`;
- **invarianti**: ogni codice compare una sola volta; ogni nodo diverso
  dalla radice ha da una a tre voci; ogni nodo interno con `k` voci ha
  `k + 1` figli; tutte le foglie sono alla stessa profondità.

Ciclo di vita dell'indice, dichiarato: la costruzione avviene **dopo il
caricamento** del registro, sulla proiezione pubblica `preventivi()`, e
l'indice così costruito risponde a più interrogazioni sulla stessa
fotografia. Una modifica del registro richiede una **nuova costruzione**
dell'indice: la vecchia fotografia continua a rappresentare i dati
precedenti, perché i valori `Preventivo` sono immutabili.

L'indice B-tree serve query esatte, viste ordinate e intervalli; l'indice
hash della tappa U18 conserva il proprio ruolo nelle query esatte con costo
atteso e l'indice BST della tappa U17 nelle query ordinate su memoria
interna. Il confronto fra le consultazioni appartiene al rapporto della
tappa, costruito dal punto di avvio `confronto_cli_u19.py`.

Nessuna lettura, nessuna scrittura, nessuna stampa: l'import non ha effetti.
"""

from registro_dominio import DESTINAZIONI_AMMESSE, valida_dominio_record
from registro_modello_u14 import Preventivo

#: Grado minimo del B-tree della tappa: nodi stabili da una a tre voci.
GRADO_MINIMO = 2


def valida_chiave(codice) -> None:
    """Convalida la chiave dell'indice e non restituisce nulla.

    La validazione è quella **riusata** dal modello del registro: il codice
    deve superare il controllo del campo `codice` di `valida_dominio_record`,
    applicato a un record sintetico che lascia gli altri due campi nel
    dominio. Un valore che non è una stringa solleva `TypeError`; una stringa
    vuota solleva `ValueError`. Entrambi gli errori precedono ogni effetto e
    valgono anche sull'indice vuoto.
    """
    if not isinstance(codice, str):
        raise TypeError(f"chiave attesa di tipo str, ricevuto {type(codice).__name__}")
    errore = valida_dominio_record(
        {"codice": codice, "destinazione": DESTINAZIONI_AMMESSE[0], "totale_cent": 0}
    )
    if errore != "":
        raise ValueError(errore)


def _valida_record(codice, record) -> None:
    """Controlla il tipo del record e la corrispondenza con la chiave."""
    if not isinstance(record, Preventivo):
        raise TypeError("record atteso di tipo Preventivo")
    if record.codice != codice:
        raise ValueError(
            f"la chiave {codice!r} non coincide con il codice del record {record.codice!r}"
        )


def _valida_sorgente(sorgente) -> list:
    """Valida la fotografia di preventivi e restituisce la lista dei record.

    Controlli eseguiti prima di ogni costruzione: tipo dei record, validità
    dei codici e assenza di codici ripetuti. Un problema solleva l'eccezione
    dichiarata senza consegnare alcuna struttura parziale.
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


class _NodoBTree:
    """Nodo del B-tree: voci `(codice, record)` ordinate e figli."""

    __slots__ = ("figli", "voci")

    def __init__(self, voci=None, figli=None):
        self.voci = list(voci) if voci else []
        self.figli = list(figli) if figli else []

    def e_foglia(self):
        """Restituisce `True` quando il nodo non ha figli."""
        return len(self.figli) == 0


class IndiceBTreeU19:
    """Indice di consultazione per codice, costruito su B-tree di grado 2."""

    def __init__(self):
        """Crea un indice vuoto."""
        self._radice = None
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di codici presenti, compresi gli interni."""
        return self._dimensione

    @property
    def altezza(self):
        """Restituisce l'altezza in archi; -1 sull'indice vuoto."""
        altezza = -1
        nodo = self._radice
        while nodo is not None:
            altezza += 1
            nodo = nodo.figli[0] if not nodo.e_foglia() else None
        return altezza

    @staticmethod
    def _posizione(voci, codice):
        """Restituisce il primo indice con codice almeno pari a `codice`."""
        indice = 0
        while indice < len(voci) and voci[indice][0] < codice:
            indice += 1
        return indice

    def _discendi(self, codice):
        """Restituisce la coppia `(nodo, indice)` della voce richiesta."""
        valida_chiave(codice)
        nodo = self._radice
        while nodo is not None:
            indice = self._posizione(nodo.voci, codice)
            if indice < len(nodo.voci) and nodo.voci[indice][0] == codice:
                return nodo, indice
            if nodo.e_foglia():
                return None, 0
            nodo = nodo.figli[indice]
        return None, 0

    def cerca(self, codice):
        """Restituisce il record associato al `codice`.

        La voce in un nodo interno del B-tree si risolve senza visitare i
        figli del nodo. Il codice assente solleva `KeyError`.
        """
        nodo, indice = self._discendi(codice)
        if nodo is None:
            raise KeyError(codice)
        return nodo.voci[indice][1]

    def contiene(self, codice):
        """Restituisce `True` se il codice è presente, `False` altrimenti."""
        valida_chiave(codice)
        nodo, _indice = self._discendi(codice)
        return nodo is not None

    def ricerca_con_conteggi(self, codice):
        """Esegue la ricerca e documenta percorso, nodi e confronti.

        Ogni confronto d'ordine fra il codice richiesto e un codice del nodo
        conta uno, compresa l'ultima valutazione falsa; ogni uguaglianza
        effettivamente eseguita conta uno. Il risultato logico coincide con
        `cerca`; l'assenza solleva `KeyError` soltanto in `cerca`.
        """
        valida_chiave(codice)
        percorso, nodi, ordine, uguaglianza = [], 0, 0, 0
        nodo = self._radice
        while nodo is not None:
            nodi += 1
            percorso.append([voce[0] for voce in nodo.voci])
            indice = 0
            while indice < len(nodo.voci) and nodo.voci[indice][0] < codice:
                ordine += 1
                indice += 1
            if indice < len(nodo.voci):
                ordine += 1
                uguaglianza += 1
                if nodo.voci[indice][0] == codice:
                    return {
                        "trovato": True,
                        "record": nodo.voci[indice][1],
                        "percorso": percorso,
                        "nodi": nodi,
                        "confronti": ordine + uguaglianza,
                    }
            if nodo.e_foglia():
                return {
                    "trovato": False,
                    "record": None,
                    "percorso": percorso,
                    "nodi": nodi,
                    "confronti": ordine + uguaglianza,
                }
            nodo = nodo.figli[indice]
        return {
            "trovato": False,
            "record": None,
            "percorso": percorso,
            "nodi": nodi,
            "confronti": ordine + uguaglianza,
        }

    def voci_ordinate(self):
        """Restituisce una lista nuova di coppie in ordine di codice."""
        risultato = []

        def _visita(nodo):
            for indice, voce in enumerate(nodo.voci):
                if not nodo.e_foglia():
                    _visita(nodo.figli[indice])
                risultato.append(voce)
            if not nodo.e_foglia():
                _visita(nodo.figli[len(nodo.voci)])

        if self._radice is not None:
            _visita(self._radice)
        return risultato

    def fotografia_ordinata(self):
        """Restituisce le coppie `(codice, record)` in ordine lessicografico."""
        return self.voci_ordinate()

    def intervallo(self, minimo, massimo):
        """Restituisce le coppie con codice fra gli estremi inclusi.

        Un intervallo con il limite inferiore maggiore del superiore solleva
        `ValueError`; un intervallo valido privo di codici restituisce una
        lista vuota. La versione comune filtra la visita completa.
        """
        valida_chiave(minimo)
        valida_chiave(massimo)
        if minimo > massimo:
            raise ValueError(
                f"intervallo invertito: {minimo!r} maggiore di {massimo!r}"
            )
        return [
            (codice, record)
            for codice, record in self.voci_ordinate()
            if minimo <= codice <= massimo
        ]

    def _dividi(self, nodo):
        """Divide il nodo con quattro voci; restituisce separatrice e destro."""
        separatrice = nodo.voci[GRADO_MINIMO - 1]
        destro = _NodoBTree(nodo.voci[GRADO_MINIMO:], [])
        if not nodo.e_foglia():
            destro.figli = nodo.figli[GRADO_MINIMO:]
            nodo.figli = nodo.figli[:GRADO_MINIMO]
        nodo.voci = nodo.voci[: GRADO_MINIMO - 1]
        return separatrice, destro

    def _inserisci(self, nodo, codice, record):
        """Inserisce nel sottoalbero; restituisce l'eventuale split."""
        indice = self._posizione(nodo.voci, codice)
        if indice < len(nodo.voci) and nodo.voci[indice][0] == codice:
            raise ValueError(f"codice già presente: {codice!r}")
        if nodo.e_foglia():
            nodo.voci.insert(indice, (codice, record))
            if len(nodo.voci) == 2 * GRADO_MINIMO:
                return self._dividi(nodo)
            return None
        esito = self._inserisci(nodo.figli[indice], codice, record)
        if esito is None:
            return None
        separatrice, destro = esito
        nodo.voci.insert(indice, separatrice)
        nodo.figli.insert(indice + 1, destro)
        if len(nodo.voci) == 2 * GRADO_MINIMO:
            return self._dividi(nodo)
        return None

    def inserisci(self, codice, record):
        """Crea l'associazione `codice` → `record` con divisioni dal basso.

        Un codice duplicato solleva `ValueError` e conserva voci e
        dimensione. La divisione della vecchia radice crea una nuova radice
        con una separatrice e due figli.
        """
        valida_chiave(codice)
        _valida_record(codice, record)
        if self._radice is None:
            self._radice = _NodoBTree([(codice, record)], [])
            self._dimensione += 1
            return
        esito = self._inserisci(self._radice, codice, record)
        if esito is not None:
            separatrice, destro = esito
            self._radice = _NodoBTree([separatrice], [self._radice, destro])
        self._dimensione += 1

    def controlla_invarianti(self):
        """Verifica lo stato stabile; solleva `AssertionError` al difetto."""
        if self._radice is None:
            assert self._dimensione == 0, "dimensione con radice assente"
            return
        visitati, visti, totale, profondita = set(), set(), [0], []

        def _visita(nodo, minimo, massimo, livello):
            assert id(nodo) not in visitati, "nodo raggiunto due volte"
            visitati.add(id(nodo))
            numero = len(nodo.voci)
            if nodo is self._radice:
                assert 1 <= numero <= 2 * GRADO_MINIMO - 1, f"radice con {numero} voci"
            else:
                assert GRADO_MINIMO - 1 <= numero <= 2 * GRADO_MINIMO - 1, (
                    f"nodo con {numero} voci"
                )
            precedente = None
            for codice, record in nodo.voci:
                valida_chiave(codice)
                assert codice not in visti, f"codice {codice!r} duplicato"
                visti.add(codice)
                if precedente is not None:
                    assert precedente < codice, "voci non ordinate nel nodo"
                precedente = codice
                if minimo is not None:
                    assert minimo < codice, f"codice {codice!r} sotto il limite"
                if massimo is not None:
                    assert codice < massimo, f"codice {codice!r} sopra il limite"
                assert isinstance(record, Preventivo), "record non Preventivo"
                assert record.codice == codice, "chiave e record non coincidenti"
                totale[0] += 1
            if nodo.e_foglia():
                profondita.append(livello)
            else:
                assert len(nodo.figli) == numero + 1, (
                    f"{numero} voci e {len(nodo.figli)} figli"
                )
                limiti = [minimo] + [voce[0] for voce in nodo.voci] + [massimo]
                for posizione, figlio in enumerate(nodo.figli):
                    _visita(
                        figlio, limiti[posizione], limiti[posizione + 1], livello + 1
                    )

        _visita(self._radice, None, None, 0)
        assert len(set(profondita)) == 1, "foglie a profondità diverse"
        assert totale[0] == self._dimensione, (
            f"dimensione dichiarata {self._dimensione}, voci raggiungibili {totale[0]}"
        )


def costruisci_indice(preventivi):
    """Costruisce l'indice completo sulla fotografia dei `preventivi`.

    La sorgente è validata prima di ogni inserimento: tipo dei record,
    validità dei codici e assenza di duplicati. Un problema solleva
    l'eccezione dichiarata senza consegnare una struttura parziale.
    """
    candidati = _valida_sorgente(preventivi)
    indice = IndiceBTreeU19()
    for record in candidati:
        indice.inserisci(record.codice, record)
    indice.controlla_invarianti()
    return indice
