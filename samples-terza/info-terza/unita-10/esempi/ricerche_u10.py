"""Ricerche dell'Unità 10: lineare, dicotomica iterativa e ricorsiva.

Questo modulo espone il **contratto canonico** del capitolo PY-14 e le sue
varianti esplicite. Il contratto canonico restituisce il **primo indice** della
chiave cercata oppure `None`, senza modificare l'argomento: la scelta rende
confrontabili i duplicati e permette di studiare separatamente le varianti.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
Le funzioni sono pure: non mutano la lista ricevuta e non producono output.

I nomi delle variabili sono italiani senza accenti; i testi di docstring e
commenti mantengono l'italiano corretto.
"""


# ---------------------------------------------------------------------------
# Contratto canonico - primo indice oppure None
# ---------------------------------------------------------------------------


def cerca_lineare(valori, bersaglio):
    """Restituisce il primo indice di `bersaglio` in `valori`, oppure `None`.

    Precondizione: `valori` è una sequenza indicizzabile di valori confrontabili
    con `bersaglio` tramite `==`. Nessun ordinamento richiesto.

    Postcondizione: il risultato è il più piccolo indice `i` tale che
    `valori[i] == bersaglio`, oppure `None` se `bersaglio` non compare. La
    lista ricevuta non viene modificata. L'indice `0` è un risultato valido:
    la sua validità va controllata con `is None`, non con la verità del valore.

    L'uscita avviene al primo incontro, quindi non si esaminano gli elementi
    successivi. Il caso migliore è 1 con il bersaglio in posizione 0,
    il caso peggiore n.

    Esempio:

        cerca_lineare([4, 7, 7, 9], 7)   # -> 1
        cerca_lineare([4, 7, 7, 9], 8)   # -> None
        cerca_lineare([], 7)             # -> None
    """
    for indice in range(len(valori)):
        if valori[indice] == bersaglio:
            return indice
    return None


def cerca_dicotomica(valori, bersaglio):
    """Restituisce il primo indice di `bersaglio` in una lista ordinata.

    Precondizione: `valori` è una lista **non decrescente** rispetto alla stessa
    relazione usata per confrontare `bersaglio`. Il controllo di questa
    precondizione non è compito della funzione: verificare l'ordine a ogni
    chiamata costerebbe n e annullerebbe il vantaggio della ricerca.

    Postcondizione: stesso contratto di `cerca_lineare` - primo indice oppure
    `None`, argomento invariato. Anche in presenza di duplicati il risultato è
    la **prima** occorrenza: dopo una corrispondenza al medio la ricerca
    continua nella metà sinistra e il miglior candidato viene conservato.

    Estremi inclusivi: `sinistra = 0`, `destra = len(valori) - 1` e il ciclo
    prosegue con `sinistra <= destra`. Ogni passo esamina il medio con un
    sondaggio e produce un intervallo strettamente più corto.

    Esempio:

        cerca_dicotomica([1, 3, 3, 3, 8], 3)   # -> 1
        cerca_dicotomica([1, 3, 3, 3, 8], 0)   # -> None
    """
    sinistra = 0
    destra = len(valori) - 1
    candidato = None
    while sinistra <= destra:
        medio = (sinistra + destra) // 2
        if valori[medio] == bersaglio:
            candidato = medio
            destra = medio - 1          # la prima occorrenza è a sinistra o qui
        elif valori[medio] < bersaglio:
            sinistra = medio + 1        # il bersaglio, se c'è, è più a destra
        else:
            destra = medio - 1          # il bersaglio, se c'è, è più a sinistra
    return candidato


def cerca_dicotomica_ricorsiva(valori, bersaglio):
    """Come `cerca_dicotomica`, organizzata come ricorsione sugli estremi.

    Precondizione e postcondizione identiche a `cerca_dicotomica`. L'ausiliario
    `_primo_indice` riceve gli estremi `sinistra` e `destra` come interi e non
    costruisce mai sottoliste: nessuno slicing, quindi nessuna copia di
    elementi. La memoria aggiuntiva è costituita soltanto dai frame dello
    stack, al massimo log n contemporanei.
    """
    return _primo_indice(valori, bersaglio, 0, len(valori) - 1)


def _primo_indice(valori, bersaglio, sinistra, destra):
    """Cerca il primo indice di `bersaglio` nell'intervallo `[sinistra, destra]`.

    Caso base: `sinistra > destra` indica un intervallo vuoto e restituisce
    `None`. Riduzione: ogni chiamata passa a un intervallo strettamente più
    corto, quindi la ricorsione termina. Quando il medio contiene il bersaglio,
    il risultato della metà sinistra prevale se presente; altrimenti il medio
    stesso è la prima occorrenza.
    """
    if sinistra > destra:
        return None
    medio = (sinistra + destra) // 2
    if valori[medio] == bersaglio:
        a_sinistra = _primo_indice(valori, bersaglio, sinistra, medio - 1)
        return medio if a_sinistra is None else a_sinistra
    if valori[medio] < bersaglio:
        return _primo_indice(valori, bersaglio, medio + 1, destra)
    return _primo_indice(valori, bersaglio, sinistra, medio - 1)


# ---------------------------------------------------------------------------
# Varianti di contratto - non intercambiabili fra loro
# ---------------------------------------------------------------------------


def contiene(valori, bersaglio):
    """Restituisce `True` se `bersaglio` compare in `valori`, altrimenti `False`.

    Contratto booleano: non dice **dove** si trova la chiave e non distingue la
    prima occorrenza da una qualsiasi. Non è intercambiabile con il contratto
    del primo indice: su duplicati il risultato è uguale, ma l'informazione no.
    """
    return cerca_lineare(valori, bersaglio) is not None


def cerca_un_indice(valori, bersaglio):
    """Restituisce **un** indice di `bersaglio` in lista ordinata, oppure `None`.

    Contratto diverso dal precedente: si accontenta di una corrispondenza
    qualsiasi e può terminare al primo medio, senza proseguire a sinistra. Su
    `[1, 3, 3, 3, 8]` con bersaglio `3` il risultato può essere `2` invece di
    `1`: è un esito corretto per questo contratto e sbagliato per il primo
    indice. Il caso migliore è 1 per qualunque posizione del medio.
    """
    sinistra = 0
    destra = len(valori) - 1
    while sinistra <= destra:
        medio = (sinistra + destra) // 2
        if valori[medio] == bersaglio:
            return medio
        if valori[medio] < bersaglio:
            sinistra = medio + 1
        else:
            destra = medio - 1
    return None


def cerca_tutti_gli_indici(valori, bersaglio):
    """Restituisce la **lista** di tutti gli indici di `bersaglio`, in ordine.

    Contratto che produce output: il risultato contiene un elemento per ogni
    occorrenza, quindi il suo costo non può essere costante. La scansione
    completa dell'argomento costa n e la lista prodotta k,
    dove k è il numero di occorrenze: il tempo totale è n + k, che
    è n quando k ≤ n. Anche su lista ordinata la risposta a
    «dove sono **tutti**?» richiede di elencare le occorrenze.
    """
    indici = []
    for indice in range(len(valori)):
        if valori[indice] == bersaglio:
            indici.append(indice)
    return indici


def posizione_di_inserimento(valori, valore):
    """Restituisce la posizione in cui `valore` andrebbe inserito in ordine.

    Precondizione: `valori` non decrescente. Il risultato è l'indice `p` tale
    che inserire `valore` in `valori[p]` mantiene l'ordine e gli elementi
    attualmente in posizione `p` o successiva spostano a destra. A parità con
    valori già presenti, `p` è la posizione della **prima** occorrenza: è la
    stessa regola di `bisect.bisect_left` della libreria standard.

    È un contratto diverso dalla ricerca: non dice se il valore c'è, dice dove
    starebbe. La posizione si trova in log n, ma inserire davvero un
    elemento in una `list` costa n per gli spostamenti.
    """
    sinistra = 0
    destra = len(valori)          # estremo destro escluso: p può valere len(valori)
    while sinistra < destra:
        medio = (sinistra + destra) // 2
        if valori[medio] < valore:
            sinistra = medio + 1
        else:
            destra = medio
    return sinistra


if __name__ == "__main__":
    # Dimostrazione dei quattro contratti sulle stesse liste.
    # Uscita attesa:
    #   lineare 7 -> 1 | dicotomica 7 -> 1 | ricorsiva 7 -> 1 | contiene 7 -> True
    #   un_indice 3 -> 2 | tutti 3 -> [1, 2, 3] | inserimento 3 -> 1
    #   lineare 8 -> None | dicotomica 8 -> None | ricorsiva 8 -> None
    valori = [4, 7, 7, 9]
    print(f"lineare 7 -> {cerca_lineare(valori, 7)} | "
          f"dicotomica 7 -> {cerca_dicotomica(valori, 7)} | "
          f"ricorsiva 7 -> {cerca_dicotomica_ricorsiva(valori, 7)} | "
          f"contiene 7 -> {contiene(valori, 7)}")
    ordinati = [1, 3, 3, 3, 8]
    print(f"un_indice 3 -> {cerca_un_indice(ordinati, 3)} | "
          f"tutti 3 -> {cerca_tutti_gli_indici(ordinati, 3)} | "
          f"inserimento 3 -> {posizione_di_inserimento(ordinati, 3)}")
    print(f"lineare 8 -> {cerca_lineare(valori, 8)} | "
          f"dicotomica 8 -> {cerca_dicotomica(valori, 8)} | "
          f"ricorsiva 8 -> {cerca_dicotomica_ricorsiva(valori, 8)}")
