"""B-tree didattico con grado minimo — Unità 19 (cap. PY-35).

Il modulo realizza il contenitore `BTreeDidattico` con i contratti del
capitolo: nodi con voci ordinate `(chiave, dato)`, grado minimo `t` fissato
alla costruzione, chiavi di tipo esatto `int` oppure `str`, unicità delle
chiavi nell'intero B-tree, occupazione da `t - 1` a `2t - 1` voci per ogni
nodo diverso dalla radice, esattamente `k + 1` figli per un nodo interno con
`k` voci e tutte le foglie alla stessa profondità.

La variante delle modifiche adottata in tutti i materiali è la riparazione
dal basso: l'inserimento colloca la voce nella foglia e divide gli eventuali
nodi eccedenti risalendo verso la radice; la cancellazione rimuove la voce e
ripara gli eventuali nodi carenti risalendo verso la radice. Un nodo in attesa
di riparazione è uno stato temporaneo: il metodo `controlla_invarianti`
verifica gli stati stabili completati.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations


def _valida_chiave(chiave, tipo_chiave):
    """Convalida la `chiave` contro il dominio dichiarato del B-tree.

    Il dominio è il tipo esatto indicato da `tipo_chiave`, `int` oppure `str`:
    `type` esclude anche `bool`, che Python considera sottoinsieme di `int`,
    ed esclude le sottoclassi. Le chiavi di una stessa istanza hanno tutte lo
    stesso tipo; il dato associato può essere di qualunque tipo, compresi
    `None`, `0` e la stringa vuota. Un tipo fuori dominio solleva `TypeError`.
    """
    if tipo_chiave not in (int, str):
        raise ValueError(f"tipo_chiave atteso int o str, ricevuto {tipo_chiave!r}")
    if type(chiave) is not tipo_chiave:
        raise TypeError(
            f"chiave attesa di tipo {tipo_chiave.__name__}, ricevuto {type(chiave).__name__}"
        )


class NodoBTree:
    """Nodo didattico del B-tree: voci ordinate e riferimenti ai figli.

    L'attributo `voci` è la lista delle coppie `(chiave, dato)` del nodo del
    B-tree, in ordine strettamente crescente delle chiavi. L'attributo `figli`
    è la lista dei riferimenti ai nodi figli del nodo del B-tree: una lista
    vuota indica una foglia del B-tree, una lista di `k + 1` riferimenti indica
    un nodo interno del B-tree con `k` voci. Ogni nodo del B-tree dispone di
    liste proprie: la costruzione condivide soltanto le coppie immutabili.
    """

    __slots__ = ("voci", "figli")

    def __init__(self, voci=None, figli=None):
        self.voci = list(voci) if voci else []
        self.figli = list(figli) if figli else []

    def e_foglia(self):
        """Restituisce `True` quando il nodo del B-tree non ha figli."""
        return len(self.figli) == 0

    def chiavi(self):
        """Restituisce la lista delle chiavi del nodo del B-tree, in ordine."""
        return [chiave for chiave, _dato in self.voci]


class EsitoRicerca:
    """Risultato strumentato della ricerca di una chiave nel B-tree.

    L'attributo `trovato` indica se la chiave è presente nel B-tree;
    l'attributo `dato` conserva il dato associato quando la ricerca ha
    successo, `None` altrimenti. L'attributo `percorso` elenca le chiavi di
    ogni nodo del B-tree visitato dalla ricerca, dalla radice verso la foglia.
    Gli attributi `nodi`, `confronti_ordine` e `confronti_uguaglianza`
    contano rispettivamente i nodi del B-tree visitati, i confronti d'ordine
    fra la chiave richiesta e le chiavi dei nodi e le uguaglianze
    effettivamente eseguite; `confronti` è la somma dei due conteggi.
    """

    __slots__ = ("trovato", "dato", "percorso", "nodi", "confronti_ordine", "confronti_uguaglianza")

    def __init__(self, trovato, dato, percorso, nodi, confronti_ordine, confronti_uguaglianza):
        self.trovato = trovato
        self.dato = dato
        self.percorso = percorso
        self.nodi = nodi
        self.confronti_ordine = confronti_ordine
        self.confronti_uguaglianza = confronti_uguaglianza

    @property
    def confronti(self):
        """Restituisce il totale dei confronti fra chiavi della ricerca."""
        return self.confronti_ordine + self.confronti_uguaglianza


class BTreeDidattico:
    """Contenitore didattico con voci ordinate, grado minimo e invarianti.

    Il contenitore conserva `radice`, il riferimento al nodo radice del
    B-tree (`None` sul B-tree vuoto), `grado_minimo`, il grado minimo `t` del
    B-tree, `tipo_chiave`, il tipo esatto delle chiavi, e `dimensione`, il
    numero delle associazioni presenti nel B-tree comprese le voci dei nodi
    interni del B-tree.
    """

    def __init__(self, grado_minimo=2, tipo_chiave=int):
        """Crea un B-tree vuoto con grado minimo e dominio delle chiavi dati.

        Un grado minimo minore di 2 solleva `ValueError`; un tipo di chiave
        diverso da `int` e `str` solleva `ValueError`.
        """
        if isinstance(grado_minimo, bool) or not isinstance(grado_minimo, int):
            raise TypeError(
                f"grado minimo atteso di tipo int, ricevuto {type(grado_minimo).__name__}"
            )
        if grado_minimo < 2:
            raise ValueError(f"grado minimo atteso almeno 2, ricevuto {grado_minimo}")
        if tipo_chiave not in (int, str):
            raise ValueError(f"tipo_chiave atteso int o str, ricevuto {tipo_chiave!r}")
        self.radice = None
        self.grado_minimo = grado_minimo
        self.tipo_chiave = tipo_chiave
        self.dimensione = 0

    def __len__(self):
        """Restituisce il numero di associazioni del B-tree; 0 sul vuoto."""
        return self.dimensione

    # -- Consultazione ----------------------------------------------------

    @staticmethod
    def _posizione_locale(voci, chiave):
        """Restituisce il primo indice `i` con chiave almeno pari a `chiave`.

        La scansione locale del nodo del B-tree esamina le voci in ordine e si
        arresta alla prima chiave maggiore o uguale alla chiave richiesta;
        quando tutte le chiavi del nodo sono minori, restituisce `k`, il numero
        delle voci del nodo. Il chiamante conta i confronti d'ordine.
        """
        indice = 0
        while indice < len(voci) and voci[indice][0] < chiave:
            indice += 1
        return indice

    def _cerca_nodo(self, chiave):
        """Restituisce la coppia `(nodo, indice)` della voce richiesta.

        La ricerca nel B-tree confronta la chiave richiesta con le chiavi del
        nodo corrente del B-tree e prosegue nel figlio del nodo che copre
        l'intervallo della chiave. Quando la ricerca nel B-tree incontra la
        voce, restituisce il nodo del B-tree e l'indice della voce; quando la
        ricerca raggiunge una foglia del B-tree senza incontrare la voce,
        restituisce `(None, 0)`. La ricerca nel B-tree non modifica lo stato.
        """
        _valida_chiave(chiave, self.tipo_chiave)
        nodo = self.radice
        while nodo is not None:
            indice = self._posizione_locale(nodo.voci, chiave)
            if indice < len(nodo.voci) and nodo.voci[indice][0] == chiave:
                return nodo, indice
            if nodo.e_foglia():
                return None, 0
            nodo = nodo.figli[indice]
        return None, 0

    def cerca(self, chiave):
        """Restituisce il dato associato alla `chiave` nel B-tree.

        Quando la voce è in un nodo interno del B-tree, il metodo `cerca` del
        B-tree restituisce il dato senza visitare i figli del nodo. Una chiave
        assente dal B-tree solleva `KeyError`; un dato `None` conservato nel
        B-tree è invece un risultato legittimo. Il metodo conserva lo stato.
        """
        nodo, indice = self._cerca_nodo(chiave)
        if nodo is None:
            raise KeyError(chiave)
        return nodo.voci[indice][1]

    def contiene(self, chiave):
        """Restituisce `True` quando la `chiave` è presente nel B-tree.

        Una chiave assente dal B-tree o un B-tree vuoto producono `False`. Una
        chiave di tipo fuori dominio solleva `TypeError`.
        """
        _valida_chiave(chiave, self.tipo_chiave)
        nodo, _indice = self._cerca_nodo(chiave)
        return nodo is not None

    def ricerca_con_conteggi(self, chiave):
        """Esegue la ricerca della `chiave` contando nodi e confronti.

        Il risultato logico della ricerca con conteggi coincide con il metodo
        `cerca` del B-tree; l'oggetto `EsitoRicerca` documenta inoltre il
        percorso dei nodi del B-tree e i contatori. Ogni confronto d'ordine fra
        la chiave richiesta e una chiave del nodo del B-tree incrementa il
        contatore d'ordine, compresa l'ultima valutazione falsa che arresta la
        scansione locale; ogni uguaglianza effettivamente eseguita sulla voce
        candidata incrementa il contatore d'uguaglianza. Gli accessi agli
        indici delle liste del nodo non rientrano in questi conteggi.
        """
        _valida_chiave(chiave, self.tipo_chiave)
        percorso = []
        nodi = 0
        confronti_ordine = 0
        confronti_uguaglianza = 0
        nodo = self.radice
        while nodo is not None:
            nodi += 1
            percorso.append(nodo.chiavi())
            indice = 0
            while indice < len(nodo.voci) and nodo.voci[indice][0] < chiave:
                confronti_ordine += 1
                indice += 1
            if indice < len(nodo.voci):
                confronti_ordine += 1
            if indice < len(nodo.voci) and nodo.voci[indice][0] == chiave:
                confronti_uguaglianza += 1
                return EsitoRicerca(
                    True,
                    nodo.voci[indice][1],
                    percorso,
                    nodi,
                    confronti_ordine,
                    confronti_uguaglianza,
                )
            if indice < len(nodo.voci):
                confronti_uguaglianza += 1
            if nodo.e_foglia():
                return EsitoRicerca(
                    False, None, percorso, nodi, confronti_ordine, confronti_uguaglianza
                )
            nodo = nodo.figli[indice]
        return EsitoRicerca(False, None, percorso, nodi, confronti_ordine, confronti_uguaglianza)

    def voci_ordinate(self):
        """Restituisce una nuova lista di coppie in ordine crescente.

        La visita ordinata del B-tree alterna ogni figlio del nodo del B-tree
        alla voce successiva del nodo e comprende anche le voci dei nodi
        interni del B-tree. La lista restituita è un nuovo oggetto: modifiche
        alla lista non alterano il B-tree.
        """
        risultato = []

        def _visita(nodo):
            for indice, voce in enumerate(nodo.voci):
                if not nodo.e_foglia():
                    _visita(nodo.figli[indice])
                risultato.append(voce)
            if not nodo.e_foglia():
                _visita(nodo.figli[len(nodo.voci)])

        if self.radice is not None:
            _visita(self.radice)
        return risultato

    def altezza(self):
        """Restituisce l'altezza in archi del B-tree; -1 sul B-tree vuoto.

        Un B-tree formato dalla sola radice foglia del B-tree ha altezza 0.
        """
        altezza = -1
        nodo = self.radice
        while nodo is not None:
            altezza += 1
            nodo = nodo.figli[0] if not nodo.e_foglia() else None
        return altezza

    # -- Verifica degli invarianti ----------------------------------------

    def controlla_invarianti(self):
        """Verifica lo stato stabile del B-tree e segnala il vincolo violato.

        Lo strumento visita la struttura completa del B-tree e controlla
        occupazione dei nodi, numero dei figli (`k + 1` per un nodo interno
        con `k` voci), tipo e unicità delle chiavi, ordine locale delle voci,
        limiti ereditati dagli antenati del nodo, profondità uniforme delle
        foglie del B-tree e coincidenza della dimensione dichiarata con le
        voci raggiunte. Riconosce anche riferimenti ripetuti a uno stesso nodo
        del B-tree e cicli nelle strutture artificialmente corrotte. Alla prima
        violazione solleva `AssertionError` con il vincolo e il contesto; è un
        controllo didattico con un costo proprio di scansione completa,
        distinto dal costo della ricerca nel B-tree.
        """
        grado = self.grado_minimo
        if self.radice is None:
            assert self.dimensione == 0, f"dimensione {self.dimensione} con radice assente"
            return
        assert self.dimensione >= 1, f"dimensione {self.dimensione} con radice presente"
        visitati = set()
        chiavi_viste = set()
        totale = [0]
        profondita_foglie = []

        def _visita(nodo, minimo, massimo, profondita):
            assert id(nodo) not in visitati, "nodo del B-tree raggiunto due volte"
            visitati.add(id(nodo))
            numero = len(nodo.voci)
            if nodo is self.radice:
                assert 1 <= numero <= 2 * grado - 1, (
                    f"radice del B-tree con {numero} voci fuori [1, {2 * grado - 1}]"
                )
            else:
                assert grado - 1 <= numero <= 2 * grado - 1, (
                    f"nodo del B-tree con {numero} voci fuori [{grado - 1}, {2 * grado - 1}]"
                )
            precedente = None
            for chiave, _dato in nodo.voci:
                assert type(chiave) is self.tipo_chiave, (
                    f"chiave {chiave!r} di tipo {type(chiave).__name__} nel B-tree"
                )
                assert chiave not in chiavi_viste, f"chiave {chiave!r} duplicata nel B-tree"
                chiavi_viste.add(chiave)
                if precedente is not None:
                    assert precedente < chiave, (
                        f"voci {precedente!r} e {chiave!r} non ordinate nel nodo del B-tree"
                    )
                precedente = chiave
                if minimo is not None:
                    assert minimo < chiave, (
                        f"chiave {chiave!r} sotto il limite {minimo!r} dell'antenato"
                    )
                if massimo is not None:
                    assert chiave < massimo, (
                        f"chiave {chiave!r} sopra il limite {massimo!r} dell'antenato"
                    )
                totale[0] += 1
            if nodo.e_foglia():
                profondita_foglie.append(profondita)
            else:
                assert len(nodo.figli) == numero + 1, (
                    f"nodo del B-tree con {numero} voci e {len(nodo.figli)} figli"
                )
                limiti = [minimo] + [voce[0] for voce in nodo.voci] + [massimo]
                for posizione, figlio in enumerate(nodo.figli):
                    assert isinstance(figlio, NodoBTree), (
                        "figlio del nodo del B-tree di tipo non atteso"
                    )
                    _visita(figlio, limiti[posizione], limiti[posizione + 1], profondita + 1)

        _visita(self.radice, None, None, 0)
        assert len(set(profondita_foglie)) == 1, (
            f"foglie del B-tree a profondità diverse: {sorted(set(profondita_foglie))}"
        )
        assert totale[0] == self.dimensione, (
            f"voci raggiunte {totale[0]} diverse dalla dimensione {self.dimensione}"
        )

    # -- Modifiche dal basso ----------------------------------------------

    def _dividi_eccedente(self, nodo):
        """Divide il nodo con `2t` voci e restituisce separatrice e destro.

        Il passo di divisione del nodo del B-tree sceglie la voce di indice
        `t - 1` come separatrice del nodo, conserva `t - 1` voci nel nodo
        sinistro del B-tree e `t` voci nel nodo destro del B-tree; per un nodo
        interno del B-tree i figli diventano rispettivamente `t` e `t + 1`. La
        scelta usa la mediana inferiore nell'elenco temporaneo di lunghezza
        pari. Il chiamante adotta la separatrice nel padre del nodo.
        """
        grado = self.grado_minimo
        separatrice = nodo.voci[grado - 1]
        destro = NodoBTree(nodo.voci[grado:], [])
        if not nodo.e_foglia():
            destro.figli = nodo.figli[grado:]
            nodo.figli = nodo.figli[:grado]
        nodo.voci = nodo.voci[: grado - 1]
        return separatrice, destro

    def _inserisci(self, nodo, chiave, dato):
        """Inserisce la coppia nel sottoalbero e segnala l'eventuale split.

        La voce entra nella foglia del B-tree selezionata dalla chiave; quando
        la foglia raggiunge temporaneamente `2t` voci, la divisione produce
        una separatrice e un nuovo figlio destro del nodo. Ogni padre del nodo
        adotta la separatrice ricevuta e, se diventa eccedente, si divide a
        sua volta. Il metodo restituisce `None` quando il sottoalbero resta
        stabile, altrimenti la coppia `(separatrice, destro)`. Una chiave già
        presente nel B-tree solleva `ValueError` senza modificare lo stato.
        """
        indice = self._posizione_locale(nodo.voci, chiave)
        if indice < len(nodo.voci) and nodo.voci[indice][0] == chiave:
            raise ValueError(f"chiave {chiave!r} già presente nel B-tree")
        if nodo.e_foglia():
            nodo.voci.insert(indice, (chiave, dato))
            if len(nodo.voci) == 2 * self.grado_minimo:
                return self._dividi_eccedente(nodo)
            return None
        esito = self._inserisci(nodo.figli[indice], chiave, dato)
        if esito is None:
            return None
        separatrice, destro = esito
        nodo.voci.insert(indice, separatrice)
        nodo.figli.insert(indice + 1, destro)
        if len(nodo.voci) == 2 * self.grado_minimo:
            return self._dividi_eccedente(nodo)
        return None

    def inserisci(self, chiave, dato):
        """Inserisce la coppia nel B-tree con divisioni dal basso.

        La voce entra nella foglia del B-tree selezionata dalla chiave; ogni
        nodo eccedente del B-tree viene diviso risalendo verso la radice del
        B-tree. La divisione della vecchia radice del B-tree crea una nuova
        radice con una separatrice e due figli. Una chiave già presente nel
        B-tree solleva `ValueError` e conserva lo stato del B-tree.
        """
        _valida_chiave(chiave, self.tipo_chiave)
        if self.radice is None:
            self.radice = NodoBTree([(chiave, dato)], [])
            self.dimensione += 1
            return
        esito = self._inserisci(self.radice, chiave, dato)
        if esito is not None:
            separatrice, destro = esito
            self.radice = NodoBTree([separatrice], [self.radice, destro])
        self.dimensione += 1

    def _prendi_predecessore(self, nodo):
        """Restituisce la coppia massima del sottoalbero del `nodo`."""
        corrente = nodo
        while not corrente.e_foglia():
            corrente = corrente.figli[-1]
        return corrente.voci[-1]

    def _ripara_se_carente(self, padre, indice_figlio):
        """Ripara il figlio del `padre` quando è temporaneamente carente.

        Un nodo carente del B-tree contiene temporaneamente `t - 2` voci. La
        riparazione del nodo prova il prestito dal fratello sinistro del nodo
        quando il fratello ha almeno `t` voci, poi dal fratello destro del
        nodo quando il fratello ha almeno `t` voci; altrimenti fonde il nodo
        con il fratello sinistro quando presente, oppure con il fratello
        destro. Nel prestito la voce separatrice del padre del nodo entra nel
        nodo carente e la voce estrema del fratello sostituisce la separatrice
        nel padre; per nodi interni del B-tree il prestito trasferisce anche
        un sottoalbero del fratello. Nella fusione il nodo risultante unisce
        il nodo carente, la voce separatrice del padre e il fratello,
        conservando l'ordine dei sottoalberi del B-tree. Un figlio stabile
        resta invariato.
        """
        grado = self.grado_minimo
        if indice_figlio >= len(padre.figli):
            return
        carente = padre.figli[indice_figlio]
        if len(carente.voci) != grado - 2:
            return
        if indice_figlio > 0 and len(padre.figli[indice_figlio - 1].voci) >= grado:
            fratello = padre.figli[indice_figlio - 1]
            carente.voci.insert(0, padre.voci[indice_figlio - 1])
            padre.voci[indice_figlio - 1] = fratello.voci.pop()
            if not fratello.e_foglia():
                carente.figli.insert(0, fratello.figli.pop())
            return
        if (
            indice_figlio < len(padre.figli) - 1
            and len(padre.figli[indice_figlio + 1].voci) >= grado
        ):
            fratello = padre.figli[indice_figlio + 1]
            carente.voci.append(padre.voci[indice_figlio])
            padre.voci[indice_figlio] = fratello.voci.pop(0)
            if not fratello.e_foglia():
                carente.figli.append(fratello.figli.pop(0))
            return
        if indice_figlio > 0:
            sinistro = padre.figli[indice_figlio - 1]
            sinistro.voci.append(padre.voci.pop(indice_figlio - 1))
            sinistro.voci.extend(carente.voci)
            if not carente.e_foglia():
                sinistro.figli.extend(carente.figli)
            del padre.figli[indice_figlio]
        else:
            destro = padre.figli[indice_figlio + 1]
            carente.voci.append(padre.voci.pop(indice_figlio))
            carente.voci.extend(destro.voci)
            if not carente.e_foglia():
                carente.figli.extend(destro.figli)
            del padre.figli[indice_figlio + 1]

    def _rimuovi(self, nodo, chiave):
        """Rimuove la `chiave` dal sottoalbero e ripara risalendo.

        La rimozione in una foglia del B-tree elimina direttamente la voce. La
        rimozione di una voce interna del B-tree la sostituisce con la coppia
        del predecessore e rimuove la coppia dalla sua posizione precedente
        nel B-tree. Dopo la ricorsione, il figlio visitato viene riparato
        quando è temporaneamente carente; l'eventuale carenza del nodo stesso
        viene riparata dal padre del nodo. Il metodo restituisce `True` quando
        la chiave era presente nel sottoalbero.
        """
        indice = self._posizione_locale(nodo.voci, chiave)
        presente = indice < len(nodo.voci) and nodo.voci[indice][0] == chiave
        if presente and nodo.e_foglia():
            del nodo.voci[indice]
            return True
        if presente:
            predecessore = self._prendi_predecessore(nodo.figli[indice])
            nodo.voci[indice] = predecessore
            trovato = self._rimuovi(nodo.figli[indice], predecessore[0])
            self._ripara_se_carente(nodo, indice)
            return trovato
        if nodo.e_foglia():
            return False
        trovato = self._rimuovi(nodo.figli[indice], chiave)
        self._ripara_se_carente(nodo, indice)
        return trovato

    def rimuovi(self, chiave):
        """Rimuove la `chiave` dal B-tree con riparazioni dal basso.

        La dimensione complessiva del B-tree diminuisce una sola volta. Quando
        la vecchia radice del B-tree resta vuota con un unico figlio, il figlio
        sostituisce la radice; quando resta vuota senza figli, il B-tree torna
        vuoto con altezza -1. Una chiave assente dal B-tree solleva `KeyError`
        e conserva lo stato nella variante dal basso adottata.
        """
        _valida_chiave(chiave, self.tipo_chiave)
        if self.radice is None:
            raise KeyError(chiave)
        if not self._rimuovi(self.radice, chiave):
            raise KeyError(chiave)
        self.dimensione -= 1
        if len(self.radice.voci) == 0:
            if self.radice.e_foglia():
                self.radice = None
            else:
                self.radice = self.radice.figli[0]
