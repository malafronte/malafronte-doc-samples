"""Mutabilità, identità, alias e copie: i riferimenti dell'Unità 7.

Collocare il file in `programmi/riferimenti_copie_u7.py` della raccolta
dello studente. Il modulo rende osservabili, senza stampare, quattro fatti
distinti del modello a oggetti di Python:

1. assegnamento e passaggio di parametro collegano un NOME a un OGGETTO;
   due nomi possono indicare lo stesso oggetto (alias);
2. una funzione può MODIFICARE l'oggetto ricevuto, oppure limitarsi a
   riassegnare il proprio parametro: solo la prima azione è visibile al
   chiamante;
3. una copia superficiale (`copy()`, slicing, `list()`) crea una lista
   nuova ma condivide gli ELEMENTI; se gli elementi sono liste, le righe
   interne restano condivise;
4. una copia profonda costruisce anche le strutture annidate; il corso la
   realizza a mano con cicli annidati prima di incontrare lo strumento
   generale.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/riferimenti_copie_u7.py
"""


# ---------------------------------------------------------------------------
# Effetti sul parametro: modifica contro riassegnamento
# ---------------------------------------------------------------------------


def aggiungi_alias(elemento: list[int], valore: int) -> None:
    """Aggiunge `valore` alla lista `elemento` ricevuta e non restituisce nulla.

    Riceve la lista `elemento` e l'intero `valore` da aggiungere. MODIFICA
    l'oggetto lista indicato dal parametro: chi chiama osserva
    l'aggiornamento sulla propria variabile, perché parametro e variabile
    del chiamante indicano la STESSA lista. Il risultato è `None`. Per lista
    vuota il risultato è una lista di un solo elemento.

    Questa è la ragione per cui gli alias sono utili: permettono a una
    funzione di aggiornare una struttura già posseduta dal chiamante.
    """
    elemento.append(valore)


def riassegna_parametro(elemento: list[int]) -> None:
    """Sostituisce il parametro `elemento` con una nuova lista vuota, senza effetti visibili.

    Riceve la lista `elemento` e la usa soltanto per riassegnare il NOME
    LOCALE `elemento` a una lista NUOVA e vuota. Non MODIFICA la lista
    ricevuta: l'assegnamento cambia il legame fra nome e oggetto nel solo
    frame della funzione. Il risultato è `None`. Per lista vuota l'effetto
    sul chiamante è ugualmente nullo.

    Il contrasto con `aggiungi_alias` è il punto della funzione: due scritte
    apparentemente simili (`elemento.append(...)` contro
    `elemento = [...]`) hanno conseguenze opposte per chi chiama. Per
    restituire una lista diversa il modo esplicito è `return`.
    """
    elemento = []


def modifica_cella(matrice: list[list[int]], riga: int, colonna: int, valore: int) -> None:
    """Scrive `valore` nella cella (`riga`, `colonna`) della `matrice` ricevuta.

    Riceve la matrice `matrice`, gli indici `riga` e `colonna` e il
    `valore` da scrivere. MODIFICA in loco la lista della riga indicata,
    quindi la matrice intera: chi chiama osserva il cambiamento. Il
    risultato è `None`. Per matrice vuota la chiamata non è applicabile:
    gli indici devono appartenere alle dimensioni già note.

    La riga è una lista condivisa fra tutti i nomi che indicano la matrice:
    la scrittura è visibile attraverso ogni alias.
    """
    matrice[riga][colonna] = valore


# ---------------------------------------------------------------------------
# Copie di una struttura annidata
# ---------------------------------------------------------------------------


def copia_superficiale(matrice: list[list[int]]) -> list[list[int]]:
    """Restituisce una copia superficiale della `matrice`, con le righe condivise.

    Riceve la matrice `matrice` e restituisce `matrice.copy()`: la lista
    esterna è NUOVA, ma gli elementi che contiene sono gli STESSI riferimenti
    di partenza. Poiché ogni elemento è a sua volta una lista di interi,
    le righe interne restano CONDIVISE fra la copia e l'originale: una
    scrittura come `copia[0][0] = 99` si vede anche da `matrice[0][0]`.
    L'argomento non viene modificato dalla copia stessa. Per matrice vuota
    il risultato è una lista vuota nuova.

    La profondità di una copia va decisa sulla struttura: superficiale per
    liste di valori immutabili, profonda quando gli elementi sono a loro
    volta contenitori modificabili.
    """
    return matrice.copy()


def ricostruisci_matrice(matrice: list[list[int]]) -> list[list[int]]:
    """Restituisce una matrice nuova con righe INDIPENDENTI da quelle ricevute.

    Riceve la matrice `matrice` e costruisce, con due cicli annidati
    espliciti, una lista esterna nuova le cui righe sono liste nuove: la
    copia è profonda fino al livello degli interi, che sono immutabili e
    possono essere copiati per riferimento. L'argomento non viene
    modificato. Per matrice vuota il risultato è una lista vuota nuova; per
    matrice con righe di lunghezze diverse la funzione rispetta comunque
    la lunghezza di ogni riga, senza imporre la rettangolarità.

    Dopo questa funzione `copia_profonda_manuale` dichiara lo stesso
    procedimento con il nome generale che gli compete.
    """
    ricostruita = []
    for riga in matrice:
        nuova_riga = []
        for elemento in riga:
            nuova_riga.append(elemento)
        ricostruita.append(nuova_riga)
    return ricostruita


def copia_profonda_manuale(matrice: list[list[int]]) -> list[list[int]]:
    """Restituisce una copia profonda della `matrice`, costruita a mano con cicli annidati.

    Riceve la matrice `matrice` e restituisce una struttura nuova in cui
    lista esterna e righe interne sono oggetti distinti da quelli ricevuti;
    gli interi sono immutabili e restano condivisi senza conseguenze.
    L'argomento non viene modificato. Per matrice vuota il risultato è una
    lista vuota nuova.

    Nella libreria standard esiste `copy.deepcopy`, che realizza la copia
    profonda di qualunque struttura e sarebbe lo strumento generale. Il
    corso la costruisce prima A MANO per rendere visibile che cosa significa
    «copiare a ogni livello»: ogni contenitore annidato va creato di nuovo.
    """
    copia = []
    for riga in matrice:
        riga_copiata = []
        for elemento in riga:
            riga_copiata.append(elemento)
        copia.append(riga_copiata)
    return copia


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: le funzioni sopra restituiscono
    # e non scrivono nulla.
    print("0) Modifica del parametro contro riassegnamento del parametro")
    elenco = [1, 2]
    aggiungi_alias(elenco, 3)
    print("aggiungi_alias(elenco, 3) ->", elenco, "-> il chiamante vede 3")
    riassegna_parametro(elenco)
    print("riassegna_parametro(elenco) ->", elenco, "-> nessun cambiamento visibile")
    print()
    originale = [[1, 2], [3, 4]]
    print("1) Alias: due nomi, una sola matrice")
    alias = originale
    print("originale:", originale)
    print("alias    :", alias, "-> stesso oggetto:", alias is originale)

    print()
    print("2) Copia superficiale: lista esterna nuova, righe condivise")
    copia = copia_superficiale(originale)
    print("copia    :", copia, "-> lista esterna diversa:", copia is not originale)
    print("prima riga condivisa:", copia[0] is originale[0])

    print()
    print("3) Dopo la mutazione interna copia[0][0] = 99")
    copia[0][0] = 99
    print("copia    :", copia, "-> la copia vede 99")
    print("originale:", originale, "-> vede 99 perché la riga è condivisa")
    print("alias    :", alias, "-> vede 99 perché indica la stessa matrice")

    print()
    print("4) Dopo originale.append([5, 6])")
    originale.append([5, 6])
    print("originale:", originale)
    print("alias    :", alias, "-> vede la nuova riga")
    print("copia    :", copia, "-> NON la vede: la lista esterna è propria")

    print()
    print("5) Copia profonda manuale: nessuna riga condivisa")
    profonda = copia_profonda_manuale(originale)
    profonda[0][0] = 111
    print("profonda :", profonda, "-> cella scritta nella copia")
    print("originale:", originale, "-> invariato, righe indipendenti")
    print("nessuna riga condivisa:", not any(
        riga_copia is riga_origine for riga_copia, riga_origine in zip(profonda, originale)
    ))

    # Osservazione opzionale (non richiesta dal percorso essenziale).
    # DOPO aver costruito la copia profonda a mano, si può confrontarla con
    # `copy.deepcopy`, lo strumento generale della libreria standard che
    # realizza la stessa operazione su strutture di qualunque profondità.
    # Il corso non lo usa nelle consegne: qui serve solo a riconoscere che
    # il procedimento manuale anticipa uno strumento già esistente.
    import copy

    con_modulo = copy.deepcopy(originale)
    con_modulo[0][0] = 222
    print()
    print("6) Osservazione opzionale con copy.deepcopy")
    print("con_modulo:", con_modulo, "-> cella scritta nella copia")
    print("originale :", originale, "-> invariato, come con la copia manuale")
    print("i due risultati coincidono nella struttura:",
          copy.deepcopy(originale) == copia_profonda_manuale(originale))

    print()
    print("7) Tupla con elemento modificabile")
    tupla = ([1, 2], 3)
    print("prima della mutazione:", tupla)
    # La tupla protegge i propri RIFERIMENTI: l'elemento in posizione 0 non
    # può essere sostituito, perché `tupla[0] = [...]` solleva `TypeError`.
    # L'oggetto a cui quel riferimento punta resta però modificabile, e
    # `tupla[0].append(9)` è del tutto legale.
    tupla[0].append(9)
    print("dopo tupla[0].append(9):", tupla, "-> mutazione legale sull'elemento")

    print()
    print("8) Uguaglianza contro identità")
    sinistra = [1, 2, 3]
    destra = [1, 2, 3]
    print("sinistra:", sinistra, "destra:", destra)
    print("sinistra == destra :", sinistra == destra, "-> stesso contenuto")
    print("sinistra is destra :", sinistra is destra, "-> oggetti distinti")
    alias_lista = sinistra
    print("sinistra is alias_lista:", sinistra is alias_lista, "-> stesso oggetto")
    print("alias_lista == destra  :", alias_lista == destra)
