"""Conteggi delle scansioni dell'Unità 9: visite, addizioni e confronti.

Collocare il file in `programmi/conteggi_scansioni.py` della raccolta
dello studente. Il modulo contiene il problema svolto I del capitolo PY-13:
il riepilogo di una lista di interi a due scansioni e a una scansione, la
scansione con arresto `contiene_zero` e le varianti STRUMENTATE che contano
le operazioni del modello di costo.

Modello di costo adottato: ogni esecuzione del corpo di un ciclo che
attraversa la lista è una VISITA e costa 1; ogni `totale += valore` è una
ADDIZIONE; ogni `valore > 0` o `valore == 0` è un CONFRONTO. Le operazioni
su numeri di dimensione limitata hanno costo unitario: non si contano byte
né istruzioni dell'interprete. Le due scansioni eseguono 2n visite e quella
singola n visite, ma le addizioni al totale sono n in entrambe e n sono
anche i confronti sui valori: non tutte le operazioni raddoppiano.

Le funzioni ordinarie e quelle strumentate hanno CONTRATTI DIVERSI. Le
prime restituiscono il solo risultato e sono quelle da cronometrare; le
seconde aggiungono il conteggio delle operazioni e non vanno misurate per
attribuirne il tempo alla versione ordinaria. I contatori sono nuovi a ogni
esecuzione: nessuno stato globale si accumula fra prove successive.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/conteggi_scansioni.py
"""


# ---------------------------------------------------------------------------
# Problema svolto I — riepilogo a due scansioni e a una scansione
# ---------------------------------------------------------------------------


def riepilogo_due_scansioni(valori: list[int]) -> tuple[int, int]:
    """Restituisce `(totale, positivi)` attraversando `valori` due volte.

    Contratto: `valori` è una lista di interi; il risultato è la tupla
    `(totale, positivi)`, dove `totale` è la somma algebrica dei valori e
    `positivi` è il numero di valori strettamente maggiori di zero.
    L'argomento resta invariato; non esegue input né output. Per la lista
    vuota il risultato è `(0, 0)`.

    Modello di costo: l'operazione contata è la visita al corpo del ciclo
    che attraversa la lista e questa versione ne esegue 2n. Le addizioni al
    totale sono n e i confronti `valore > 0` sono n: il doppio delle visite
    non significa il doppio di ogni istruzione né il doppio del tempo.
    """
    totale = 0
    for valore in valori:
        totale += valore
    positivi = 0
    for valore in valori:
        if valore > 0:
            positivi += 1
    return totale, positivi


def riepilogo_una_scansione(valori: list[int]) -> tuple[int, int]:
    """Restituisce `(totale, positivi)` con un solo attraversamento.

    Stesso contratto, stesso risultato e stesso argomento invariato di
    `riepilogo_due_scansioni`; cambia l'organizzazione del lavoro, non la
    promessa. Ogni elemento viene visitato una volta sola: n visite,
    n addizioni al totale e n confronti `valore > 0`.

    Entrambe le versioni hanno tempo Θ(n) e spazio ausiliario Θ(1) nel
    modello a parole di dimensione limitata: la riduzione delle visite da
    2n a n non cambia l'ordine di crescita.
    """
    totale = 0
    positivi = 0
    for valore in valori:
        totale += valore
        if valore > 0:
            positivi += 1
    return totale, positivi


def riepilogo_con_soglia(valori: list[int], soglia: int) -> tuple[int, int]:
    """Restituisce `(totale, oltre_soglia)` con un solo attraversamento.

    Variante con riscontro del problema svolto I: il `totale` è lo stesso di
    `riepilogo_una_scansione`, mentre il secondo campo conta i valori
    strettamente maggiori di `soglia`. Con `soglia = 0` il conteggio coincide
    con quello dei valori positivi; cambiando soglia cambia il secondo campo
    e non il primo. Dominio: `valori` lista di interi, `soglia` intero.
    Nessun input, nessuna stampa, argomenti invariati.
    """
    totale = 0
    oltre_soglia = 0
    for valore in valori:
        totale += valore
        if valore > soglia:
            oltre_soglia += 1
    return totale, oltre_soglia


# ---------------------------------------------------------------------------
# Scansione con arresto
# ---------------------------------------------------------------------------


def contiene_zero(valori: list[int]) -> bool:
    """Restituisce True se `valori` contiene almeno uno zero.

    Dominio: `valori` è una lista di interi. Il ciclo si arresta al primo
    zero incontrato; la lista vuota restituisce False senza eseguire
    confronti. Operazione contata: il confronto `valore == 0`, da 1 a n
    secondo la posizione del primo zero, oppure n se lo zero è assente.
    Nessun input, nessuna stampa, argomento invariato.
    """
    for valore in valori:
        if valore == 0:
            return True
    return False


# ---------------------------------------------------------------------------
# Versioni strumentate — contratto diverso, contatori nuovi a ogni chiamata
# ---------------------------------------------------------------------------


def riepilogo_due_scansioni_osservato(
    valori: list[int],
) -> tuple[int, int, dict[str, int]]:
    """Come `riepilogo_due_scansioni`, con il conteggio delle operazioni.

    CONTRATTO DIVERSO: oltre alla coppia `(totale, positivi)` restituisce
    anche `statistiche`, un dizionario NUOVO a ogni esecuzione con le chiavi
    `visite`, `addizioni` e `confronti`. Il contatore si azzera a ogni
    chiamata perché le statistiche nascono dentro la funzione: non esiste
    alcun contatore globale che sopravvive fra prove successive. Il
    risultato algoritmico coincide con quello della versione ordinaria e va
    confrontato con quello prima di usare i conteggi.
    """
    totale = 0
    statistiche = {"visite": 0, "addizioni": 0, "confronti": 0}
    for valore in valori:
        statistiche["visite"] += 1
        statistiche["addizioni"] += 1
        totale += valore
    positivi = 0
    for valore in valori:
        statistiche["visite"] += 1
        statistiche["confronti"] += 1
        if valore > 0:
            positivi += 1
    return totale, positivi, statistiche


def riepilogo_una_scansione_osservato(
    valori: list[int],
) -> tuple[int, int, dict[str, int]]:
    """Come `riepilogo_una_scansione`, con il conteggio delle operazioni.

    CONTRATTO DIVERSO: restituisce la terza `(totale, positivi, statistiche)`
    con le stesse chiavi e la stessa convenzione di
    `riepilogo_due_scansioni_osservato`. Le visite valgono n mentre le
    addizioni e i confronti restano n: serve a verificare che la riduzione
    del lavoro riguarda le visite e non ogni operazione del modello.
    """
    totale = 0
    positivi = 0
    statistiche = {"visite": 0, "addizioni": 0, "confronti": 0}
    for valore in valori:
        statistiche["visite"] += 1
        statistiche["addizioni"] += 1
        totale += valore
        statistiche["confronti"] += 1
        if valore > 0:
            positivi += 1
    return totale, positivi, statistiche


def contiene_zero_osservato(valori: list[int]) -> tuple[bool, dict[str, int]]:
    """Come `contiene_zero`, con il conteggio dei confronti eseguiti.

    CONTRATTO DIVERSO: restituisce la coppia `(esito, statistiche)`, dove
    `statistiche` è un dizionario nuovo a ogni esecuzione con la chiave
    `confronti`. Il conteggio si ferma all'arresto del ciclo: per n = 4 gli
    attesi sono 1, 2, 3, 4 confronti con lo zero in posizione iniziale,
    intermedia, finale e con lo zero ultimo, e 4 confronti con esito False
    quando lo zero è assente. La lista vuota restituisce `(False, 0)`.
    """
    statistiche = {"confronti": 0}
    for valore in valori:
        statistiche["confronti"] += 1
        if valore == 0:
            return True, statistiche
    return False, statistiche


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    casi = [
        ("[3, -2, 0, 5]", [3, -2, 0, 5]),
        ("[0]", [0]),
        ("[-3, -1]", [-3, -1]),
        ("[2, 2]", [2, 2]),
        ("[]", []),
    ]
    print("Riepiloghi equivalenti — attesi del capitolo")
    print("valori          due scansioni  una scansione")
    for etichetta, valori in casi:
        due = riepilogo_due_scansioni(valori)
        una = riepilogo_una_scansione(valori)
        print(f"{etichetta:<15} {str(due):<14} {una}")

    print()
    print("Conteggi strumentati sulla lista [3, -2, 0, 5] (n = 4)")
    valori = [3, -2, 0, 5]
    _, _, statistiche_due = riepilogo_due_scansioni_osservato(valori)
    _, _, statistiche_una = riepilogo_una_scansione_osservato(valori)
    print("due scansioni:", statistiche_due)
    print("una scansione:", statistiche_una)
    print("le addizioni e i confronti coincidono; cambiano le visite")

    print()
    print("I contatori si azzerano a ogni esecuzione")
    print("prima esecuzione :", riepilogo_una_scansione_osservato(valori)[2])
    print("seconda esecuzione:", riepilogo_una_scansione_osservato(valori)[2])

    print()
    print("Scansione con arresto — confronti attesi per n = 4")
    per_quattro = [[0, 7, 7, 7], [7, 0, 7, 7], [7, 7, 0, 7], [7, 7, 7, 0], [7, 7, 7, 7]]
    for sequenza in per_quattro:
        esito, statistiche = contiene_zero_osservato(sequenza)
        print(f"{sequenza}  esito {esito!s:<5} confronti {statistiche['confronti']}")
    esito, statistiche = contiene_zero_osservato([])
    print(f"[]  esito {esito!s:<5} confronti {statistiche['confronti']}")

    print()
    print("Variante con soglia — stesso totale, diverso secondo campo")
    for soglia in (0, 2, 3, 5):
        print(f"soglia {soglia}: {riepilogo_con_soglia([3, -2, 0, 5], soglia)}")
