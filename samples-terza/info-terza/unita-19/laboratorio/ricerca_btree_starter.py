"""Starter del laboratorio LAB-PY-U19 — ricerca nel B-tree e dossier comparativo.

Il modulo è deliberatamente incompleto. La rappresentazione dei nodi, il
contenitore con grado minimo, le modifiche dal basso, il controllo degli
invarianti, la strumentazione dei conteggi, i dati e i generatori delle
fixture sono già disponibili; i metodi marcati con `TODO` costituiscono il
lavoro dello studente. La suite `test_pubblici.py` fallisce all'inizio con
`NotImplementedError` nei punti di consultazione: gli errori attesi sono
parte del percorso e scompaiono con il completamento della fase L2.

Contratto del B-tree: grado minimo `t = 2`, chiavi di tipo esatto `int`
oppure `str` con tipo unico per istanza, unicità delle chiavi, occupazione
stabile da `t - 1` a `2t - 1` voci fuori radice, `k + 1` figli per un nodo
interno con `k` voci, foglie alla stessa profondità, `KeyError` per la chiave
assente, dimensione decrementata una sola volta per rimozione.

Contratto dell'indice: codici testuali non vuoti con zeri significativi,
costruzione che rifiuta i duplicati con `ValueError` senza consegnare una
struttura parziale, query che preservano la raccolta principale.

Ambiente: CPython sul computer, esecuzione con `uv run python
laboratorio/ricerca_btree_starter.py` dalla cartella `unita-19`.
"""

from __future__ import annotations


class NodoBTree:
    """Nodo del B-tree: voci `(chiave, dato)` ordinate e figli."""

    __slots__ = ("voci", "figli")

    def __init__(self, voci=None, figli=None):
        self.voci = list(voci) if voci else []
        self.figli = list(figli) if figli else []

    def e_foglia(self):
        """Restituisce `True` quando il nodo non ha figli."""
        return len(self.figli) == 0

    def chiavi(self):
        """Restituisce le chiavi del nodo in ordine."""
        return [chiave for chiave, _dato in self.voci]


class BTreeDidattico:
    """B-tree didattico con grado minimo 2 e chiavi di tipo unico."""

    def __init__(self, grado_minimo=2, tipo_chiave=int):
        if isinstance(grado_minimo, bool) or not isinstance(grado_minimo, int):
            raise TypeError("grado minimo atteso di tipo int")
        if grado_minimo < 2:
            raise ValueError("grado minimo atteso almeno 2")
        if tipo_chiave not in (int, str):
            raise ValueError("tipo_chiave atteso int o str")
        self.radice = None
        self.grado_minimo = grado_minimo
        self.tipo_chiave = tipo_chiave
        self.dimensione = 0

    def __len__(self):
        """Restituisce il numero di associazioni; 0 sul vuoto."""
        return self.dimensione

    def _valida(self, chiave):
        """Convalida la chiave contro il dominio della propria istanza."""
        if type(chiave) is not self.tipo_chiave:
            raise TypeError(f"chiave attesa di tipo {self.tipo_chiave.__name__}")

    @staticmethod
    def _posizione(voci, chiave):
        """Restituisce il primo indice con chiave almeno pari a `chiave`."""
        indice = 0
        while indice < len(voci) and voci[indice][0] < chiave:
            indice += 1
        return indice

    # --- lavoro dello studente: consultazione (fase L2) ------------------
    def cerca(self, chiave):
        """TODO (L2): restituisce il dato associato o solleva `KeyError`."""
        raise NotImplementedError("cerca da completare nella fase L2")

    def contiene(self, chiave):
        """TODO (L2): restituisce `True` se la chiave è presente."""
        raise NotImplementedError("contiene da completare nella fase L2")

    # --- rappresentazione e modifiche fornite (fasi L1, L3) ---------------
    def altezza(self):
        """Restituisce l'altezza in archi; -1 sul vuoto."""
        altezza = -1
        nodo = self.radice
        while nodo is not None:
            altezza += 1
            nodo = nodo.figli[0] if not nodo.e_foglia() else None
        return altezza

    def voci_ordinate(self):
        """Restituisce una nuova lista di coppie in ordine di chiave."""
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

    def ricerca_con_conteggi(self, chiave):
        """Strumentazione fornita: esito, percorso, nodi e confronti.

        Ogni confronto d'ordine fra la chiave richiesta e una chiave del nodo
        conta uno, compresa l'ultima valutazione falsa; ogni uguaglianza
        effettivamente eseguita conta uno. Lo strumento serve a verificare le
        previsioni della fase L2, non a sostituirle.
        """
        self._valida(chiave)
        percorso, nodi, ordine, uguaglianza = [], 0, 0, 0
        nodo = self.radice
        while nodo is not None:
            nodi += 1
            percorso.append(nodo.chiavi())
            indice = 0
            while indice < len(nodo.voci) and nodo.voci[indice][0] < chiave:
                ordine += 1
                indice += 1
            if indice < len(nodo.voci):
                ordine += 1
                uguaglianza += 1
                if nodo.voci[indice][0] == chiave:
                    return {
                        "trovato": True,
                        "dato": nodo.voci[indice][1],
                        "percorso": percorso,
                        "nodi": nodi,
                        "ordine": ordine,
                        "uguaglianza": uguaglianza,
                    }
            if nodo.e_foglia():
                return {
                    "trovato": False,
                    "dato": None,
                    "percorso": percorso,
                    "nodi": nodi,
                    "ordine": ordine,
                    "uguaglianza": uguaglianza,
                }
            nodo = nodo.figli[indice]
        return {
            "trovato": False,
            "dato": None,
            "percorso": percorso,
            "nodi": nodi,
            "ordine": ordine,
            "uguaglianza": uguaglianza,
        }

    def controlla_invarianti(self):
        """Verifica lo stato stabile; solleva `AssertionError` al difetto."""
        grado = self.grado_minimo
        if self.radice is None:
            assert self.dimensione == 0, "dimensione con radice assente"
            return
        visitati, chiavi_viste, totale, profondita = set(), set(), [0], []

        def _visita(nodo, minimo, massimo, livello):
            assert id(nodo) not in visitati, "nodo raggiunto due volte"
            visitati.add(id(nodo))
            numero = len(nodo.voci)
            if nodo is self.radice:
                assert 1 <= numero <= 2 * grado - 1, f"radice con {numero} voci"
            else:
                assert grado - 1 <= numero <= 2 * grado - 1, f"nodo con {numero} voci"
            precedente = None
            for chiave, _dato in nodo.voci:
                assert type(chiave) is self.tipo_chiave, f"chiave {chiave!r} fuori dominio"
                assert chiave not in chiavi_viste, f"chiave {chiave!r} duplicata"
                chiavi_viste.add(chiave)
                if precedente is not None:
                    assert precedente < chiave, "voci non ordinate nel nodo"
                precedente = chiave
                if minimo is not None:
                    assert minimo < chiave, f"chiave {chiave!r} sotto il limite dell'antenato"
                if massimo is not None:
                    assert chiave < massimo, f"chiave {chiave!r} sopra il limite dell'antenato"
                totale[0] += 1
            if nodo.e_foglia():
                profondita.append(livello)
            else:
                assert len(nodo.figli) == numero + 1, f"{numero} voci e {len(nodo.figli)} figli"
                limiti = [minimo] + [voce[0] for voce in nodo.voci] + [massimo]
                for posizione, figlio in enumerate(nodo.figli):
                    _visita(figlio, limiti[posizione], limiti[posizione + 1], livello + 1)

        _visita(self.radice, None, None, 0)
        assert len(set(profondita)) == 1, "foglie a profondità diverse"
        assert totale[0] == self.dimensione, "voci raggiunte diverse dalla dimensione"

    def _dividi(self, nodo):
        grado = self.grado_minimo
        separatrice = nodo.voci[grado - 1]
        destro = NodoBTree(nodo.voci[grado:], [])
        if not nodo.e_foglia():
            destro.figli = nodo.figli[grado:]
            nodo.figli = nodo.figli[:grado]
        nodo.voci = nodo.voci[: grado - 1]
        return separatrice, destro

    def _inserisci(self, nodo, chiave, dato):
        indice = self._posizione(nodo.voci, chiave)
        if indice < len(nodo.voci) and nodo.voci[indice][0] == chiave:
            raise ValueError(f"chiave {chiave!r} duplicata")
        if nodo.e_foglia():
            nodo.voci.insert(indice, (chiave, dato))
            if len(nodo.voci) == 2 * self.grado_minimo:
                return self._dividi(nodo)
            return None
        esito = self._inserisci(nodo.figli[indice], chiave, dato)
        if esito is None:
            return None
        separatrice, destro = esito
        nodo.voci.insert(indice, separatrice)
        nodo.figli.insert(indice + 1, destro)
        if len(nodo.voci) == 2 * self.grado_minimo:
            return self._dividi(nodo)
        return None

    def inserisci(self, chiave, dato):
        """Inserisce la coppia con divisioni dal basso; duplicato con `ValueError`."""
        self._valida(chiave)
        if self.radice is None:
            self.radice = NodoBTree([(chiave, dato)], [])
            self.dimensione += 1
            return
        esito = self._inserisci(self.radice, chiave, dato)
        if esito is not None:
            separatrice, destro = esito
            self.radice = NodoBTree([separatrice], [self.radice, destro])
        self.dimensione += 1

    def _predecessore(self, nodo):
        corrente = nodo
        while not corrente.e_foglia():
            corrente = corrente.figli[-1]
        return corrente.voci[-1]

    def _ripara(self, padre, indice):
        grado = self.grado_minimo
        if indice >= len(padre.figli):
            return
        carente = padre.figli[indice]
        if len(carente.voci) != grado - 2:
            return
        if indice > 0 and len(padre.figli[indice - 1].voci) >= grado:
            fratello = padre.figli[indice - 1]
            carente.voci.insert(0, padre.voci[indice - 1])
            padre.voci[indice - 1] = fratello.voci.pop()
            if not fratello.e_foglia():
                carente.figli.insert(0, fratello.figli.pop())
            return
        if indice < len(padre.figli) - 1 and len(padre.figli[indice + 1].voci) >= grado:
            fratello = padre.figli[indice + 1]
            carente.voci.append(padre.voci[indice])
            padre.voci[indice] = fratello.voci.pop(0)
            if not fratello.e_foglia():
                carente.figli.append(fratello.figli.pop(0))
            return
        if indice > 0:
            sinistro = padre.figli[indice - 1]
            sinistro.voci.append(padre.voci.pop(indice - 1))
            sinistro.voci.extend(carente.voci)
            if not carente.e_foglia():
                sinistro.figli.extend(carente.figli)
            del padre.figli[indice]
        else:
            destro = padre.figli[indice + 1]
            carente.voci.append(padre.voci.pop(indice))
            carente.voci.extend(destro.voci)
            if not carente.e_foglia():
                carente.figli.extend(destro.figli)
            del padre.figli[indice + 1]

    def _rimuovi(self, nodo, chiave):
        indice = self._posizione(nodo.voci, chiave)
        presente = indice < len(nodo.voci) and nodo.voci[indice][0] == chiave
        if presente and nodo.e_foglia():
            del nodo.voci[indice]
            return True
        if presente:
            predecessore = self._predecessore(nodo.figli[indice])
            nodo.voci[indice] = predecessore
            trovato = self._rimuovi(nodo.figli[indice], predecessore[0])
            self._ripara(nodo, indice)
            return trovato
        if nodo.e_foglia():
            return False
        trovato = self._rimuovi(nodo.figli[indice], chiave)
        self._ripara(nodo, indice)
        return trovato

    def rimuovi(self, chiave):
        """Rimuove la chiave con riparazioni dal basso; assente con `KeyError`."""
        self._valida(chiave)
        if self.radice is None:
            raise KeyError(chiave)
        if not self._rimuovi(self.radice, chiave):
            raise KeyError(chiave)
        self.dimensione -= 1
        if len(self.radice.voci) == 0:
            self.radice = None if self.radice.e_foglia() else self.radice.figli[0]


def _foglia(coppie):
    """Restituisce una foglia con le coppie ordinate date."""
    return NodoBTree(list(coppie), [])


def costruisci_d1():
    """Costruisce D1: radice `[10 | 20]` e otto associazioni, altezza 1."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        [(10, "dato-10"), (20, "dato-20")],
        [
            _foglia([(5, "dato-5"), (6, "dato-6"), (7, "dato-7")]),
            _foglia([(12, "dato-12"), (17, "dato-17")]),
            _foglia([(30, "dato-30")]),
        ],
    )
    albero.dimensione = 8
    return albero


def costruisci_d2():
    """Costruisce D2 con gli inserimenti `1..10`: dieci voci, altezza 2."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    for chiave in range(1, 11):
        albero.inserisci(chiave, f"dato-{chiave}")
    return albero


def costruisci_prestito_destro():
    """Stato D3b: radice `[20]`, foglie `[5]` e `[25, 30]`."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        [(20, "dato-20")], [_foglia([(5, "dato-5")]), _foglia([(25, "dato-25"), (30, "dato-30")])]
    )
    albero.dimensione = 4
    return albero


def costruisci_prestito_sinistro():
    """Stato D3c: radice `[20]`, foglie `[5, 10]` e `[25]`."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        [(20, "dato-20")], [_foglia([(5, "dato-5"), (10, "dato-10")]), _foglia([(25, "dato-25")])]
    )
    albero.dimensione = 4
    return albero


def costruisci_fusione_radice():
    """Stato D3e: radice `[10]`, foglie `[5]` e `[15]`."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        [(10, "dato-10")], [_foglia([(5, "dato-5")]), _foglia([(15, "dato-15")])]
    )
    albero.dimensione = 3
    return albero


def costruisci_d4():
    """Stato D4: radice `[40]`, altezza 2, sette chiavi."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    sinistro = NodoBTree(
        [(20, "dato-20")], [_foglia([(10, "dato-10")]), _foglia([(30, "dato-30")])]
    )
    destro = NodoBTree([(60, "dato-60")], [_foglia([(50, "dato-50")]), _foglia([(70, "dato-70")])])
    albero.radice = NodoBTree([(40, "dato-40")], [sinistro, destro])
    albero.dimensione = 7
    return albero


def costruisci_d5():
    """Stato D5: radice `[40]`, altezza 2, prestito interno atteso."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    sinistro = NodoBTree(
        [(20, "dato-20"), (30, "dato-30")],
        [_foglia([(10, "dato-10")]), _foglia([(25, "dato-25")]), _foglia([(35, "dato-35")])],
    )
    destro = NodoBTree([(60, "dato-60")], [_foglia([(50, "dato-50")]), _foglia([(70, "dato-70")])])
    albero.radice = NodoBTree([(40, "dato-40")], [sinistro, destro])
    albero.dimensione = 9
    return albero


def fixture_foglie_diverse():
    """Fixture corrotta: foglie a profondità diverse con nodi localmente validi.

    La radice `[20]` ha la foglia `[10]` a profondità 1 e il nodo interno
    `[30]` con foglie `[25]`, `[35]` a profondità 2: occupazione e numero di
    figli sono regolari, la profondità delle foglie no.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    destro = NodoBTree([(30, "dato-30")], [_foglia([(25, "dato-25")]), _foglia([(35, "dato-35")])])
    albero.radice = NodoBTree([(20, "dato-20")], [_foglia([(10, "dato-10")]), destro])
    albero.dimensione = 5
    return albero


def fixture_limite_antentato():
    """Fixture corrotta: discendente fuori dal limite dell'antenato.

    La foglia sinistra del B-tree contiene `25`, oltre la separatrice `10`
    della radice del B-tree: localmente ordinata, globalmente incoerente.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        [(10, "dato-10"), (20, "dato-20")],
        [
            _foglia([(5, "dato-5"), (25, "dato-25")]),
            _foglia([(12, "dato-12"), (17, "dato-17")]),
            _foglia([(30, "dato-30")]),
        ],
    )
    albero.dimensione = 8
    return albero


if __name__ == "__main__":
    albero = costruisci_d1()
    albero.controlla_invarianti()
    print("D1 pronto: radice", albero.radice.chiavi(), "altezza", albero.altezza())
    print("completare cerca e contiene (fase L2) per superare la suite iniziale")
