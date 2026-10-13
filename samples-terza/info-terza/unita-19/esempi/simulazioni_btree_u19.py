"""Simulazioni verificate delle modifiche al B-tree — Unità 19 (cap. PY-35).

Il modulo applica gli scenari di cancellazione del capitolo su stati
iniziali completi e verifica le fotografie finali con il controllo degli
invarianti: ogni scenario parte dallo stato dichiarato, esegue l'operazione
con il contenitore didattico e confronta associazioni conservate, forma
canonica e altezza con gli attesi. La lista degli scenari disponibili è una
traccia verificabile delle riparazioni dal basso, non un'implementazione
alternativa delle operazioni.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from dati_btree_u19 import (
    costruisci_d1,
    costruisci_d3b_iniziale,
    costruisci_d3c_iniziale,
    costruisci_d3d_iniziale,
    costruisci_d3e_iniziale,
    costruisci_d4_iniziale,
    costruisci_d5_iniziale,
)


def _fotografia(albero):
    """Restituisce la forma dell'albero come struttura di liste confrontabile."""
    if albero.radice is None:
        return None

    def _nodo(nodo):
        return (list(nodo.voci), [_nodo(figlio) for figlio in nodo.figli])

    return _nodo(albero.radice)


def _coppie(chiavi):
    """Restituisce le coppie `(chiave, f"dato-{chiave}")` per le chiavi date."""
    return [(chiave, f"dato-{chiave}") for chiave in chiavi]


def _atteso_radice_foglie(radice, foglie):
    """Costruisce la fotografia attesa di un B-tree di altezza 1."""
    return (_coppie(radice), [(_coppie(foglia), []) for foglia in foglie])


#: Scenari di cancellazione del capitolo: nome, costruttore dello stato
#: iniziale, chiave da rimuovere, fotografia finale attesa, altezza attesa.
SCENARI = [
    (
        "D3a-foglia-sufficiente",
        costruisci_d1,
        6,
        _atteso_radice_foglie([10, 20], [[5, 7], [12, 17], [30]]),
        1,
    ),
    (
        "D3b-prestito-destro",
        costruisci_d3b_iniziale,
        5,
        _atteso_radice_foglie([25], [[20], [30]]),
        1,
    ),
    (
        "D3c-prestito-sinistro",
        costruisci_d3c_iniziale,
        25,
        _atteso_radice_foglie([10], [[5], [20]]),
        1,
    ),
    (
        "D3d-fusione-sinistra",
        costruisci_d3d_iniziale,
        15,
        _atteso_radice_foglie([20], [[5, 10], [25]]),
        1,
    ),
    ("D3e-radice-foglia", costruisci_d3e_iniziale, 5, (_coppie([10, 15]), []), 0),
    (
        "D3f-voce-interna",
        costruisci_d1,
        20,
        _atteso_radice_foglie([10, 17], [[5, 6, 7], [12], [30]]),
        1,
    ),
    (
        "D4-fusione-propagata",
        costruisci_d4_iniziale,
        10,
        _atteso_radice_foglie([40, 60], [[20, 30], [50], [70]]),
        1,
    ),
]


def applica_scenario(nome):
    """Applica lo scenario `nome` e restituisce albero e verifica finale.

    La funzione costruisce lo stato iniziale dichiarato, rimuove la chiave
    dello scenario, controlla gli invarianti del B-tree e confronta la
    fotografia con quella attesa. Uno scenario sconosciuto solleva
    `ValueError`. Il risultato è il dizionario con `albero`, `fotografia`,
    `attesa`, `coerente`, `dimensione` e `altezza`.
    """
    for nome_candidato, costruttore, chiave, attesa, altezza in SCENARI:
        if nome_candidato == nome:
            albero = costruttore()
            iniziali = {chiave_iniziale for chiave_iniziale, _dato in albero.voci_ordinate()}
            albero.rimuovi(chiave)
            albero.controlla_invarianti()
            fotografia = _fotografia(albero)
            finali = {chiave_finale for chiave_finale, _dato in albero.voci_ordinate()}
            coerente = (
                fotografia == attesa
                and finali == iniziali - {chiave}
                and albero.altezza() == altezza
            )
            return {
                "albero": albero,
                "fotografia": fotografia,
                "attesa": attesa,
                "coerente": coerente,
                "dimensione": len(albero),
                "altezza": albero.altezza(),
            }
    raise ValueError(f"scenario sconosciuto: {nome!r}")


def verifica_d5():
    """Applica D5 e verifica prestito interno e trasferimento del figlio.

    Lo scenario elimina `50` dallo stato D5: la riparazione produce la foglia
    `[60, 70]` e un padre destro temporaneamente vuoto, poi il nodo interno
    sinistro presta attraverso la radice e trasferisce il figlio `[35]`. La
    funzione restituisce il dizionario con `albero`, `foglia_trasferita` e
    `coerente`.
    """
    albero = costruisci_d5_iniziale()
    albero.rimuovi(50)
    albero.controlla_invarianti()
    destro = albero.radice.figli[1]
    foglia_trasferita = destro.figli[0].chiavi() == [35] and [
        voce[0] for voce in destro.figli[1].voci
    ] == [60, 70]
    coerente = (
        albero.radice.chiavi() == [30]
        and albero.radice.figli[0].chiavi() == [20]
        and destro.chiavi() == [40]
        and foglia_trasferita
        and len(albero) == 8
        and albero.altezza() == 2
    )
    return {"albero": albero, "foglia_trasferita": foglia_trasferita, "coerente": coerente}


def nomi_scenari():
    """Restituisce i nomi degli scenari di cancellazione disponibili."""
    return [nome for nome, _c, _ch, _a, _h in SCENARI]
