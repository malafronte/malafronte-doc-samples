"""Problemi di algoritmica dell'Unità 7: soluzioni di riferimento.

Collocare il file in `programmi/problemi_algoritmici_u7.py` della raccolta
dello studente. Il modulo raccoglie le soluzioni dei dieci problemi
dell'unità su sequenze, scansioni e matrici. Ogni problema è una funzione
autonoma con il proprio contratto nel docstring; la scelta del
procedimento e la sua traccia stanno nella scheda del problema, qui resta
la soluzione verificabile.

Ordine di presentazione seguito: prima la scansione esplicita con i propri
accumulatori, poi la forma compatta solo dove il corso l'ha già spiegata.
Le funzioni che modificano la lista ricevuta lo dichiarano nel docstring e
restituiscono `None`; le altre restituiscono un risultato nuovo senza
toccare gli argomenti.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/problemi_algoritmici_u7.py
"""


def sopra_media(valori: list[int]) -> list[int]:
    """Restituisce i valori strettamente superiori alla media, nell'ordine di partenza.

    Riceve la lista `valori`. DUE passaggi: il primo somma gli elementi e
    ricava la media senza arrotondare, il secondo seleziona gli elementi
    con `valore > media`. Il risultato è una lista NUOVA che conserva
    l'ordine di comparizione e anche i duplicati. L'argomento non viene
    modificato. Per lista vuota il risultato è `[]`, perché non esiste una
    media da confrontare.

    Con `[12, 7, 19, 7]` la media è 11.25 e il risultato è `[12, 19]`:
    arrotondare la media a 11 oppure a 12 cambia la selezione.
    """
    if not valori:
        return []
    somma = 0
    for valore in valori:
        somma += valore
    media_valori = somma / len(valori)
    selezionati = []
    for valore in valori:
        if valore > media_valori:
            selezionati.append(valore)
    return selezionati


def inverti_sul_posto(valori: list[int]) -> None:
    """Inverte l'ordine degli elementi di `valori` sul posto e non restituisce nulla.

    Riceve la lista `valori` e la MODIFICA in loco scambiando le coppie
    simmetriche: il primo con l'ultimo, il secondo con il penultimo, e
    così via, fermandosi a metà. Due indici convergono dai due estremi
    verso il centro e a ogni passo scambiano i propri elementi.

    L'argomento viene modificato: le alias della lista osservano subito
    l'inversione. Il risultato è `None`. Per lista vuota, e per lista di un
    solo elemento, non accade nulla.

    Vincolo deliberato del problema: NON si usano `reverse()`, `reversed()`
    né lo slicing. L'obiettivo è rendere visibile il movimento degli indici
    e lo scambio con una variabile temporanea.
    """
    sinistra = 0
    destra = len(valori) - 1
    while sinistra < destra:
        temporaneo = valori[sinistra]
        valori[sinistra] = valori[destra]
        valori[destra] = temporaneo
        sinistra += 1
        destra -= 1


def segmento_piu_lungo(valori: list[int]) -> tuple[int, int]:
    """Restituisce `(inizio, lunghezza)` del segmento contiguo di valori uguali più lungo.

    Riceve la lista `valori` e individua la sequenza più lunga di elementi
    ADIACENTI tutti uguali fra loro. Restituisce la tupla
    `(inizio, lunghezza)`: la posizione del primo elemento del segmento e
    il numero dei suoi elementi. L'argomento non viene modificato.

    In caso di parità di lunghezza vince il segmento che compare PER PRIMO:
    il confronto usa `>` e non `>=`, quindi un segmento più tardo non
    sostituisce il migliore già trovato. Per lista vuota il risultato è
    `(0, 0)`, che segnala assenza di segmenti senza inventare un indice.
    Per lista di un solo elemento il risultato è `(0, 1)`.

    Con `[5, 5, 2, 2, 2, 5]` il risultato è `(2, 3)`: il segmento di tre 2
    è più lungo di quello di due 5 iniziale.
    """
    if not valori:
        return (0, 0)
    migliore_inizio = 0
    migliore_lunghezza = 1
    inizio_corrente = 0
    for posizione in range(1, len(valori)):
        if valori[posizione] != valori[posizione - 1]:
            inizio_corrente = posizione
        lunghezza_corrente = posizione - inizio_corrente + 1
        if lunghezza_corrente > migliore_lunghezza:
            migliore_inizio = inizio_corrente
            migliore_lunghezza = lunghezza_corrente
    return (migliore_inizio, migliore_lunghezza)


def fondi_ordinate(prima: list[int], seconda: list[int]) -> list[int]:
    """Fonde due liste già ordinate in senso non decrescente, senza risortarle.

    Riceve le liste `prima` e `seconda`, entrambe ordinate in senso non
    decrescente, e restituisce una lista NUOVA con tutti gli elementi di
    entrambe, ordinata allo stesso modo. Due indici percorrono le due liste
    una volta sola: a ogni passo si prende l'elemento minore fra i due
    candidati e si avanza nella lista che lo fornito. Tutti i DUPLICATI
    sono conservati, compresi quelli presenti nella stessa lista.

    L'argomento non viene modificato. Per due liste vuote il risultato è
    `[]`; se una delle due è vuota il risultato coincide con l'altra,
    copiata nella lista nuova.

    Vincolo deliberato del problema: NON si usa `sorted()` né `sort()`.
    La fusione lineare sfrutta l'ordinamento già presente e costa un solo
    passaggio sul totale degli elementi.
    """
    fusa = []
    indice_prima = 0
    indice_seconda = 0
    while indice_prima < len(prima) and indice_seconda < len(seconda):
        if prima[indice_prima] <= seconda[indice_seconda]:
            fusa.append(prima[indice_prima])
            indice_prima += 1
        else:
            fusa.append(seconda[indice_seconda])
            indice_seconda += 1
    while indice_prima < len(prima):
        fusa.append(prima[indice_prima])
        indice_prima += 1
    while indice_seconda < len(seconda):
        fusa.append(seconda[indice_seconda])
        indice_seconda += 1
    return fusa


def somme_righe_colonne(matrice: list[list[int]]) -> tuple[list[int], list[int]]:
    """Restituisce le somme per riga e le somme per colonna di una matrice rettangolare.

    Riceve la `matrice` rettangolare e non vuota, rappresentata come lista
    di liste. Restituisce la tupla `(somme_righe, somme_colonne)`: la prima
    lista contiene la somma di ogni riga nell'ordine delle righe, la seconda
    la somma di ogni colonna nell'ordine delle colonne. L'argomento non
    viene modificato.

    PRECONDIZIONE: la matrice ha almeno una riga e tutte le righe hanno la
    stessa lunghezza. Con matrice vuota il problema non è applicabile: non
    esistono colonne su cui eseguire la seconda scansione.

    Con `[[1, 2], [3, 4]]` il risultato è `([3, 7], [4, 6])`.
    """
    somme_righe = []
    for riga in matrice:
        somma = 0
        for elemento in riga:
            somma += elemento
        somme_righe.append(somma)

    numero_colonne = len(matrice[0])
    somme_colonne = []
    for j in range(numero_colonne):
        somma = 0
        for riga in matrice:
            somma += riga[j]
        somme_colonne.append(somma)

    return (somme_righe, somme_colonne)


def analizza_testo(testo: str) -> tuple[int, str, list[str]]:
    """Analizza il `testo` e restituisce conteggio, parola più lunga e elenco delle parole.

    Riceve la stringa `testo` e la suddivide sugli spazi con `split()`,
    che non produce elementi vuoti per le sequenze ripetute di separatori.
    Restituisce la tupla `(quante_parole, parola_piu_lunga, parole)`.

    La parola più lunga è quella di lunghezza massima; in caso di parità
    vince quella che compare PER PRIMA. La lista `parole` è quella prodotta
    dalla tokenizzazione, con ordine e ripetizioni intatti. L'argomento non
    viene modificato: le stringhe sono immutabili.

    Per testo vuoto, oppure composto dai soli spazi, il risultato è
    `(0, "", [])`: nessuna parola, nessuna parola più lunga.
    """
    parole = testo.split()
    if not parole:
        return (0, "", [])
    piu_lunga = parole[0]
    for parola in parole[1:]:
        if len(parola) > len(piu_lunga):
            piu_lunga = parola
    return (len(parole), piu_lunga, parole)


def indici_del_massimo(valori: list[int]) -> list[int]:
    """Restituisce tutti gli indici nei quali compare il valore massimo di `valori`.

    Riceve la lista `valori` e restituisce una lista NUOVA con gli indici
    di tutti gli elementi uguali al massimo, in ordine crescente di
    posizione. L'argomento non viene modificato. Per lista vuota il
    risultato è `[]`, perché non esiste un massimo.

    Due passaggi: il primo determina il massimo su tutti gli elementi, il
    secondo raccoglie gli indici che lo raggiungono. Con `[3, 7, 7, 2]` il
    risultato è `[1, 2]`, perché il massimo 7 compare in due posizioni.
    """
    if not valori:
        return []
    massimo = valori[0]
    for valore in valori:
        if valore > massimo:
            massimo = valore
    indici = []
    for posizione in range(len(valori)):
        if valori[posizione] == massimo:
            indici.append(posizione)
    return indici


def senza_duplicati(valori: list[int]) -> list[int]:
    """Restituisce gli elementi di `valori` senza ripetizioni, conservando il primo di ognuno.

    Riceve la lista `valori` e restituisce una lista NUOVA nella quale ogni
    elemento compare una sola volta, nella posizione della sua PRIMA
    occorrenza nell'elenco ricevuto. L'argomento non viene modificato.
    Per lista vuota il risultato è `[]`.

    Vincolo deliberato del problema: NON si usa l'insieme (`set`), che
    eliminerebbe i duplicati ma non garantirebbe l'ordine di comparizione.
    Il controllo di presenza avviene sulla lista dei risultati con
    l'operatore `in`, che scorre gli elementi già raccolti.
    """
    raccolti = []
    for valore in valori:
        if valore not in raccolti:
            raccolti.append(valore)
    return raccolti


def trasponi(matrice: list[list[int]]) -> list[list[int]]:
    """Restituisce la trasposta della `matrice`, in una struttura nuova e indipendente.

    Riceve la `matrice` rettangolare e ne restituisce la trasposta: la
    colonna `j` dell'originale diventa la riga `j` del risultato, quindi
    una matrice `righe` x `colonne` dà una matrice `colonne` x `righe`.
    Ogni riga del risultato è una lista NUOVA: l'argomento non viene
    modificato e nessuna riga è condivisa con esso.

    Per matrice vuota il risultato è `[]`. Per matrice di una sola riga
    (1xN) il risultato è una matrice di N righe di un solo elemento (Nx1);
    per matrice di una sola colonna (Nx1) il risultato è 1xN.
    """
    righe = len(matrice)
    if righe == 0:
        return []
    colonne = len(matrice[0])
    trasposta = []
    for j in range(colonne):
        nuova_riga = []
        for i in range(righe):
            nuova_riga.append(matrice[i][j])
        trasposta.append(nuova_riga)
    return trasposta


def quante_sovrapposte(testo: str, sotto: str) -> int:
    """Restituisce quante volte `sotto` compare in `testo`, anche sovrapponendosi.

    Riceve il `testo` da esaminare e la sottostringa `sotto`. Restituisce
    il numero di occorrenze considerando anche quelle SOVRAPPOSTE: dopo
    ogni occorrenza trovata la ricerca riprende dal carattere successivo a
    quello iniziale e non da quello successivo alla fine. Con `testo` uguale
    a `"aaa"` e `sotto` uguale a `"aa"` il risultato è 2, mentre `str.count`
    restituirebbe 1.

    L'argomento non viene modificato. CONTRATTO SUL VUOTO: per `sotto`
    vuoto il risultato è 0, anche se la stringa vuota compare formalmente
    in ogni posizione; contare le posizioni vuote non è l'obiettivo di
    questo problema. Per `sotto` più lunga di `testo` il risultato è 0.
    """
    if sotto == "":
        return 0
    if len(sotto) > len(testo):
        return 0
    lunghezza = len(sotto)
    conteggio = 0
    inizio = 0
    ultimo_inizio = len(testo) - lunghezza
    while inizio <= ultimo_inizio:
        if testo[inizio:inizio + lunghezza] == sotto:
            conteggio += 1
        # Avanzamento di un solo carattere: le occorrenze si possono
        # sovrapporre, quindi non si salta oltre la fine della corrispondenza.
        inizio += 1
    return conteggio


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: le funzioni sopra restituiscono
    # e non scrivono nulla.
    print("1) sopra_media — due passaggi, media non arrotondata")
    valori = [12, 7, 19, 7]
    print("   valori:", valori, "-> atteso [12, 19] con media 11.25")
    print("   risultato:", sopra_media(valori), "-> originale invariato:", valori)
    print("   [] ->", sopra_media([]))
    print("   [2, 2, 2] ->", sopra_media([2, 2, 2]), "-> nessuno supera la media")

    print()
    print("2) inverti_sul_posto — indici convergenti e scambi")
    valori = [1, 2, 3, 4, 5]
    alias = valori
    inverti_sul_posto(valori)
    print("   [1,2,3,4,5] ->", alias, "-> mutato, restituisce None")
    dispari = [1, 2, 3]
    inverti_sul_posto(dispari)
    print("   [1,2,3] ->", dispari, "-> numero dispari di elementi")
    singolo = [7]
    inverti_sul_posto(singolo)
    print("   [7] ->", singolo, "-> caso singolo")
    vuoto = []
    inverti_sul_posto(vuoto)
    print("   [] ->", vuoto, "-> nessuna operazione")

    print()
    print("3) segmento_piu_lungo — segmenti contigui di valori uguali")
    print("   [5, 5, 2, 2, 2, 5] ->", segmento_piu_lungo([5, 5, 2, 2, 2, 5]), "-> atteso (2, 3)")
    print("   [1, 1, 2, 2]       ->", segmento_piu_lungo([1, 1, 2, 2]), "-> parità, vince il primo")
    print("   [4]                ->", segmento_piu_lungo([4]), "-> caso singolo (0, 1)")
    print("   []                 ->", segmento_piu_lungo([]), "-> (0, 0)")

    print()
    print("4) fondi_ordinate — fusione lineare senza ordinamento")
    print("   [1, 3, 5] + [2, 3, 4] ->", fondi_ordinate([1, 3, 5], [2, 3, 4]))
    print("   [1, 1] + [1, 1]       ->", fondi_ordinate([1, 1], [1, 1]), "-> duplicati conservati")
    print("   [] + [2, 4]           ->", fondi_ordinate([], [2, 4]), "-> una lista vuota")
    print("   [] + []               ->", fondi_ordinate([], []))

    print()
    print("5) somme_righe_colonne — matrice rettangolare non vuota")
    matrice = [[1, 2], [3, 4]]
    print("   [[1, 2], [3, 4]] ->", somme_righe_colonne(matrice), "-> atteso ([3, 7], [4, 6])")
    print("   [[2, 4], [6, 8], [10, 12]] ->", somme_righe_colonne([[2, 4], [6, 8], [10, 12]]))

    print()
    print("6) analizza_testo — conteggio, parola più lunga, elenco")
    print("   'led rosso largo' ->", analizza_testo("led rosso largo"))
    print("   'a bb cc d'       ->", analizza_testo("a bb cc d"), "-> parità, vince la prima")
    print("   '   '             ->", analizza_testo("   "), "-> solo spazi")
    print("   ''                ->", analizza_testo(""))

    print()
    print("7) indici_del_massimo — tutti gli indici del massimo")
    print("   [3, 7, 7, 2] ->", indici_del_massimo([3, 7, 7, 2]), "-> atteso [1, 2]")
    print("   [5]          ->", indici_del_massimo([5]), "-> caso singolo [0]")
    print("   []           ->", indici_del_massimo([]), "-> []")

    print()
    print("8) senza_duplicati — primo di ogni valore, ordine conservato")
    print("   [3, 1, 3, 2, 1] ->", senza_duplicati([3, 1, 3, 2, 1]), "-> atteso [3, 1, 2]")
    print("   [4, 4, 4]       ->", senza_duplicati([4, 4, 4]))
    print("   []              ->", senza_duplicati([]))

    print()
    print("9) trasponi — righe nuove e indipendenti")
    matrice = [[2, 4], [6, 8], [10, 12]]
    trasposta = trasponi(matrice)
    print("   [[2, 4], [6, 8], [10, 12]] ->", trasposta, "-> atteso [[2, 6, 10], [4, 8, 12]]")
    print("   dimensioni 3x2 -> 2x3:", len(matrice), "x", len(matrice[0]),
          "->", len(trasposta), "x", len(trasposta[0]))
    trasposta[0][0] = 777
    print("   dopo trasposta[0][0] = 777 la matrice resta", matrice)
    print("   1xN: [[1, 2, 3]] ->", trasponi([[1, 2, 3]]))
    print("   Nx1: [[1], [2]] ->", trasponi([[1], [2]]))
    print("   [] ->", trasponi([]))

    print()
    print("10) quante_sovrapposte — occorrenze che si sovrappongono")
    print("   'aaa' / 'aa'   ->", quante_sovrapposte("aaa", "aa"), "-> atteso 2")
    print("   'aaaa' / 'aa'  ->", quante_sovrapposte("aaaa", "aa"), "-> atteso 3")
    print("   'banana' / 'an'->", quante_sovrapposte("banana", "an"), "-> atteso 2")
    print("   'ab' / 'abcd'  ->", quante_sovrapposte("ab", "abcd"), "-> sottostringa più lunga")
    print("   'abc' / ''     ->", quante_sovrapposte("abc", ""), "-> contratto: 0")
