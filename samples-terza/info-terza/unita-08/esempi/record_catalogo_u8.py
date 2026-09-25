"""Record del catalogo dell'Unità 8: dalle liste parallele ai dizionari.

Collocare il file in `programmi/record_catalogo_u8.py` della raccolta dello
studente. Il modulo contiene il problema svolto del capitolo PY-12, parte
III: la migrazione da tre liste parallele a una lista di RECORD, cioè di
dizionari che descrivono ciascun articolo con gli stessi campi, e le
operazioni di consultazione, aggiornamento, inserimento, cancellazione e
ordinamento sul catalogo risultante.

Modello ricordato: nelle liste parallele la corrispondenza fra codice,
descrizione e quantità è garantita dallo stesso indice; nel record la
corrispondenza è espressa dalla struttura. Il codice è una STRINGA e
conserva gli zeri iniziali: "007" e "7" sono codici diversi. I campi dei
record sono `codice` (stringa non vuota), `descrizione` (stringa non vuota)
e `quantita` (intero non negativo).

Le annotazioni dei parametri dichiarano il contratto ma non convalidano gli
argomenti: il controllo esplicito implementato qui riguarda tipo, dominio e
relazioni fra dati, perché un rifiuto deve produrre `None` oppure `False`
senza modifiche, non un errore imprevisto.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/record_catalogo_u8.py
"""

CODICI_CANONICI = ["R10", "007", "L05"]

DESCRIZIONI_CANONICHE = ["Resistore", "Vite, lunga", "LED"]

QUANTITA_CANONICHE = [12, 4, 8]


# ---------------------------------------------------------------------------
# Migrazione dalle liste parallele ai record
# ---------------------------------------------------------------------------


def crea_articoli(
    codici: list[str], descrizioni: list[str], quantita: list[int]
) -> list[dict] | None:
    """Restituisce la lista dei record del catalogo, oppure `None` se i dati sono invalidi.

    Riceve tre liste parallele: `codici` di stringhe non vuote, `descrizioni`
    di stringhe non vuote e `quantita` di interi non negativi. Restituisce
    una lista NUOVA di record NUOVI, ciascuno un dizionario con le chiavi
    `codice`, `descrizione` e `quantita`, nell'ordine delle liste ricevute.

    I dati sono validi soltanto se le tre liste hanno la STESSA lunghezza,
    ogni codice e ogni descrizione sono stringhe non vuote, i codici sono
    UNIVOCI e ogni quantità è un intero esatto non negativo (`True` non è
    una quantità). Se un controllo fallisce il risultato è `None` e le
    liste ricevute non vengono modificate: nessun catalogo parziale viene
    prodotto. Tre liste vuote sono dati validi e producono `[]`.

    Ogni record è un oggetto proprio: due record distinti non condividono
    il dizionario, neppure quando descrivono articoli uguali. La lunghezza
    uguale delle liste parallele non basta da sola a garantire che le
    associazioni siano corrette: la correttezza dei dati è responsabilità di
    chi compila le liste.
    """
    if len(codici) != len(descrizioni) or len(codici) != len(quantita):
        return None
    visti = set()
    for posizione in range(len(codici)):
        codice = codici[posizione]
        descrizione = descrizioni[posizione]
        valore = quantita[posizione]
        if type(codice) is not str or codice == "":
            return None
        if type(descrizione) is not str or descrizione == "":
            return None
        if type(valore) is not int or valore < 0:
            return None
        if codice in visti:
            return None
        visti.add(codice)
    articoli = []
    for posizione in range(len(codici)):
        articoli.append(
            {
                "codice": codici[posizione],
                "descrizione": descrizioni[posizione],
                "quantita": quantita[posizione],
            }
        )
    return articoli


# ---------------------------------------------------------------------------
# Consultazione
# ---------------------------------------------------------------------------


def cerca_indice_articolo(articoli: list[dict], codice: str) -> int | None:
    """Restituisce la posizione dell'articolo con il `codice` cercato, oppure `None`.

    Riceve la lista `articoli`, già composta da record validi con codici
    univoci, e il `codice` da cercare. La scansione confronta il campo
    `codice` di ogni record, da sinistra a destra, e restituisce la
    posizione del primo riscontro; il contratto con codici univoci garantisce
    che sia anche l'unico. Se il codice non compare il risultato è `None`.

    L'indice 0 è un risultato valido e non indica l'assenza: è `None` a
    segnalare che il codice non c'è. La ricerca non modifica la lista né i
    record: legge e restituisce la posizione.
    """
    for posizione in range(len(articoli)):
        if articoli[posizione]["codice"] == codice:
            return posizione
    return None


# ---------------------------------------------------------------------------
# Aggiornamenti
# ---------------------------------------------------------------------------


def imposta_quantita(
    articoli: list[dict], codice: str, nuova_quantita: int
) -> bool:
    """Aggiorna la quantità dell'articolo indicato e restituisce l'esito.

    Riceve la lista `articoli`, il `codice` dell'articolo da aggiornare e la
    `nuova_quantita`. Restituisce `True` soltanto se il codice è presente e
    la quantità è un intero esatto non negativo (`True` non è una quantità):
    in tal caso sostituisce il solo campo `quantita` del record, che deve
    poter valere anche 0.

    Se il codice è assente oppure la quantità è fuori dominio il risultato è
    `False` e lo stato del catalogo resta INVARIATO: l'aggiornamento è
    atomico rispetto al contratto, non esistono modifiche parziali. Nessun
    campo diverso da `quantita` viene toccato.
    """
    if type(nuova_quantita) is not int or nuova_quantita < 0:
        return False
    posizione = cerca_indice_articolo(articoli, codice)
    if posizione is None:
        return False
    articoli[posizione]["quantita"] = nuova_quantita
    return True


def inserisci_articolo(
    articoli: list[dict], codice: str, descrizione: str, quantita: int
) -> bool:
    """Aggiunge in fondo un articolo nuovo e restituisce l'esito.

    Riceve la lista `articoli` e i tre campi del nuovo record. Restituisce
    `True` soltanto se i dati rispettano il dominio — `codice` e
    `descrizione` stringhe non vuote, `quantita` intero esatto non negativo —
    e il codice non è già presente. In tal caso inserisce in fondo un record
    NUOVO, con un dizionario proprio.

    Se i dati sono fuori dominio oppure il codice è già presente il
    risultato è `False` e la lista resta INVARIATA: in particolare il record
    esistente con quel codice NON viene sovrascritto né aggiornato. Per
    cambiare la quantità di un articolo già presente si usa
    `imposta_quantita`.
    """
    if type(codice) is not str or codice == "":
        return False
    if type(descrizione) is not str or descrizione == "":
        return False
    if type(quantita) is not int or quantita < 0:
        return False
    if cerca_indice_articolo(articoli, codice) is not None:
        return False
    articoli.append({"codice": codice, "descrizione": descrizione, "quantita": quantita})
    return True


def elimina_articolo(articoli: list[dict], codice: str) -> bool:
    """Rimuove l'intero record dell'articolo indicato e restituisce l'esito.

    Riceve la lista `articoli` e il `codice` dell'articolo da eliminare.
    Se il codice è presente rimuove l'INTERO record dalla lista e restituisce
    `True`; gli articoli successivi compattano le posizioni. Se il codice è
    assente il risultato è `False` e la lista resta INVARIATA. La rimozione
    tocca il record intero e non un singolo campo.
    """
    posizione = cerca_indice_articolo(articoli, codice)
    if posizione is None:
        return False
    del articoli[posizione]
    return True


# ---------------------------------------------------------------------------
# Ordinamento del catalogo
# ---------------------------------------------------------------------------


def chiave_articolo(articolo: dict) -> tuple[str, str]:
    """Restituisce la chiave di ordinamento dell'`articolo` ricevuto.

    Riceve un record del catalogo e restituisce la tupla
    `(descrizione, codice)`. Confrontando queste chiave si ordinano gli
    articoli per descrizione crescente e, a parità di descrizione, per
    codice crescente: il criterio secondario mantiene determinato
    l'ordinamento anche quando il criterio primario non basta a decidere.
    """
    return (articolo["descrizione"], articolo["codice"])


def ordina_articoli(articoli: list[dict]) -> list[dict]:
    """Restituisce una lista NUOVA di record ordinati per `(descrizione, codice)`.

    Riceve la lista `articoli` e restituisce una lista esterna NUOVA,
    prodotta da `sorted` con `key=chiave_articolo`, che ordina per
    descrizione crescente e, a parità, per codice crescente. La lista
    ricevuta NON viene riordinata e conserva il proprio ordine.

    I record della lista risultante sono gli stessi OGGETTI della lista
    ricevuta, non copie: la lista è nuova, i record sono condivisi. Un
    aggiornamento fatto attraverso un record si vede quindi da entrambe le
    liste. Per due record con la stessa descrizione, per esempio
    `{"codice": "R10", "descrizione": "Resistore", "quantita": 12}` e
    `{"codice": "R20", "descrizione": "Resistore", "quantita": 7}`, il
    risultato colloca prima R10 e poi R20.
    """
    return sorted(articoli, key=chiave_articolo)


def ordina_articoli_lambda(articoli: list[dict]) -> list[dict]:
    """Come `ordina_articoli`, con la chiave espressa da una lambda.

    Stesso ricevuto, stesso risultato e stessi effetti di `ordina_articoli`.
    La funzione `chiave_articolo` è qui sostituita dalla lambda equivalente
    `lambda articolo: (articolo["descrizione"], articolo["codice"])`: una
    funzione senza nome, adatta quando la chiave serve una sola volta e la
    sua formula è immediatamente leggibile. Le due versioni concordano su
    ogni catalogo e la si confronta per verificarlo.
    """
    return sorted(articoli, key=lambda articolo: (articolo["descrizione"], articolo["codice"]))


# ---------------------------------------------------------------------------
# Controesempio — ordinare la sola lista delle descrizioni
# ---------------------------------------------------------------------------


def controsesempio_ordina_descrizioni(descrizioni: list[str]) -> list[str]:
    """CONTROESEMPIO: restituisce le sole `descrizioni` ordinate.

    NON È LA SOLUZIONE del problema e non va usata per presentare il
    catalogo. Ordinare soltanto la lista delle descrizioni può lasciare
    lunghezze uguali e apparentemente regolari, ma rompe le associazioni con
    codici e quantità, che restano nell'ordine di partenza.

    Sul dataset canonico la prima riga presentata diventa R10/LED/12: il
    codice R10 e la quantità 12 appartengono al Resistore, mentre la
    descrizione LED è arrivata per prima dalla lista ordinata. Le lunghezze
    delle tre liste sono ancora 3, 3, 3: la forma è quella giusta e il
    contenuto è sbagliato. L'ordinamento corretto sposta l'INTERO record,
    come fa `ordina_articoli`.
    """
    return sorted(descrizioni)


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    print("Migrazione dalle liste parallele ai record")
    print("codici      :", CODICI_CANONICI)
    print("descrizioni :", DESCRIZIONI_CANONICHE)
    print("quantita    :", QUANTITA_CANONICHE)
    articoli = crea_articoli(CODICI_CANONICI, DESCRIZIONI_CANONICHE, QUANTITA_CANONICHE)
    for articolo in articoli:
        print("  record:", articolo)
    print("record distinti fra loro:", articoli[0] is not articoli[1])
    print("lunghezze discordanti 3,2,3:", crea_articoli(["R10", "007", "L05"], ["Resistore", "LED"], [12, 4, 8]))
    print("tre liste vuote           :", crea_articoli([], [], []))

    print()
    print("Consultazione")
    print("indice di R10 :", cerca_indice_articolo(articoli, "R10"))
    print("indice di X99 :", cerca_indice_articolo(articoli, "X99"))
    con_007_e_7 = crea_articoli(["007", "7"], ["Vite, lunga", "Vite corta"], [4, 9])
    print("\"007\" e \"7\" sono codici diversi:",
          cerca_indice_articolo(con_007_e_7, "007"), "e", cerca_indice_articolo(con_007_e_7, "7"))

    print()
    print("Aggiornamenti")
    print("imposta 007 a 0 :", imposta_quantita(articoli, "007", 0), articoli[1])
    print("imposta 007 a -1:", imposta_quantita(articoli, "007", -1), articoli[1], "(stato invariato)")
    print("imposta X99 a 5 :", imposta_quantita(articoli, "X99", 5), "(codice assente)")
    print("inserisci 007 duplicato:", inserisci_articolo(articoli, "007", "Vite corta", 9), articoli[1])
    print("inserisci C20          :", inserisci_articolo(articoli, "C20", "Condensatore", 3), articoli[-1])
    print("elimina X99            :", elimina_articolo(articoli, "X99"))
    print("elimina C20            :", elimina_articolo(articoli, "C20"), len(articoli))

    print()
    print("Ordinamento per (descrizione, codice)")
    ordinati = ordina_articoli(articoli)
    print("lista ordinata :", [(a["codice"], a["descrizione"], a["quantita"]) for a in ordinati])
    print("input invariato:", [a["codice"] for a in articoli])
    print("record condivisi:", ordinati[0] is articoli[2], "(il primo ordinato è il record L05 della lista ricevuta)")
    print("lambda concorda:", ordina_articoli_lambda(articoli) == ordinati)

    print()
    print("Controesempio: ordinare la sola lista delle descrizioni")
    ordinate = controsesempio_ordina_descrizioni(DESCRIZIONI_CANONICHE)
    print("descrizioni ordinate:", ordinate)
    print("codici invariati    :", CODICI_CANONICI)
    print("quantita invariate  :", QUANTITA_CANONICHE)
    print("prima riga presentata:",
          CODICI_CANONICI[0], "/", ordinate[0], "/", QUANTITA_CANONICHE[0])
