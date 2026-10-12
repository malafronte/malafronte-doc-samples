"""Tabella hash didattica con concatenamento — Unità 18 (cap. PY-34).

Il modulo realizza la classe `TabellaHashConcatenata` con i contratti del
capitolo: chiavi di tipo esatto `int` oppure `str`, valori di qualunque tipo,
inserimento in testa dopo la verifica della presenza, crescita per raddoppio
quando un nuovo inserimento porta il fattore di carico oltre la soglia 1.0 e
redistribuzione con collocazione interna diretta.

La funzione hash è deterministica e indipendente dalla capacità: per un intero
restituisce l'intero stesso, per una stringa accumula
`h = (31 * h + ord(carattere)) % 65521` su ogni carattere. L'indice del bucket
è `hash_didattico(chiave) % m`, con `m` capacità corrente. Con divisore
positivo il resto Python è un indice valido anche per interi negativi.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

#: Soglia di crescita del modello: un nuovo inserimento che porta il carico
#: oltre questo valore provoca il raddoppio della capacità.
SOGLIA_CARICO = 1.0

#: Parametri della funzione hash testuale didattica.
_BASE_STRINGHE = 31
_MODULO_STRINGHE = 65521


def hash_didattico(chiave):
    """Restituisce l'intero hash didattico della `chiave`.

    Un intero produce sé stesso; una stringa accumula il valore carattere per
    carattere con base 31 e modulo interno 65521. Un tipo fuori dal dominio
    solleva `TypeError`.
    """
    if type(chiave) is int:
        return chiave
    if type(chiave) is str:
        accumulatore = 0
        for carattere in chiave:
            accumulatore = (_BASE_STRINGHE * accumulatore + ord(carattere)) % _MODULO_STRINGHE
        return accumulatore
    raise TypeError(f"chiave attesa di tipo int o str, ricevuto {type(chiave).__name__}")


def _valida_chiave(chiave):
    """Convalida la chiave contro il dominio dichiarato della tabella.

    Il dominio è il tipo esatto `int` oppure il tipo esatto `str`: `type`
    esclude anche `bool`, che Python considera sottoinsieme di `int`, ed
    esclude le sottoclassi. La stringa vuota è una chiave ammessa dalla
    tabella generale; il costruttore dell'indice applicativo applica invece i
    vincoli del proprio dominio.
    """
    if type(chiave) not in (int, str):
        raise TypeError(f"chiave attesa di tipo int o str, ricevuto {type(chiave).__name__}")


class _NodoHash:
    """Nodo interno di una catena: chiave, valore e riferimento al successivo."""

    __slots__ = ("chiave", "valore", "successivo")

    def __init__(self, chiave, valore, successivo=None):
        self.chiave = chiave
        self.valore = valore
        self.successivo = successivo


class TabellaHashConcatenata:
    """Dizionario didattico con bucket, catene, carico e redistribuzione.

    Il contenitore conserva `_bucket`, la lista degli `m` riferimenti alle
    teste delle catene, e `_dimensione`, il numero delle associazioni
    presenti. Ogni posizione vuota contiene `None`; ogni nodo raggiungibile
    appartiene al bucket `hash_didattico(chiave) % m` e ogni chiave compare in
    una sola associazione.
    """

    def __init__(self, capacita=5):
        """Crea una tabella vuota con `capacita` bucket.

        Una capacità di tipo fuori contratto solleva `TypeError`; una capacità
        minore di 1 solleva `ValueError`.
        """
        if isinstance(capacita, bool) or not isinstance(capacita, int):
            raise TypeError(f"capacità attesa di tipo int, ricevuto {type(capacita).__name__}")
        if capacita < 1:
            raise ValueError(f"capacità minima 1, ricevuto {capacita}")
        self._bucket = [None] * capacita
        self._dimensione = 0

    def __len__(self):
        """Restituisce il numero di associazioni presenti; 0 sul vuoto."""
        return self._dimensione

    @property
    def capacita(self):
        """Restituisce il numero dei bucket; è sempre positivo."""
        return len(self._bucket)

    @property
    def fattore_carico(self):
        """Restituisce il rapporto `_dimensione / capacita`.

        Nel concatenamento il valore esprime la lunghezza media delle catene,
        includendo quelle vuote.
        """
        return self._dimensione / len(self._bucket)

    def _indice(self, chiave):
        """Restituisce il bucket selezionato dalla `chiave`."""
        _valida_chiave(chiave)
        return hash_didattico(chiave) % len(self._bucket)

    def _nodo_per_chiave(self, chiave):
        """Restituisce il nodo con la chiave richiesta, oppure `None`."""
        _valida_chiave(chiave)
        corrente = self._bucket[hash_didattico(chiave) % len(self._bucket)]
        while corrente is not None:
            if corrente.chiave == chiave:
                return corrente
            corrente = corrente.successivo
        return None

    def contiene(self, chiave):
        """Restituisce `True` se `chiave` è presente, `False` altrimenti.

        La tabella vuota e la chiave assente producono `False`; lo stato resta
        conservato.
        """
        return self._nodo_per_chiave(chiave) is not None

    def cerca(self, chiave):
        """Restituisce il valore associato a `chiave`.

        La chiave assente solleva `KeyError` e conserva lo stato. La presenza
        è determinata dalla struttura e dal confronto della chiave: un valore
        associato può valere `None`, `0`, `False` o `""` e resta un valore
        legittimo, distinto dall'assenza.
        """
        nodo = self._nodo_per_chiave(chiave)
        if nodo is None:
            raise KeyError(chiave)
        return nodo.valore

    def confronti_per(self, chiave):
        """Restituisce il numero di confronti di uguaglianza di una ricerca.

        La scansione esamina la sola catena selezionata dalla chiave: una
        catena vuota richiede 0 confronti, una ricerca riuscita conta i nodi
        fino a quello richiesto, una ricerca fallita conta l'intera catena.
        Il conteggio misura confronti fra chiavi, non letture di bucket né
        calcoli di indice.
        """
        _valida_chiave(chiave)
        confronti = 0
        corrente = self._bucket[hash_didattico(chiave) % len(self._bucket)]
        while corrente is not None:
            confronti += 1
            if corrente.chiave == chiave:
                break
            corrente = corrente.successivo
        return confronti

    def assegna(self, chiave, valore):
        """Inserisce la chiave nuova oppure aggiorna la chiave presente.

        La chiave presente conserva la propria posizione e riceve il nuovo
        valore; la chiave nuova crea un nodo in testa alla catena selezionata
        e incrementa la dimensione di uno. Quando il nuovo inserimento porta
        il carico oltre la soglia del modello, la capacità raddoppia e ogni
        associazione viene ricollocata. L'aggiornamento lascia invariata la
        capacità nella politica scelta.
        """
        _valida_chiave(chiave)
        indice = hash_didattico(chiave) % len(self._bucket)
        corrente = self._bucket[indice]
        while corrente is not None:
            if corrente.chiave == chiave:
                corrente.valore = valore
                return
            corrente = corrente.successivo
        self._bucket[indice] = _NodoHash(chiave, valore, self._bucket[indice])
        self._dimensione += 1
        if self._dimensione / len(self._bucket) > SOGLIA_CARICO:
            self._ridimensiona(2 * len(self._bucket))

    def rimuovi(self, chiave):
        """Elimina l'associazione di `chiave` e restituisce il valore rimosso.

        La cancellazione della testa sostituisce il riferimento iniziale del
        bucket; la cancellazione dopo un predecessore collega il predecessore
        al successore. La dimensione diminuisce di uno. La chiave assente
        solleva `KeyError` e conserva associazioni, dimensione e capacità.
        """
        _valida_chiave(chiave)
        indice = hash_didattico(chiave) % len(self._bucket)
        precedente = None
        corrente = self._bucket[indice]
        while corrente is not None:
            if corrente.chiave == chiave:
                if precedente is None:
                    self._bucket[indice] = corrente.successivo
                else:
                    precedente.successivo = corrente.successivo
                self._dimensione -= 1
                return corrente.valore
            precedente = corrente
            corrente = corrente.successivo
        raise KeyError(chiave)

    def coppie(self):
        """Restituisce una lista nuova di tuple `(chiave, valore)`.

        La raccolta attraversa i bucket in ordine e ciascuna catena dalla
        testa: è una fotografia superficiale delle associazioni. Gli oggetti
        valore restano condivisi con la tabella; l'ordine dei bucket e delle
        catene è fuori dal contratto applicativo.
        """
        risultato = []
        for testa in self._bucket:
            corrente = testa
            while corrente is not None:
                risultato.append((corrente.chiave, corrente.valore))
                corrente = corrente.successivo
        return risultato

    def _ridimensiona(self, nuova_capacita):
        """Ricolloca ogni associazione in una tabella di `nuova_capacita` bucket.

        Il procedimento attraversa una volta le vecchie catene nell'ordine dei
        bucket e, dentro ciascuna catena, dalla testa; calcola il nuovo indice
        di ogni chiave e crea il nodo nella nuova catena. L'ordine delle
        catene può cambiare; il risultato contrattuale è la conservazione
        delle associazioni. La collocazione è diretta, perché l'unicità è già
        stata verificata: richiamare l'inserimento pubblico per ogni nodo
        ripeterebbe la ricerca dei duplicati. La dimensione logica resta
        invariata.
        """
        nuovi_bucket = [None] * nuova_capacita
        for testa in self._bucket:
            corrente = testa
            while corrente is not None:
                seguente = corrente.successivo
                nuovo_indice = hash_didattico(corrente.chiave) % nuova_capacita
                nuovi_bucket[nuovo_indice] = _NodoHash(
                    corrente.chiave, corrente.valore, nuovi_bucket[nuovo_indice]
                )
                corrente = seguente
        self._bucket = nuovi_bucket

    def lunghezze_bucket(self):
        """Restituisce la lista delle lunghezze delle catene per bucket."""
        lunghezze = []
        for testa in self._bucket:
            lunghezza = 0
            corrente = testa
            while corrente is not None:
                lunghezza += 1
                corrente = corrente.successivo
            lunghezze.append(lunghezza)
        return lunghezze

    def controlla_invarianti(self):
        """Verifica capacità, appartenenza, unicità, termine e dimensione.

        Lo strumento solleva `AssertionError` alla prima violazione: è un
        controllo didattico della rappresentazione interna, distinto dall'API
        applicativa, con un costo proprio di scansione completa.
        """
        assert len(self._bucket) > 0, "capacità non positiva"
        assert len(self._bucket) == self.capacita, "capacità e bucket non coincidenti"
        visti = set()
        totale = 0
        for posizione, testa in enumerate(self._bucket):
            corrente = testa
            while corrente is not None:
                identita = id(corrente)
                assert identita not in visti, "nodo raggiunto due volte"
                visti.add(identita)
                _valida_chiave(corrente.chiave)
                atteso = hash_didattico(corrente.chiave) % len(self._bucket)
                assert atteso == posizione, (
                    f"chiave {corrente.chiave!r} nel bucket {posizione}, atteso {atteso}"
                )
                totale += 1
                corrente = corrente.successivo
        assert totale == self._dimensione, (
            f"dimensione dichiarata {self._dimensione}, nodi raggiungibili {totale}"
        )
        chiavi = [chiave for chiave, _valore in self.coppie()]
        assert len(set(map(repr_chiave, chiavi))) == len(chiavi), "chiave ripetuta"
        assert self._dimensione / len(self._bucket) <= SOGLIA_CARICO + 1e-9, (
            "carico oltre la soglia del modello"
        )


def repr_chiave(chiave):
    """Restituisce una rappresentazione che distingue tipo e valore.

    La distinzione serve al controllo di unicità: l'intero `7` e la stringa
    `"7"` sono chiavi diverse del modello, anche se la loro stampa può
    coincidere.
    """
    return (type(chiave).__name__, chiave)
