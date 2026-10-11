"""Soluzioni formative degli esercizi di base — Unità 17.

Il modulo raccoglie le funzioni e le classi citate nelle soluzioni
guidate della raccolta di esercizi dell'Unità 17. Ogni soluzione è
autonoma e verificabile; il codice usa soltanto i costrutti raggiunti
nelle unità precedenti e i moduli `alberi_binari_u17` e `bst_u17`.
"""

from __future__ import annotations

from alberi_binari_u17 import Nodo, altezza, conta_foglie, conta_nodi, inordine


# --- PY-U17-C01 ---------------------------------------------------------
def elementi_di_un_albero(radice):
    """Restituisce nodi, archi, foglie e sottoalberi di un albero.

    La relazione fra nodi e archi è `archi = nodi - 1` per un albero non
    vuoto, perché ogni nodo diverso dalla radice ha un solo padre.
    """
    nodi = conta_nodi(radice)
    foglie = conta_foglie(radice)
    return {"nodi": nodi, "archi": max(nodi - 1, 0), "foglie": foglie}


# --- PY-U17-C02 ---------------------------------------------------------
def profondita_e_altezza(radice, valore):
    """Restituisce `(profondita, altezza_del_sottoalbero)` per `valore`.

    Entrambe le misure sono in archi: la radice ha profondità 0, una
    foglia ha altezza 0 e il sottoalbero vuoto ha altezza -1.
    """

    def cerca(nodo, profondita):
        if nodo is None:
            return None
        if nodo.valore == valore:
            return nodo, profondita
        trovato = cerca(nodo.sinistro, profondita + 1)
        if trovato is not None:
            return trovato
        return cerca(nodo.destro, profondita + 1)

    risultato = cerca(radice, 0)
    if risultato is None:
        return None, None
    nodo, profondita = risultato
    return profondita, altezza(nodo)


# --- PY-U17-T02 ---------------------------------------------------------
def visita_con_accumulatore(nodo, ordine, risultato=None):
    """Restituisce i valori nell'`ordine` richiesto usando un accumulatore.

    La funzione esterna crea una nuova lista, l'ausiliaria la riempie e
    la funzione restituisce quella lista: la concatenazione ripetuta di
    liste intermedie viene evitata.
    """
    if risultato is None:
        risultato = []
    if nodo is None:
        return risultato
    if ordine == "preordine":
        risultato.append(nodo.valore)
    visita_con_accumulatore(nodo.sinistro, ordine, risultato)
    if ordine == "inordine":
        risultato.append(nodo.valore)
    visita_con_accumulatore(nodo.destro, ordine, risultato)
    if ordine == "postordine":
        risultato.append(nodo.valore)
    return risultato


# --- PY-U17-T01 ---------------------------------------------------------
def conta_nodi_a_profondita(nodo, profondita_richiesta, profondita=0):
    """Conta i nodi situati alla `profondita_richiesta`.

    La profondità è in archi e la radice ha profondità 0; una profondità
    negativa oppure superiore all'altezza restituisce 0.
    """
    if nodo is None:
        return 0
    if profondita == profondita_richiesta:
        return 1
    if profondita > profondita_richiesta:
        return 0
    return conta_nodi_a_profondita(
        nodo.sinistro, profondita_richiesta, profondita + 1
    ) + conta_nodi_a_profondita(nodo.destro, profondita_richiesta, profondita + 1)


# --- PY-U17-T03 / T04 / T05 --------------------------------------------
def ricerca_con_contratti(albero, chiave):
    """Mostra i due contratti distinti di `cerca` e `contiene`.

    Il risultato è una coppia `(presente, dato)`: il dato può valere
    `None`, `0`, `False` o `""` e resta un dato valido, distinto
    dall'assenza che il contratto di `cerca` segnala con `KeyError`.
    """
    presente = albero.contiene(chiave)
    if not presente:
        return False, None
    return True, albero.cerca(chiave)


def inserisci_o_aggiorna(albero, chiave, dato):
    """Inserisce la coppia o aggiorna il dato della chiave già presente.

    L'intenzione è dichiarata dallo stato precedente: la chiave nuova
    viene inserita, quella esistente viene aggiornata senza far crescere
    l'albero.
    """
    if albero.contiene(chiave):
        albero.aggiorna(chiave, dato)
        return "aggiornato"
    albero.inserisci(chiave, dato)
    return "inserito"


# --- PY-U17-E02 ---------------------------------------------------------
def controllo_ordine_solo_padre_errato(nodo, limite_inferiore=None, limite_superiore=None):
    """Versione deliberatamente incompleta del controllo d'ordine.

    Il controllo confronta la chiave soltanto con i limiti del padre
    immediato e trasmette gli stessi limiti ai figli: il discendente 45
    nel sottoalbero sinistro di 40 supera il limite imposto dalla radice
    eppure non viene rilevato. La versione corretta aggiorna i limiti a
    ogni discesa.
    """
    if nodo is None:
        return True
    if limite_inferiore is not None and nodo.chiave <= limite_inferiore:
        return False
    if limite_superiore is not None and nodo.chiave >= limite_superiore:
        return False
    # I limiti non vengono ristretti: qui si annida il difetto.
    return controllo_ordine_solo_padre_errato(
        nodo.sinistro, limite_inferiore, limite_superiore
    ) and controllo_ordine_solo_padre_errato(nodo.destro, limite_inferiore, limite_superiore)


# --- PY-U17-X01 ---------------------------------------------------------
def preordine_iterativo(radice):
    """Restituisce il preordine usando una pila esplicita.

    La pila conserva i nodi ancora da elaborare: il nodo viene estratto,
    elaborato e sostituito dai figli inseriti prima il destro e poi il
    sinistro, così il sinistro viene estratto per primo.
    """
    if radice is None:
        return []
    risultato = []
    pila = [radice]
    while pila:
        nodo = pila.pop()
        risultato.append(nodo.valore)
        if nodo.destro is not None:
            pila.append(nodo.destro)
        if nodo.sinistro is not None:
            pila.append(nodo.sinistro)
    return risultato


# --- utilità di verifica -------------------------------------------------
def costruisci_d1_nodi():
    """Costruisce D1 con la classe `Nodo` del capitolo PY-32."""
    nodo_25 = Nodo(25)
    nodo_35 = Nodo(35)
    nodo_55 = Nodo(55)
    nodo_10 = Nodo(10)
    nodo_30 = Nodo(30, nodo_25, nodo_35)
    nodo_50 = Nodo(50, None, nodo_55)
    nodo_70 = Nodo(70)
    nodo_20 = Nodo(20, nodo_10, nodo_30)
    nodo_60 = Nodo(60, nodo_50, nodo_70)
    return Nodo(40, nodo_20, nodo_60)


def verifica_soluzioni_base():
    """Esegue i controlli essenziali sulle soluzioni e restituisce gli esiti."""
    d1 = costruisci_d1_nodi()
    esiti = {
        "elementi": elementi_di_un_albero(d1),
        "profondita_altezza_20": profondita_e_altezza(d1, 20),
        "inordine": inordine(d1),
        "preordine_iterativo": preordine_iterativo(d1),
        "nodi_profondita_3": conta_nodi_a_profondita(d1, 3),
    }
    assert esiti["elementi"] == {"nodi": 10, "archi": 9, "foglie": 5}
    assert esiti["profondita_altezza_20"] == (1, 2)
    assert esiti["nodi_profondita_3"] == 3
    return esiti


if __name__ == "__main__":
    for nome, valore in verifica_soluzioni_base().items():
        print(f"{nome}: {valore}")
