"""Operazioni sulle collezioni dell'Unità 8: dizionari e insiemi in azione.

Collocare il file in `programmi/operazioni_collezioni_u8.py` della raccolta
dello studente. Il modulo raccoglie le PROVE corrette delle API di `dict` e
di `set` sui due dataset canonici del capitolo PY-12: le scorte per i
dizionari, la coppia di insiemi A/B per le operazioni fra insiemi.

Modello ricordato: un dizionario è un mapping MUTABILE di associazioni
chiave -> valore, con chiavi uniche e con l'ordine di inserimento
conservato; un insieme è una raccolta MUTABILE di elementi hashable unici,
senza indice e senza ordinamento. Ogni funzione `prova_...` costruisce il
proprio stato di partenza, esegue le operazioni e RESTITUISCE l'evidenza
osservata invece di stamparla, così che la stessa prova sia riusabile dai
test. Nessuna funzione modifica i valori di modulo: le prove partono da una
copia oppure da un letterale.

GLI ERRORI INTENZIONALI SONO ISOLATI nelle funzioni `demo_errore_...`, che
sollevano davvero l'eccezione documentata. Non vengono richiamate dalla
demo ordinaria e sono richiamabili a parte, una alla volta, per osservare
il tipo di errore e l'operazione che lo produce.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/operazioni_collezioni_u8.py
"""

SCORTE_INIZIALI = {"R10": 12, "L05": 4}

A_INSIEME = {"A", "B", "C"}

B_INSIEME = {"B", "D"}

REGISTRO_INIZIALE = {"S1": [20, 21]}


# ---------------------------------------------------------------------------
# Dizionari — chiavi, valori e ordine di inserimento
# ---------------------------------------------------------------------------


def prova_chiave_e_valore() -> tuple[bool, bool]:
    """Restituisce i due esiti di appartenenza sulla chiave e sul valore.

    Usa `SCORTE_INIZIALI` come dataset di partenza e restituisce la tupla
    `("R10" in scorte, 12 in scorte)`. L'operatore `in` applicato a un
    dizionario interroga le CHIAVI e non i valori: il primo esito è `True`
    perché "R10" è una chiave, il secondo è `False` perché 12 è un valore e
    non compare mai fra le chiavi. Nessuno dei due argomenti viene inserito.
    """
    scorte = dict(SCORTE_INIZIALI)
    return ("R10" in scorte, 12 in scorte)


def prova_aggiornamento_e_ordine() -> tuple[int, list[str]]:
    """Restituisce lunghezza e ordine delle chiavi dopo l'aggiornamento di R10.

    Parte da `SCORTE_INIZIALI`, assegna `scorte["R10"] = 15` e restituisce
    `(len(scorte), list(scorte))`. Aggiornare una chiave ESISTENTE non
    aggiunge associazioni e non cambia la posizione della chiave: la
    lunghezza resta 2 e l'ordine resta R10, L05. L'ordine di inserimento è
    distinto dall'ordinamento alfabetico o numerico dei valori.
    """
    scorte = dict(SCORTE_INIZIALI)
    scorte["R10"] = 15
    return (len(scorte), list(scorte))


def prova_zero_lecito() -> tuple[int, bool, int]:
    """Restituisce gli effetti dell'aggiunta di C20 con quantità zero.

    Parte da `SCORTE_INIZIALI`, esegue `scorte["C20"] = 0` e restituisce
    `(len(scorte), "C20" in scorte, scorte["C20"])`. Lo zero è un VALORE
    lecito: l'associazione viene creata, la lunghezza diventa 3 e il valore
    memorizzato è 0. Nessun valore è riservato per indicare l'assenza.
    """
    scorte = dict(SCORTE_INIZIALI)
    scorte["C20"] = 0
    return (len(scorte), "C20" in scorte, scorte["C20"])


def prova_get_con_default() -> tuple[int, bool]:
    """Restituisce il risultato di `get` con default e lo stato della chiave.

    Parte da `SCORTE_INIZIALI` e restituisce
    `(scorte.get("X99", 0), "X99" in scorte)`. Il metodo `get` legge senza
    inserire: per la chiave assente restituisce il default 0 e il dizionario
    resta di due associazioni, con "X99" ancora assente. Il default serve a
    produrre un risultato di lavoro, non a registrare l'associazione.
    """
    scorte = dict(SCORTE_INIZIALI)
    return (scorte.get("X99", 0), "X99" in scorte)


def prova_setdefault_su_presente() -> tuple[int, int, int]:
    """Restituisce il ritorno di `setdefault` e il valore conservato.

    Parte da `SCORTE_INIZIALI`, aggiunge C20 con quantità 0, esegue
    `valore = scorte.setdefault("C20", 9)` e restituisce
    `(valore, scorte["C20"], len(scorte))`. `setdefault` restituisce il
    valore ESISTENTE senza sostituirlo: tutti e tre gli elementi della
    tupla riportano 0 e la lunghezza resta 3. Il secondo argomento viene
    usato soltanto quando la chiave è assente.
    """
    scorte = dict(SCORTE_INIZIALI)
    scorte["C20"] = 0
    valore = scorte.setdefault("C20", 9)
    return (valore, scorte["C20"], len(scorte))


def prova_setdefault_su_assente() -> tuple[int, dict[str, int]]:
    """Restituisce il ritorno di `setdefault` su assente e il dizionario dopo.

    Parte da `SCORTE_INIZIALI`, esegue `valore = scorte.setdefault("C20", 9)`
    e restituisce `(valore, scorte)`. La chiave era assente: `setdefault`
    INSERISCE `("C20", 9)` in fondo e restituisce il default 9, che è anche
    il valore memorizzato. Il ritorno del metodo copre entrambi i casi con
    una sola operazione.
    """
    scorte = dict(SCORTE_INIZIALI)
    valore = scorte.setdefault("C20", 9)
    return (valore, scorte)


def prova_popitem_ultima_inserita() -> tuple[tuple[str, int], list[str]]:
    """Restituisce la coppia tolta da `popitem` e le chiavi rimaste.

    Costruisce `{"R10": 12, "L05": 4, "C20": 0}` ed esegue
    `coppia = scorte.popitem()`. Il metodo rimuove e restituisce una coppia
    `(chiave, valore)` sotto forma di tupla: l'ULTIMA chiave inserita ancora
    presente, non una scelta casuale. Il risultato è
    `(("C20", 0), ["R10", "L05"])`. Su un dizionario vuoto `popitem` solleva
    `KeyError`: il caso è isolato in `demo_errore_popitem_vuoto`.
    """
    scorte = {"R10": 12, "L05": 4, "C20": 0}
    coppia = scorte.popitem()
    return (coppia, list(scorte))


def prova_cancella_e_reinserisci() -> list[str]:
    """Restituisce l'ordine delle chiavi dopo cancellazione e reinserimento.

    Parte da `SCORTE_INIZIALI`, esegue `del scorte["R10"]` e poi
    `scorte["R10"] = 12`. La cancellazione toglie l'associazione; il
    reinserimento la crea di nuovo e la sposta in FONDO. La lista delle
    chiavi restituita è quindi `["L05", "R10"]`, diversa dall'ordine di
    partenza R10, L05. Aggiornare un valore non produce questo effetto.
    """
    scorte = dict(SCORTE_INIZIALI)
    del scorte["R10"]
    scorte["R10"] = 12
    return list(scorte)


def prova_none_non_e_assenza() -> tuple[bool, bool, bool, bool]:
    """Restituisce quattro esiti per distinguere `None` da assente.

    Confronta `{"A": None}` e `{}` e restituisce la tupla
    `(get_su_none_is_none, get_su_vuoto_is_none, "A" in con_none, "A" in vuoto)`,
    che vale `(True, True, True, False)`. Il metodo `get` restituisce `None`
    in entrambi i casi e quindi non basta a distinguerli: il test di
    appartenenza risponde invece senza ambiguità. Per lo stesso motivo 0,
    `False` e la lista vuota non indicano automaticamente l'assenza, perché
    sono valori leciti. Il valore `None` resta un valore come gli altri.
    """
    con_none = {"A": None}
    vuoto = {}
    return (
        con_none.get("A") is None,
        vuoto.get("A") is None,
        "A" in con_none,
        "A" in vuoto,
    )


def prova_vista_e_fotografia() -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    """Restituisce la vista e la fotografia dopo le modifiche del dizionario.

    Costruisce le scorte di partenza, acquisisce `vista = scorte.items()` e
    `fotografia = list(scorte.items())`, poi aggiorna R10 a 15 e aggiunge
    C20 con 0. Restituisce `(list(vista), fotografia)`, i due contenuti
    dopo le modifiche.

    La vista è un oggetto CHE OSSERVA il dizionario: le modifiche successive
    compaiono nel suo contenuto. La lista della fotografia è stata costruita
    in quel momento e conserva le associazioni di allora. La fotografia non
    copia però profondamente i valori: se un valore fosse una lista mutabile
    resterebbe condiviso.
    """
    scorte = dict(SCORTE_INIZIALI)
    vista = scorte.items()
    fotografia = list(scorte.items())
    scorte["R10"] = 15
    scorte["C20"] = 0
    return (list(vista), fotografia)


def prova_copia_superficiale() -> tuple[list[int], list[int], list[int], list[int]]:
    """Restituisce quattro fotografie del registro e della sua copia.

    Usa `registro = {"S1": [20, 21]}` e `copia = registro.copy()`, poi
    esegue `copia["S1"].append(22)` e infine assegna una lista nuova con
    `copia["S1"] = [99]`. Restituisce
    `(registro_dopo_append, copia_dopo_append, registro_dopo_sostituzione,
    copia_dopo_sostituzione)`, che valgono
    `([20, 21, 22], [20, 21, 22], [20, 21, 22], [99])`.

    `copy` produce un dizionario NUOVO con le stesse associazioni, ma i
    valori restano gli stessi oggetti: l'append sulla lista della copia è
    quindi osservato anche dal registro. Assegnare una lista NUOVA a
    `copia["S1"]` sostituisce solo l'associazione della copia. Questa è una
    copia SUPERFICIALE e non un'indipendenza completa dei due registri.
    """
    registro = {"S1": [20, 21]}
    copia = registro.copy()
    copia["S1"].append(22)
    dopo_append_registro = list(registro["S1"])
    dopo_append_copia = list(copia["S1"])
    copia["S1"] = [99]
    dopo_sostituzione_registro = list(registro["S1"])
    dopo_sostituzione_copia = list(copia["S1"])
    return (
        dopo_append_registro,
        dopo_append_copia,
        dopo_sostituzione_registro,
        dopo_sostituzione_copia,
    )


# ---------------------------------------------------------------------------
# Dizionari — ritorni ed effetti delle API di aggiornamento e rimozione
# ---------------------------------------------------------------------------


def prova_ritorno_di_update() -> tuple[bool, dict[str, int]]:
    """Restituisce il ritorno di `update` e il dizionario aggiornato.

    Parte da `SCORTE_INIZIALI`, esegue
    `esito = scorte.update({"R10": 15, "C20": 0})` e restituisce
    `(esito is None, scorte)`. Il metodo modifica il dizionario e
    restituisce `None`: il risultato dell'operazione è il dizionario
    aggiornato, che si osserva attraverso il nome `scorte`. Le chiavi già
    presenti vengono aggiornate, quelle assenti vengono inserite in fondo.
    """
    scorte = dict(SCORTE_INIZIALI)
    esito = scorte.update({"R10": 15, "C20": 0})
    return (esito is None, scorte)


def prova_ritorno_di_clear() -> tuple[bool, dict[str, int]]:
    """Restituisce il ritorno di `clear` e il dizionario svuotato.

    Parte da `SCORTE_INIZIALI`, esegue `esito = scorte.clear()` e restituisce
    `(esito is None, scorte)`. Il metodo rimuove tutte le associazioni e
    restituisce `None`; il risultato è il dizionario stesso, che risulta
    vuoto ma è sempre lo stesso oggetto.
    """
    scorte = dict(SCORTE_INIZIALI)
    esito = scorte.clear()
    return (esito is None, scorte)


def prova_pop_con_default() -> tuple[int, int, int]:
    """Restituisce i ritorni di `pop` con default, presente e assente.

    Parte da `SCORTE_INIZIALI` e restituisce
    `(tolto, sostitutivo, len(scorte))` dopo `tolto = scorte.pop("R10")` e
    `sostitutivo = scorte.pop("X99", 0)`. Il valore tolto è 12 e l'intera
    associazione viene rimossa; per la chiave assente il default 0 viene
    restituito senza inserire nulla e la lunghezza finale è 1.
    """
    scorte = dict(SCORTE_INIZIALI)
    tolto = scorte.pop("R10")
    sostitutivo = scorte.pop("X99", 0)
    return (tolto, sostitutivo, len(scorte))


def prova_popitem_e_ordine_rimanente() -> tuple[bool, bool]:
    """Restituisce due esiti di corrispondenza fra `popitem` e ordine.

    Costruisce `{"R10": 12, "L05": 4, "C20": 0}`, estrae con `popitem` e
    restituisce `(coppia == ("C20", 0), list(scorte) == ["R10", "L05"])`.
    La coppia estratta corrisponde all'ultima chiave inserita e le chiavi
    rimaste conservano il proprio ordine. L'uguaglianza dei dizionari non
    dipende invece dall'ordine: due dizionari con le stesse associazioni in
    ordine diverso sono uguali, mentre `list(d)` mostra l'ordine effettivo.
    """
    scorte = {"R10": 12, "L05": 4, "C20": 0}
    coppia = scorte.popitem()
    return (coppia == ("C20", 0), list(scorte) == ["R10", "L05"])


# ---------------------------------------------------------------------------
# Dizionari — chiavi ammesse e chiavi rifiutate (hashability)
# ---------------------------------------------------------------------------


def prova_chiavi_ammesse() -> dict:
    """Restituisce un dizionario costruito con tre chiavi ammesse.

    Le chiavi devono essere HASHABLE, cioè con hash stabile e confronto
    coerente. Stringhe, interi e tuple di elementi hashable sono ammesse e
    convivono nello stesso dizionario: la tupla `(1, 2)` è una chiave
    diversa dalla stringa `"(1, 2)"` e dall'intero 1. L'hash è un meccanismo
    interno e i suoi valori numerici non sono attesi portabili: non vanno
    usati come identificatori da confrontare fra programmi.
    """
    chiavi = {"testo": 1, 7: 2, (1, 2): 3}
    return chiavi


# ---------------------------------------------------------------------------
# Errori intenzionali isolati: nessuna di queste funzioni è richiamata dalla
# demo ordinaria. Ciascuna solleva l'eccezione documentata, da osservare una
# alla volta.
# ---------------------------------------------------------------------------


def demo_errore_accesso_assente() -> None:
    """Solleva `KeyError`: accesso diretto a una chiave assente.

    L'istruzione `scorte["X99"]` cerca la chiave "X99", non la trova e
    interrompe il programma con `KeyError: 'X99'`. Il messaggio riporta la
    chiave mancante. Per leggere senza rischiare ci si avvale di `get`, del
    test di appartenenza oppure di un controllo esplicito.
    """
    scorte = dict(SCORTE_INIZIALI)
    scorte["X99"]


def demo_errore_pop_senza_default() -> None:
    """Solleva `KeyError`: `pop` di una chiave assente senza default.

    L'istruzione `scorte.pop("X99")` senza secondo argomento chiede di
    rimuovere una chiave assente e restituire il valore tolto: non essendoci
    nulla da restituire, il programma si interrompe con `KeyError`. Il
    default, se fornito, sostituisce il valore di ritorno e non viene
    memorizzato.
    """
    scorte = dict(SCORTE_INIZIALI)
    scorte.pop("X99")


def demo_errore_popitem_vuoto() -> None:
    """Solleva `KeyError`: `popitem` su un dizionario vuoto.

    L'istruzione `{}.popitem()` non ha alcuna coppia da rimuovere e
    restituire: il programma si interrompe con `KeyError`. Prima di usare
    `popitem` si controlla che il dizionario contenga almeno un'associazione.
    """
    vuoto = {}
    vuoto.popitem()


def demo_errore_chiave_lista() -> None:
    """Solleva `TypeError`: una lista come chiave di dizionario.

    L'istruzione `chiavi = {[1, 2]: "x"}` non arriva a costruire il
    dizionario: la lista non è hashabile perché mutabile e il programma si
    interrompe con `TypeError: unhashable type: 'list'`. L'errore riguarda la
    CHIAVE e non il valore: i valori possono essere liste.
    """
    chiavi = {[1, 2]: "x"}


def demo_errore_chiave_tupla_con_lista() -> None:
    """Solleva `TypeError`: una tupla che contiene una lista come chiave.

    L'istruzione `chiavi = {(1, [2]): "x"}` solleva
    `TypeError: unhashable type: 'list'`. Una tupla è hashabile soltanto se
    TUTTI i propri elementi lo sono: `("a", 1)` è una chiave ammessa,
    `(1, [2])` no. La struttura annidata non nasconde l'elemento non
    hashabile.
    """
    chiavi = {(1, [2]): "x"}


# ---------------------------------------------------------------------------
# Insiemi — operazioni fra insiemi
# ---------------------------------------------------------------------------


def prova_prodotti_fra_insiemi() -> dict[str, set[str]]:
    """Restituisce i cinque insiemi prodotti dalle operazioni binarie.

    Usa `A_INSIEME = {"A", "B", "C"}` e `B_INSIEME = {"B", "D"}` e
    restituisce un dizionario con le chiavi `unione`, `intersezione`,
    `differenza_a_meno_b`, `differenza_b_meno_a`, `differenza_simmetrica`.
    L'unione raccoglie gli elementi di almeno uno dei due; l'intersezione
    quelli comuni; la differenza è ORIENTATA: `A - B` e `B - A` sono
    operazioni diverse e producono risultati diversi; la differenza
    simmetrica raccoglie gli elementi presenti in un solo insieme.

    Ogni operatore con `|`, `&`, `-`, `^` produce un insieme NUOVO e non
    modifica gli operandi. I corrispondenti metodi `union`, `intersection`,
    `difference`, `symmetric_difference` fanno lo stesso e accettano anche
    altri iterabili, mentre gli operatori richiedono insiemi.
    """
    a = set(A_INSIEME)
    b = set(B_INSIEME)
    return {
        "unione": a | b,
        "intersezione": a & b,
        "differenza_a_meno_b": a - b,
        "differenza_b_meno_a": b - a,
        "differenza_simmetrica": a ^ b,
    }


def prova_confronti_fra_insiemi() -> tuple[bool, bool, bool, bool]:
    """Restituisce quattro esiti di confronto fra sottoinsiemi e disgiunzione.

    Usa `A_INSIEME` e `B_INSIEME` e restituisce la tupla
    `({"B"} < a, a.isdisjoint(b), set() <= a, confronto_incompleto)`,
    che vale `(True, False, True, True)`. Con `<=` e `>=` si confrontano sottoinsiemi non
    propri; con `<` e `>` i sottoinsiemi PROPRI, che devono anche differire
    per almeno un elemento. L'insieme vuoto è sottoinsieme di ogni insieme e
    non è proprio di sé stesso. `isdisjoint` risponde `True` soltanto se non
    ci sono elementi comuni.

    La relazione di sottoinsieme non è un ordinamento totale: fra
    `{"A"}` e `{"B"}` nessuno dei due è sottoinsieme dell'altro e nessuno
    dei due confronti `<` è `True`.
    """
    a = set(A_INSIEME)
    b = set(B_INSIEME)
    sottoinsieme_proprio = {"B"} < a
    disgiunti = a.isdisjoint(b)
    vuoto_sottoinsieme = set() <= a
    confronto_incompleto = ({"A"} < {"B"}, {"B"} < {"A"})
    return (sottoinsieme_proprio, disgiunti, vuoto_sottoinsieme, confronto_incompleto == (False, False))


def prova_operatori_e_metodi() -> tuple[set[str], set[str], bool]:
    """Restituisce il confronto fra operatore e metodo, con iterabile non set.

    Costruisce `a = {"A", "B"}` e restituisce
    `(a.union(["B", "D"]), a | {"B", "D"}, a == {"A", "B"})`. Il metodo
    `union` accetta la LISTA `["B", "D"]` e attraversa i suoi elementi;
    l'operatore `|` richiede un insieme. Entrambi producono un insieme nuovo
    e l'insieme di partenza resta uguale a sé stesso.
    """
    a = {"A", "B"}
    return (a.union(["B", "D"]), a | {"B", "D"}, a == {"A", "B"})


def prova_aggiornamenti_in_posto() -> tuple[set[str], set[str], set[str]]:
    """Restituisce tre insiemi dopo gli aggiornamenti in posto.

    Parte da `{"A", "B", "C"}` ed esegue `add("AB")`, poi da `{"A", "B"}`
    esegue `update("AB")`, infine da `{"A", "B", "C"}` esegue
    `difference_update({"C"})`. Restituisce i tre insiemi aggiornati:
    `{"A", "AB", "B", "C"}`, `{"A", "B"}`, `{"A", "B"}`.

    `add` inserisce l'intero argomento come UN elemento: `add("AB")`
    aggiunge la stringa "AB". `update` attraversa invece l'iterabile e ne
    inserisce gli elementi: `update("AB")` attraversa i caratteri "A" e "B",
    già presenti. I metodi con `_update` modificano l'insieme in posto e
    restituiscono `None`; i corrispondenti metodi senza `_update`
    restituiscono un insieme nuovo.
    """
    con_add = {"A", "B", "C"}
    con_add.add("AB")
    con_update = {"A", "B"}
    con_update.update("AB")
    con_difference = {"A", "B", "C"}
    con_difference.difference_update({"C"})
    return (con_add, con_update, con_difference)


def prova_remove_e_discard() -> tuple[set[str], bool]:
    """Restituisce l'insieme dopo `remove` e l'esito del `discard` su assente.

    Parte da `{"A", "B"}`, esegue `insieme.discard("X")` e poi
    `insieme.remove("A")`. Restituisce `(insieme, "X" in insieme)`, che vale
    `({"B"}, False)`. `discard` di un elemento assente NON segnala nulla e
    lascia l'insieme invariato; `remove` di un elemento assente solleva
    `KeyError`, come mostrato in `demo_errore_remove_assente`. Entrambi i
    metodi restituiscono `None`: l'effetto si osserva sull'insieme.
    """
    insieme = {"A", "B"}
    insieme.discard("X")
    insieme.remove("A")
    return (insieme, "X" in insieme)


def prova_pop_insieme() -> tuple[bool, bool, int]:
    """Restituisce le proprietà dell'elemento estratto con `pop`.

    Costruisce `{"A", "B", "C"}`, misura la cardinalità ed esegue
    `estratto = insieme.pop()`. Restituisce
    `(estratto_prima_presente, estratto_ora_assente, diminuzione)`, che vale
    `(True, True, 1)`. `pop` estrae un elemento ARBITRARIO dell'insieme: non
    una scelta casuale governabile e non il primo in ordine di inserimento.
    La prova non fissa quale elemento viene estratto e controlla soltanto
    che fosse presente, che ora sia assente e che la cardinalità diminuisca
    di uno. Su un insieme vuoto `pop` solleva `KeyError`.
    """
    insieme = {"A", "B", "C"}
    prima = len(insieme)
    estratto = insieme.pop()
    return (
        estratto in {"A", "B", "C"},
        estratto not in insieme,
        prima - len(insieme) == 1,
    )


def prova_copia_e_clear_insieme() -> tuple[set[str], set[str], bool]:
    """Restituisce l'insieme, la sua copia e l'esito del confronto dopo `clear`.

    Parte da `A_INSIEME`, costruisce `copia = insieme.copy()`, esegue
    `insieme.clear()` e restituisce `(insieme, copia, copia == A_INSIEME)`.
    Gli elementi di un insieme sono hashable e quindi immutabili: la copia
    superficiale è qui sufficiente a rendere indipendenti i due insiemi.
    `clear` svuota l'insieme di partenza e restituisce `None`; la copia
    conserva i propri elementi.
    """
    insieme = set(A_INSIEME)
    copia = insieme.copy()
    insieme.clear()
    return (insieme, copia, copia == A_INSIEME)


def prova_insieme_vuoto_e_duplicati() -> tuple[int, set[int], list[int]]:
    """Restituisce gli esiti della costruzione per vuoto e per duplicati.

    Restituisce `(len(set()), set([3, 1, 3, 2, 1]), [3, 1, 3, 2, 1])`.
    `set()` costruisce l'insieme VUOTO: non esiste un letterale vuoto, perché
    `{}` denota un dizionario. La conversione da lista elimina i duplicati e
    conserva solo gli elementi distinti. La lista di partenza non viene
    modificata e conserva duplicati e ordine: sostituire la lista con
    `list(set(valori))` perderebbe l'ordine di incontro, che è un
    contratto da garantire separatamente.
    """
    valori = [3, 1, 3, 2, 1]
    return (len(set()), set(valori), list(valori))


# ---------------------------------------------------------------------------
# Errori intenzionali isolati sugli insiemi
# ---------------------------------------------------------------------------


def demo_errore_remove_assente() -> None:
    """Solleva `KeyError`: `remove` di un elemento assente.

    L'istruzione `{"A", "B"}.remove("X")` chiede di rimuovere un elemento
    che non c'è e il programma si interrompe con `KeyError: 'X'`. Per una
    rimozione che tollera l'assenza si usa `discard`, che non segnala nulla.
    """
    insieme = {"A", "B"}
    insieme.remove("X")


def demo_errore_pop_insieme_vuoto() -> None:
    """Solleva `KeyError`: `pop` su un insieme vuoto.

    L'istruzione `set().pop()` non ha elementi da estrarre e il programma si
    interrompe con `KeyError`. Prima di `pop` si controlla la cardinalità
    dell'insieme.
    """
    insieme = set()
    insieme.pop()


def demo_errore_indice_insieme() -> None:
    """Solleva `TypeError`: indicizzazione o slicing di un insieme.

    L'istruzione `insieme[0]` solleva `TypeError: 'set' object is not
    subscriptable`: un insieme non è una sequenza, non ha posizioni e non
    ammette né indice né slicing. Per scorrerne gli elementi si usa un
    ciclo `for`; per richiedere un ordine si costruisce una lista, per
    esempio con `sorted` quando gli elementi sono confrontabili.
    """
    insieme = {"A", "B"}
    insieme[0]


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    print("Dizionari — scorte, ordine, viste e copie")
    print("dataset di partenza :", dict(SCORTE_INIZIALI))
    print("chiave contro valore:", prova_chiave_e_valore())
    print("aggiornamento R10   :", prova_aggiornamento_e_ordine())
    print("zero lecito (C20)   :", prova_zero_lecito())
    print("get con default     :", prova_get_con_default())
    print("setdefault su presente:", prova_setdefault_su_presente())
    print("setdefault su assente :", prova_setdefault_su_assente())
    print("popitem             :", prova_popitem_ultima_inserita())
    print("cancella e reinserisci:", prova_cancella_e_reinserisci())
    print("None non è assenza  :", prova_none_non_e_assenza())
    print("vista e fotografia  :", prova_vista_e_fotografia())
    print("copia superficiale  :", prova_copia_superficiale())
    print("ritorno di update   :", prova_ritorno_di_update())
    print("ritorno di clear    :", prova_ritorno_di_clear())
    print("pop con default     :", prova_pop_con_default())
    print("popitem e ordine    :", prova_popitem_e_ordine_rimanente())
    print("chiavi ammesse      :", prova_chiavi_ammesse())

    print()
    print("Insiemi — operazioni e confronti")
    print("dataset A e B       :", set(A_INSIEME), set(B_INSIEME))
    prodotti = prova_prodotti_fra_insiemi()
    for nome in sorted(prodotti):
        print(f"  {nome + ':':<24}", sorted(prodotti[nome]))
    print("confronti           :", prova_confronti_fra_insiemi())
    print("operatori e metodi  :", prova_operatori_e_metodi())
    print("aggiornamenti in posto:", prova_aggiornamenti_in_posto())
    print("remove e discard    :", prova_remove_e_discard())
    print("pop su insieme      :", prova_pop_insieme())
    print("copia e clear       :", prova_copia_e_clear_insieme())
    print("vuoto e duplicati   :", prova_insieme_vuoto_e_duplicati())

    print()
    print("Errori intenzionali isolati (NON eseguiti da questa demo)")
    print("  demo_errore_accesso_assente()     -> KeyError: 'X99'")
    print("  demo_errore_pop_senza_default()   -> KeyError: 'X99'")
    print("  demo_errore_popitem_vuoto()       -> KeyError")
    print("  demo_errore_chiave_lista()        -> TypeError: unhashable type: 'list'")
    print("  demo_errore_chiave_tupla_con_lista() -> TypeError: unhashable type: 'list'")
    print("  demo_errore_remove_assente()      -> KeyError: 'X'")
    print("  demo_errore_pop_insieme_vuoto()   -> KeyError")
    print("  demo_errore_indice_insieme()      -> TypeError: 'set' object is not subscriptable")
