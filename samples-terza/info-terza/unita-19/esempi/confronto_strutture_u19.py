"""Confronto riproducibile delle strutture di ricerca — Unità 19 (cap. PY-36).

Il modulo definisce adattatori con risultati confrontabili per lista non
ordinata, lista ordinata con `bisect`, albero binario di ricerca minimale,
B-tree didattico e `dict` di Python: ogni adattatore espone `cerca`,
`contiene` e `voci_ordinate` con lo stesso dominio, lo stesso ordine e gli
stessi record restituiti. Il `dict` reale offre verifica e misure temporali;
i contatori interni appartengono ai modelli didattici, perché l'API pubblica
di `dict` ha un diverso perimetro di osservazione.

La rappresentazione BST del modulo è minimale e serve al confronto: il
trattamento completo dell'albero binario di ricerca, con cancellazione e
verifica degli invarianti, appartiene all'Unità 17. Le cancellazioni del
B-tree nel dossier sono simulazioni o ricostruzioni: una ricostruzione
dell'indice ha il proprio costo e porta il nome `ricostruzione` nel CSV.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

import bisect
import csv
import random
import statistics
import time

from btree_costruzione_u19 import costruisci_btree_riferimento


class AdattatoreLista:
    """Ricerca lineare su coppie con conteggio dei confronti di uguaglianza."""

    nome = "lista"

    def __init__(self, voci):
        self.coppie = list(voci)
        self.ultimi_confronti = 0

    def cerca(self, chiave):
        """Restituisce il dato della `chiave` o solleva `KeyError`."""
        confronti = 0
        for candidata, dato in self.coppie:
            confronti += 1
            if candidata == chiave:
                self.ultimi_confronti = confronti
                return dato
        self.ultimi_confronti = confronti
        raise KeyError(chiave)

    def contiene(self, chiave):
        """Restituisce `True` quando la `chiave` è fra le coppie."""
        try:
            self.cerca(chiave)
            return True
        except KeyError:
            return False

    def voci_ordinate(self):
        """Restituisce le coppie in ordine crescente di chiave."""
        return sorted(self.coppie, key=lambda voce: voce[0])


class AdattatoreListaOrdinata:
    """Ricerca dicotomica con `bisect` e conteggio dei confronti locali."""

    nome = "lista-ordinata"

    def __init__(self, voci):
        self.coppie = sorted(voci, key=lambda voce: voce[0])
        self.chiavi = [chiave for chiave, _dato in self.coppie]
        self.ultimi_confronti = 0

    def cerca(self, chiave):
        """Restituisce il dato della `chiave` o solleva `KeyError`."""
        posizione = bisect.bisect_left(self.chiavi, chiave)
        self.ultimi_confronti = max(1, posizione.bit_length())
        if posizione < len(self.chiavi) and self.chiavi[posizione] == chiave:
            return self.coppie[posizione][1]
        raise KeyError(chiave)

    def contiene(self, chiave):
        """Restituisce `True` quando la `chiave` è fra le coppie."""
        try:
            self.cerca(chiave)
            return True
        except KeyError:
            return False

    def voci_ordinate(self):
        """Restituisce le coppie in ordine crescente di chiave."""
        return list(self.coppie)


class _NodoBST:
    """Nodo minimale dell'albero binario di ricerca del confronto."""

    __slots__ = ("chiave", "dato", "sinistro", "destro")

    def __init__(self, chiave, dato):
        self.chiave = chiave
        self.dato = dato
        self.sinistro = None
        self.destro = None


class AdattatoreBST:
    """Albero binario di ricerca minimale con conteggio dei nodi esaminati."""

    nome = "bst"

    def __init__(self, voci):
        self.radice = None
        self.ultimi_nodi = 0
        for chiave, dato in voci:
            self._inserisci(chiave, dato)

    def _inserisci(self, chiave, dato):
        """Inserisce la coppia senza ribilanciamento; duplicato con `ValueError`."""
        if self.radice is None:
            self.radice = _NodoBST(chiave, dato)
            return
        corrente = self.radice
        while True:
            if chiave == corrente.chiave:
                raise ValueError(f"chiave {chiave!r} duplicata")
            if chiave < corrente.chiave:
                if corrente.sinistro is None:
                    corrente.sinistro = _NodoBST(chiave, dato)
                    return
                corrente = corrente.sinistro
            else:
                if corrente.destro is None:
                    corrente.destro = _NodoBST(chiave, dato)
                    return
                corrente = corrente.destro

    def cerca(self, chiave):
        """Restituisce il dato della `chiave` o solleva `KeyError`."""
        nodi = 0
        corrente = self.radice
        while corrente is not None:
            nodi += 1
            if chiave == corrente.chiave:
                self.ultimi_nodi = nodi
                return corrente.dato
            corrente = corrente.sinistro if chiave < corrente.chiave else corrente.destro
        self.ultimi_nodi = nodi
        raise KeyError(chiave)

    def contiene(self, chiave):
        """Restituisce `True` quando la `chiave` è nell'albero."""
        try:
            self.cerca(chiave)
            return True
        except KeyError:
            return False

    def voci_ordinate(self):
        """Restituisce le coppie in ordine crescente di chiave."""
        risultato = []
        pila = []
        corrente = self.radice
        while pila or corrente is not None:
            while corrente is not None:
                pila.append(corrente)
                corrente = corrente.sinistro
            corrente = pila.pop()
            risultato.append((corrente.chiave, corrente.dato))
            corrente = corrente.destro
        return risultato


class AdattatoreBTree:
    """B-tree didattico con conteggi di nodi e confronti fra chiavi."""

    nome = "b-tree"

    def __init__(self, voci, grado_minimo=2, tipo_chiave=None):
        voci = list(voci)
        if tipo_chiave is None:
            tipo_chiave = type(voci[0][0]) if voci else int
        self.indice = costruisci_btree_riferimento(
            voci, grado_minimo=grado_minimo, tipo_chiave=tipo_chiave
        )
        self.ultimo_esito = None

    def cerca(self, chiave):
        """Restituisce il dato della `chiave` o solleva `KeyError`."""
        self.ultimo_esito = self.indice.ricerca_con_conteggi(chiave)
        if not self.ultimo_esito.trovato:
            raise KeyError(chiave)
        return self.ultimo_esito.dato

    def contiene(self, chiave):
        """Restituisce `True` quando la `chiave` è nel B-tree."""
        return self.indice.contiene(chiave)

    def voci_ordinate(self):
        """Restituisce le coppie in ordine crescente di chiave."""
        return self.indice.voci_ordinate()


class AdattatoreDict:
    """Dizionario nativo come oracolo di verifica e riferimento temporale."""

    nome = "dict"

    def __init__(self, voci):
        self.tabella = dict(voci)

    def cerca(self, chiave):
        """Restituisce il dato della `chiave` o solleva `KeyError`."""
        return self.tabella[chiave]

    def contiene(self, chiave):
        """Restituisce `True` quando la `chiave` è nel dizionario."""
        return chiave in self.tabella

    def voci_ordinate(self):
        """Restituisce le coppie in ordine crescente di chiave."""
        return sorted(self.tabella.items(), key=lambda voce: voce[0])


#: Costruttori degli adattatori nell'ordine di presentazione del capitolo.
ADATTATORI = (
    AdattatoreLista,
    AdattatoreListaOrdinata,
    AdattatoreBST,
    AdattatoreBTree,
    AdattatoreDict,
)


def genera_interi(quantita, famiglia="crescenti", seme=19):
    """Genera `quantita` coppie con chiavi intere uniche della `famiglia`.

    Le famiglie sono `crescenti`, `inversi` e `mescolati` con `random.Random`
    e seme registrato; il dato della chiave `x` è `f"dato-{x}"`. La stessa
    chiamata produce lo stesso dataset.
    """
    chiavi = list(range(1, quantita + 1))
    if famiglia == "inversi":
        chiavi.reverse()
    elif famiglia == "mescolati":
        random.Random(seme).shuffle(chiavi)
    elif famiglia != "crescenti":
        raise ValueError(f"famiglia sconosciuta: {famiglia!r}")
    return [(chiave, f"dato-{chiave}") for chiave in chiavi]


def query_campione(voci):
    """Restituisce query riuscite e fallite per le voci date.

    Le query riuscite coprono primo, centro e ultimo della sequenza ordinata;
    le query fallite coprono sotto il minimo, sopra il massimo e un valore
    intermedio assente. Le sorgenti canoniche hanno chiavi uniche; il
    duplicato è un caso d'errore indipendente.
    """
    chiavi = sorted(chiave for chiave, _dato in voci)
    sotto = chiavi[0] - 1
    sopra = chiavi[-1] + 1
    buco = next(
        (
            candidato
            for candidato in range(chiavi[0] + 1, chiavi[-1])
            if candidato not in set(chiavi)
        ),
        sopra + 1,
    )
    return {
        "riuscite": [chiavi[0], chiavi[len(chiavi) // 2], chiavi[-1]],
        "fallite": [sotto, sopra, buco],
    }


def _metrica(adattatore, query):
    """Esegue la query e restituisce esito e metrica con unità dichiarata."""
    try:
        dato = adattatore.cerca(query)
        esito = f"trovato:{dato!r}"
    except KeyError:
        esito = "assente"
    if isinstance(adattatore, AdattatoreBTree) and adattatore.ultimo_esito is not None:
        metrica = (
            f"nodi={adattatore.ultimo_esito.nodi} confronti={adattatore.ultimo_esito.confronti}"
        )
    elif isinstance(adattatore, AdattatoreBST):
        metrica = f"nodi={adattatore.ultimi_nodi}"
    elif isinstance(adattatore, (AdattatoreLista, AdattatoreListaOrdinata)):
        metrica = f"confronti={adattatore.ultimi_confronti}"
    else:
        metrica = "oracolo"
    return esito, metrica


def esegui_confronto(voci, query, adattatori=ADATTATORI):
    """Esegue le stesse query sugli adattatori e verifica l'equivalenza.

    La funzione costruisce ogni indice fuori dalle misure, verifica le query
    esatte contro `dict` e gli intervalli contro `sorted` con filtro, poi
    registra esiti e metriche con unità. Restituisce il dizionario con
    `righe` (una per coppia struttura-query), `coerente` (esiti identici per
    ogni query) e `preparazione` (nomi delle strutture costruite). La stampa,
    i file e la generazione dei dati restano fuori dalle regioni misurate.
    """
    istanze = [costruttore(list(voci)) for costruttore in adattatori]
    oracolo = {chiave: dato for chiave, dato in voci}
    righe = []
    coerente = True
    for domanda in query:
        atteso = f"trovato:{oracolo[domanda]!r}" if domanda in oracolo else "assente"
        for istanza in istanze:
            esito, metrica = _metrica(istanza, domanda)
            if esito != atteso:
                coerente = False
            righe.append(
                {
                    "struttura": istanza.nome,
                    "query": domanda,
                    "atteso": atteso,
                    "esito": esito,
                    "metrica": metrica,
                    "coerente": esito == atteso,
                }
            )
    return {
        "righe": righe,
        "coerente": coerente,
        "preparazione": [istanza.nome for istanza in istanze],
    }


def misura_tempi(voci, query, adattatori=ADATTATORI, ripetizioni=5):
    """Misura la durata delle query con interprete e aggregazione dichiarati.

    La costruzione degli indici e la stampa restano fuori dalla regione
    cronometrata; ogni struttura esegue la lista completa delle query per il
    numero di ripetizioni indicato e la misura registrata è la mediana delle
    durate in secondi. Restituisce il dizionario `{nome: secondi}`.
    """
    istanze = [costruttore(list(voci)) for costruttore in adattatori]
    tempi = {}
    for istanza in istanze:
        durate = []
        for _conto in range(ripetizioni):
            inizio = time.perf_counter()
            for domanda in query:
                try:
                    istanza.cerca(domanda)
                except KeyError:
                    pass
            durate.append(time.perf_counter() - inizio)
        tempi[istanza.nome] = statistics.median(durate)
    return tempi


def salva_csv(righe, percorso):
    """Salva le righe del confronto in CSV con colonne e unità fissate."""
    with open(percorso, "w", newline="", encoding="utf-8") as archivio:
        scrittore = csv.DictWriter(
            archivio, fieldnames=["struttura", "query", "atteso", "esito", "metrica", "coerente"]
        )
        scrittore.writeheader()
        scrittore.writerows(righe)
