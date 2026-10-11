"""Soluzioni formative dei problemi di algoritmica — Unità 17.

Il modulo raccoglie le realizzazioni dei problemi T06-T13 della famiglia
«Alberi, invarianti e interrogazioni ordinate». Ogni funzione dichiara
il proprio contratto e usa i moduli `bst_u17` e `confronto_altezze_u17`
come riferimento didattico.
"""

from __future__ import annotations

from bst_u17 import AlberoBST


# --- T06: eliminare una chiave con zero o un figlio ---------------------
def rimuovi_con_zero_o_un_figlio(radice, chiave):
    """Rimuove dal sottoalbero una chiave con al più un figlio.

    Contratto: restituisce la coppia `(nuova_radice, rimosso)`. La
    radice `None` e la chiave assente producono `(radice, False)`; una
    foglia viene sostituita dal sottoalbero vuoto e un nodo con un solo
    figlio dal riferimento a quel figlio.
    """
    if radice is None:
        return None, False
    if chiave < radice.chiave:
        radice.sinistro, rimosso = rimuovi_con_zero_o_un_figlio(radice.sinistro, chiave)
        return radice, rimosso
    if chiave > radice.chiave:
        radice.destro, rimosso = rimuovi_con_zero_o_un_figlio(radice.destro, chiave)
        return radice, rimosso
    if radice.sinistro is not None and radice.destro is not None:
        raise ValueError("il nodo da eliminare ha due figli: caso trattato dal problema T07")
    figlio = radice.sinistro if radice.sinistro is not None else radice.destro
    return figlio, True


# --- T07: eliminare una chiave con due figli ---------------------------
def rimuovi_con_due_figli(nodo, chiave):
    """Rimuove dal sottoalbero anche chiavi con due figli.

    Contratto: restituisce `(nuova_radice, rimosso)`. Per il nodo con
    due figli, chiave e dato del successore inordine sostituiscono quelli
    del nodo eliminato e il nodo del successore viene rimosso dal
    sottoalbero destro; il successore ha la posizione sinistra vuota, così
    la sua rimozione ricade nei casi con al più un figlio.
    """
    if nodo is None:
        return None, False
    if chiave < nodo.chiave:
        nodo.sinistro, rimosso = rimuovi_con_due_figli(nodo.sinistro, chiave)
        return nodo, rimosso
    if chiave > nodo.chiave:
        nodo.destro, rimosso = rimuovi_con_due_figli(nodo.destro, chiave)
        return nodo, rimosso
    if nodo.sinistro is None:
        return nodo.destro, True
    if nodo.destro is None:
        return nodo.sinistro, True
    successore = nodo.destro
    while successore.sinistro is not None:
        successore = successore.sinistro
    nodo.chiave = successore.chiave
    nodo.dato = successore.dato
    nodo.destro, _ = rimuovi_con_due_figli(nodo.destro, successore.chiave)
    return nodo, True


# --- T08: verificare ordine e dimensione --------------------------------
def verifica_ordine_e_dimensione(albero):
    """Verifica limiti ereditati, struttura e dimensione del contenitore.

    Precondizione dichiarata: i collegamenti formano un albero. Il
    controllo strutturale più ampio è offerto da `AlberoBST.
    controlla_invarianti`, che conserva anche gli identificatori degli
    oggetti già visitati.
    """
    totale = _visita(albero._radice, None, None)
    assert totale == albero._dimensione, (
        f"dimensione dichiarata {albero._dimensione}, nodi raggiungibili {totale}"
    )
    return True


def _visita(nodo, limite_inferiore, limite_superiore):
    if nodo is None:
        return 0
    if limite_inferiore is not None:
        assert nodo.chiave > limite_inferiore
    if limite_superiore is not None:
        assert nodo.chiave < limite_superiore
    return (
        1
        + _visita(nodo.sinistro, limite_inferiore, nodo.chiave)
        + _visita(nodo.destro, nodo.chiave, limite_superiore)
    )


# --- T09/T10: selezionare record in un intervallo ----------------------
def intervallo_con_visita_completa(albero, minimo, massimo):
    """Termine di confronto: visita completa con filtro successivo.

    Il costo è `Θ(n)` più il costo di presentazione; il risultato è
    identico a quello della visita che esclude i sottoalberi.
    """
    if minimo > massimo:
        raise ValueError("l'estremo minimo non può superare l'estremo massimo")
    return [voce for voce in albero.voci_ordinate() if minimo <= voce[0] <= massimo]


def intervallo_con_esclusione(albero, minimo, massimo, contatore=None):
    """Query su intervallo chiuso che esclude i sottoalberi irrilevanti.

    Il sottoalbero sinistro viene visitato quando `minimo < chiave`, la
    coppia viene raccolta quando `minimo <= chiave <= massimo`, il
    sottoalbero destro viene visitato quando `chiave < massimo`. Il
    costo è `O(h + 1 + k)` con `k` risultati.
    """
    if minimo > massimo:
        raise ValueError("l'estremo minimo non può superare l'estremo massimo")
    risultato = []
    esaminati = [0]

    def visita(nodo):
        if nodo is None:
            return
        esaminati[0] += 1
        if minimo < nodo.chiave:
            visita(nodo.sinistro)
        if minimo <= nodo.chiave <= massimo:
            risultato.append((nodo.chiave, nodo.dato))
        if nodo.chiave < massimo:
            visita(nodo.destro)

    visita(albero._radice)
    if contatore is not None:
        contatore["nodi_esaminati"] = esaminati[0]
    return risultato


# --- T11/T12: forme, altezze e costi -----------------------------------
def profilo_di_un_ordine(sequenza):
    """Restituisce il profilo di costruzione di un ordine di inserimento.

    Il risultato è un dizionario con `n`, `altezza`, `nodi_costruzione`
    e `nodi_ricerca` per la ricerca dell'ultima chiave e di una chiave
    assente appena oltre il massimo.
    """
    from confronto_altezze_u17 import misura_costruzione, misura_ricerca

    albero, nodi_costruzione, altezza = misura_costruzione(sequenza)
    massimo = max(sequenza)
    return {
        "n": len(sequenza),
        "altezza": altezza,
        "nodi_costruzione": nodi_costruzione,
        "ricerca_massimo": misura_ricerca(albero, massimo),
        "ricerca_assente": misura_ricerca(albero, massimo + 1),
    }


# --- T13: indice coerente su record ------------------------------------
def indice_pieno_e_verificato(indice):
    """Controlla che ogni chiave resti associata al proprio record.

    La verifica confronta le coppie chiave-record e non soltanto
    l'ordine delle chiavi: una trasposizione di record sotto chiavi
    diverse viene rilevata.
    """
    for chiave, record in indice.voci_ordinate():
        assert chiave == record.codice, f"chiave {chiave} associata al record {record}"
    return True


def prova_completa():
    """Esegue i controlli essenziali sulle soluzioni algoritmiche."""
    albero = AlberoBST()
    for chiave in [40, 20, 60, 10, 30, 50, 70, 25, 35, 55]:
        albero.inserisci(chiave, chiave)
    assert intervallo_con_visita_completa(albero, 25, 55) == intervallo_con_esclusione(
        albero, 25, 55
    )
    contatore = {}
    assert len(intervallo_con_esclusione(albero, 25, 55, contatore)) == 6
    assert contatore["nodi_esaminati"] <= len(albero)
    verifica_ordine_e_dimensione(albero)
    radice, rimosso = rimuovi_con_due_figli(albero._radice, 40)
    assert rimosso is True and radice.chiave == 50
    assert profilo_di_un_ordine([4, 2, 6, 1, 3, 5, 7])["altezza"] == 2
    assert profilo_di_un_ordine([1, 2, 3, 4, 5, 6, 7])["altezza"] == 6
    return True


if __name__ == "__main__":
    print("soluzioni algoritmiche verificate:", prova_completa())
