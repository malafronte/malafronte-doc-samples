"""Stringhe dell'Unità 7: sequenze immutabili e API di base.

Collocare il file in `programmi/stringhe_u7.py` della raccolta dello
studente. Il modulo raccoglie le funzioni dei due problemi svolti
(pulizia etichette del catalogo e verifica del codice) e una piccola
enciclopedia della API delle stringhe, ciascuna in una funzione minima
che restituisce il risultato invece di stamparlo.

Modello ricordato: in Python una stringa è una sequenza immutabile di
caratteri. Ogni operazione di trasformazione restituisce una NUOVA
stringa e lascia invariato l'argomento ricevuto; nessuna funzione di
questo modulo modifica il proprio argomento, perché per le stringhe la
modifica in loco non è nemmeno prevista dal linguaggio.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/stringhe_u7.py
"""


# ---------------------------------------------------------------------------
# Problema svolto 1 — Pulizia etichette del catalogo
# ---------------------------------------------------------------------------


def normalizza_etichetta(etichetta: str) -> str:
    """Restituisce la forma normalizzata dell'etichetta ricevuta.

    Riceve una stringa `etichetta`, in genere con spazi iniziali e finali
    e con spazi interni ripetuti. Restituisce una NUOVA stringa con gli
    spazi esterni eliminati (`strip`), le sequenze di spazi interne ridotte
    a un singolo spazio (`split` senza argomenti seguito da `join`) e tutte
    le lettere in forma minuscola (`casefold`).

    L'argomento non viene modificato: le stringhe sono immutabili e il
    valore ricevuto resta disponibile nella sua forma originale.
    Per etichetta vuota, oppure composta dai soli spazi, il risultato è la
    stringa vuota `""`.
    """
    senza_esterni = etichetta.strip()
    parole = senza_esterni.split()
    compatta = " ".join(parole)
    return compatta.casefold()


# ---------------------------------------------------------------------------
# Problema svolto 2 — Verifica del codice
# ---------------------------------------------------------------------------


def verifica_codice(codice: str, prefisso: str, suffisso: str) -> bool:
    """Restituisce True se il codice rispetta prefisso, suffisso e lunghezza.

    Riceve il `codice` da controllare, il `prefisso` atteso all'inizio e il
    `suffisso` atteso alla fine. Restituisce True soltanto se il codice
    INIZIA con il prefisso (`startswith`), TERMINA con il suffisso
    (`endswith`) ed è strettamente più lungo della concatenazione dei due:
    la parte centrale deve contenere almeno un carattere.

    L'argomento non viene modificato: la verifica legge e non scrive.
    Con prefisso e suffisso entrambi vuoti la condizione diventa
    `len(codice) > 0`, quindi il codice vuoto non è accettato.

    Si usano `startswith` e `endswith` e non `find` con un confronto su 0:
    `find` restituisce la posizione di un segmento e non risponde alla
    domanda «il codice comincia così?», che appartiene a `startswith`.
    """
    return (
        codice.startswith(prefisso)
        and codice.endswith(suffisso)
        and len(codice) > len(prefisso) + len(suffisso)
    )


# ---------------------------------------------------------------------------
# Piccola enciclopedia della API delle stringhe
# ---------------------------------------------------------------------------


def posizione_segmento(testo: str, segmento: str) -> int:
    """Restituisce la posizione della prima occorrenza di `segmento` in `testo`.

    Riceve il `testo` da esaminare e il `segmento` da cercare. Restituisce
    l'indice del primo carattere della prima occorrenza, oppure `-1` se il
    segmento non compare. Il valore è prodotto da `str.find`.

    L'argomento non viene modificato. Per `segmento` vuoto il risultato è 0,
    perché la stringa vuota compare all'inizio di ogni testo.

    ATTENZIONE: `-1` è un SENTINELLA da CONFRONTARE (`posizione == -1`
    significa «assente»), MAI da usare come indice. In Python `testo[-1]`
    indica l'ultimo carattere e non segnala alcuna assenza: usare `-1` per
    leggere il testo restituirebbe un carattere presente, con un risultato
    silenziosamente sbagliato. La funzione restituisce l'intero proprio
    perché sia il chiamante a decidere come gestire l'assenza.
    """
    return testo.find(segmento)


def quante_volte(testo: str, sotto: str) -> int:
    """Restituisce quante volte `sotto` compare in `testo`, senza sovrapposizioni.

    Riceve il `testo` da esaminare e la sottostringa `sotto`. Restituisce
    il numero di occorrenze contate da `str.count`, che considera
    occorrenze NON sovrapposte e scorre oltre l'intera occorrenza trovata:
    in `"aaa"` la sottostringa `"aa"` risulta presente una sola volta.

    L'argomento non viene modificato. Per `sotto` vuoto il risultato è
    `len(testo) + 1`, come definito da `str.count`: le posizioni ammesse per
    una sottostringa vuota sono tutte i confini fra i caratteri.
    Per `sotto` più lunga di `testo` il risultato è 0.
    """
    return testo.count(sotto)


def tokenizza(testo: str, separatore: str | None = None) -> list[str]:
    """Restituisce l'elenco dei frammenti di `testo`, suddivisi come indicato.

    Riceve il `testo` da suddividere e un `separatore` opzionale. Senza
    separatore (`None`) usa `split()` senza argomenti: gli spazi, le
    tabulazioni e gli a capo agiscono da separatori, le sequenze ripetute
    di separatori NON producono elementi vuoti e gli spazi esterni non
    generano elementi iniziali o finali. Con un separatore esplicito usa
    `split(separatore)`: ogni occorrenza del separatore delimita un campo,
    quindi due separatori consecutivi producono un campo vuoto `""`.

    Restituisce una NUOVA lista di NUOVE stringhe; l'argomento non viene
    modificato. Il caso del `testo` vuoto segue le due regole, senza
    eccezioni: `tokenizza("")` dà `[]`, perché `split()` senza argomenti
    non produce frammenti; `tokenizza("", ",")` dà `[""]`, perché con un
    separatore esplicito gli n separatori delimitano n + 1 campi e il testo
    vuoto contiene un solo campo, che è vuoto. Nessuna informazione si perde:
    la lunghezza del risultato è sempre il numero di campi attesi.

    Esempi di contrasto: `tokenizza("a   b")` dà `["a", "b"]`,
    `tokenizza("a,,b", ",")` dà `["a", "", "b"]`,
    `tokenizza(" a , b ", ",")` dà `[" a ", " b "]`, perché con un
    separatore esplicito gli spazi attorno ai campi restano parte del testo.
    """
    if separatore is None:
        return testo.split()
    return testo.split(separatore)


def ricomponi(parole: list[str], separatore: str) -> str:
    """Restituisce le `parole` concatenate in una sola stringa, separate da `separatore`.

    Riceve l'elenco delle `parole` e il `separatore` da porre fra l'una e
    l'altra. Restituisce la stringa composta, senza separatore né iniziale
    né finale.

    L'argomento non viene modificato: la composizione legge la lista e
    produce una stringa nuova. Per elenco vuoto il risultato è `""`, perché
    non ci sono elementi da separare.

    Il metodo si chiama sul SEPARATORE e riceve le parole:
    `separatore.join(parole)`, non `parole.join(separatore)`. È il
    separatore a sapere con quale stringa unire gli elementi.
    """
    return separatore.join(parole)


def demo_spazi(etichetta: str) -> tuple[str, str, str]:
    """Confronta `strip`, `lstrip` e `rstrip` sulla stessa etichetta.

    Riceve una stringa con spazi esterni. Restituisce la tupla
    `(solo_esterni, senza_iniziali, senza_finali)` corrispondente a
    `strip()`, `lstrip()`, `rstrip()`. Nessun argomento viene modificato:
    le tre chiamate restituiscono tre nuove stringhe. Per testo vuoto o
    senza spazi esterni le tre versioni coincidono con l'originale.
    """
    return (etichetta.strip(), etichetta.lstrip(), etichetta.rstrip())


def demo_maiuscole(testo: str) -> tuple[str, str, str]:
    """Confronta `lower`, `upper` e `casefold` sullo stesso testo.

    Riceve una stringa qualsiasi. Restituisce la tupla
    `(minuscolo, maiuscolo, forma_indifferente_al_case)` con i risultati di
    `lower()`, `upper()` e `casefold()`. `casefold` è la forma più marcata
    delle minuscole e serve per confronti che ignorano le differenze fra
    maiuscole e minuscole. Nessun argomento viene modificato. Per testo
    vuoto i tre risultati sono stringhe vuote.
    """
    return (testo.lower(), testo.upper(), testo.casefold())


def demo_righe(testo: str) -> list[str]:
    """Restituisce le righe del testo secondo i caratteri di fine riga.

    Riceve un testo che può contenere `\\n`, `\\r\\n` o `\\r`. Restituisce
    l'elenco delle righe prodotto da `splitlines()`, senza i caratteri di
    fine riga. L'argomento non viene modificato. Per testo vuoto il
    risultato è `[]`; una riga vuota interna compare come elemento `""`.
    """
    return testo.splitlines()


def demo_sostituisci(testo: str, vecchio: str, nuovo: str) -> str:
    """Restituisce il testo con ogni occorrenza di `vecchio` sostituita da `nuovo`.

    Riceve il `testo` da trasformare, il frammento `vecchio` da cercare e
    il frammento `nuovo` da scrivere al suo posto. Restituisce una NUOVA
    stringa: `replace` non modifica l'argomento, perché le stringhe sono
    immutabili. Per `vecchio` vuoto la sostituzione avviene prima di ogni
    carattere e alla fine del testo; per testo vuoto il risultato coincide
    con `nuovo` solo se anche `vecchio` è vuoto, altrimenti resta `""`.
    """
    return testo.replace(vecchio, nuovo)


def demo_confini(testo: str, prefisso: str, suffisso: str) -> tuple[bool, bool]:
    """Verifica i due estremi del testo con `startswith` e `endswith`.

    Riceve il `testo` da controllare, il `prefisso` e il `suffisso` attesi.
    Restituisce la tupla `(comincia_con_prefisso, termina_con_suffisso)`.
    L'argomento non viene modificato. Con prefisso o suffisso vuoti il
    risultato corrispondente è True, perché la stringa vuota compare in
    ogni posizione di confine.
    """
    return (testo.startswith(prefisso), testo.endswith(suffisso))


def demo_classi(testo: str) -> tuple[bool, bool, bool, bool]:
    """Classifica il testo con `isalpha`, `isdigit`, `isalnum` e `isspace`.

    Riceve la stringa da esaminare. Restituisce la tupla
    `(solo_lettere, solo_cifre, solo_lettere_o_cifre, solo_spazi)`.
    L'argomento non viene modificato. Tutte e quattro le risposte sono
    False per il testo vuoto: una stringa senza caratteri non appartiene a
    nessuna di queste classi, perché non contiene elementi da esaminare.
    """
    return (testo.isalpha(), testo.isdigit(), testo.isalnum(), testo.isspace())


def demo_prefissi(testo: str, prefisso: str, suffisso: str) -> str:
    """Toglie il prefisso e il suffisso solo se presenti, con `removeprefix` e `removesuffix`.

    Riceve il `testo` da cui rimuovere gli estremi, il `prefisso` e il
    `suffisso` candidati. Restituisce la stringa centrale: il prefisso
    viene tolto soltanto se il testo comincia davvero con esso, il suffisso
    soltanto se il testo termina con esso. L'argomento non viene
    modificato. Per testo vuoto il risultato è `""`; con prefisso o
    suffisso assenti il lato corrispondente resta invariato.
    """
    senza_prefisso = testo.removeprefix(prefisso)
    return senza_prefisso.removesuffix(suffisso)


def demo_indice(testo: str, sotto: str) -> tuple[int, int]:
    """Confronta `find` e `index` sulla stessa ricerca.

    Riceve il `testo` da esaminare e la sottostringa `sotto`. Restituisce
    la tupla `(posizione_con_find, posizione_con_index)`. L'argomento non
    viene modificato.

    Le due ricerche coincidono quando il frammento è presente. Quando è
    ASSENTE il comportamento diverge: `find` restituisce la sentinella `-1`
    e l'esecuzione prosegue, mentre `index` solleva `ValueError` e il
    programma si interrompe se l'errore non viene gestito. In questa unità
    la gestione delle eccezioni non è ancora un argomento trattato, quindi
    la chiamata a `index` avviene solo dopo aver accertato la presenza con
    l'operatore `in`; il commento sulla riga seguente documenta il caso
    senza eseguirlo.

    # testo.index("frammento_assente") -> ValueError (non gestito in questa unità)
    """
    if sotto in testo:
        return (testo.find(sotto), testo.index(sotto))
    return (testo.find(sotto), -1)


def demo_indici(testo: str) -> tuple[str, str, str]:
    """Mostra indici, indici negativi e slicing su una stringa non vuota.

    Riceve una stringa con almeno un carattere. Restituisce la tupla
    `(primo_carattere, ultimo_carattere, primi_due_caratteri)` ottenuta da
    `testo[0]`, `testo[-1]` e `testo[:2]`. L'argomento non viene modificato:
    ogni estrazione produce una stringa nuova. Per testo vuoto la funzione
    non è applicabile, perché l'indice 0 non esiste: il caso limite si
    controlla prima con `len(testo) == 0`.
    """
    return (testo[0], testo[-1], testo[:2])


def contiene(testo: str, sotto: str) -> bool:
    """Restituisce True se `sotto` compare in `testo`, con l'operatore `in`.

    Riceve il `testo` da esaminare e la sottostringa `sotto`. Restituisce
    la risposta booleana dell'operatore `in`, che non fornisce la posizione.
    L'argomento non viene modificato. Per `sotto` vuoto il risultato è True,
    perché la stringa vuota compare in ogni testo.
    """
    return sotto in testo


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: le funzioni restituiscono e
    # non scrivono nulla, così restano verificabili una per una.
    etichette = ["  LED-12  ", "led   rosso    5mm", "DISPLAY  OLED   128x64 ", "   ", ""]
    # Copia della lista di partenza: serve da testimone per dimostrare che
    # nessuna normalizzazione tocca le stringhe già esistenti.
    etichette_prima = list(etichette)
    print("Pulizia etichette del catalogo")
    print(f"{'originale':<28} | {'normalizzata':<28} | originale invariato")
    for indice, etichetta in enumerate(etichette):
        normalizzata = normalizza_etichetta(etichetta)
        # La normalizzazione ha prodotto una stringa NUOVA: la variabile
        # etichetta e il suo gemello nella lista di partenza sono intatti.
        invariata = etichetta == etichette_prima[indice]
        print(f"{etichetta!r:<28} | {normalizzata!r:<28} | {invariata}")
    print("tutte le etichette originali sono invariate:", etichette == etichette_prima)

    print()
    print("Verifica del codice")
    codice = "SEN-0042-A"
    print("codice originale:", codice)
    print("SEN / A :", verifica_codice(codice, "SEN", "A"))
    print("SEN / B :", verifica_codice(codice, "SEN", "B"))
    print("SEN / SEN:", verifica_codice(codice, "SEN", "SEN"))
    print("dopo le verifiche il codice è invariato:", codice == "SEN-0042-A")

    print()
    print("Ricerche e conteggi")
    print("posizione di '0042' in", codice, "->", posizione_segmento(codice, "0042"))
    print("posizione di 'xyz' ->", posizione_segmento(codice, "xyz"), "(sentinella, non un indice)")
    print("'an' in 'banana' quante volte ->", quante_volte("banana", "an"))
    print("'aa' in 'aaa' quante volte ->", quante_volte("aaa", "aa"), "(non sovrapposte)")

    print()
    print("Suddivisione e ricomposizione")
    print("senza separatore:", tokenizza("  le due   righe  "))
    print("con separatore ',':", tokenizza("a,,b", ","))
    print("testo vuoto senza separatore:", tokenizza(""), "-> []")
    print("testo vuoto con separatore ',':", tokenizza("", ","), "-> [''] : un solo campo, vuoto")
    print("ricomposione:", ricomponi(["led", "rosso", "5mm"], " / "))

    print()
    print("API in evidenza")
    print("spazi:", demo_spazi("  corso  "))
    print("maiuscole:", demo_maiuscole("Led-12"))
    print("righe:", demo_righe("prima\nseconda\n"))
    print("sostituzione:", demo_sostituisci("led-12", "12", "24"))
    print("confini:", demo_confini("SEN-0042-A", "SEN", "A"))
    print("classi:", demo_classi("128"))
    print("prefissi e suffissi presenti:", demo_prefissi("FAM-LED-12-r2", "FAM-", "-r2"))
    print("prefisso assente:", demo_prefissi("LED-12-r2", "FAM-", "-r2"), "(il prefisso non viene tolto)")
    print("find/index presenti:", demo_indice("banana", "nan"))
    print("find/index assenti:", demo_indice("banana", "xyz"))
    print("indici:", demo_indici("led"))
    print("'an' in 'banana':", contiene("banana", "an"))
