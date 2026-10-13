"""Dati canonici delle tracce sui B-tree — Unità 19 (cap. PY-35).

Il modulo costruisce gli stati stabili usati nelle spiegazioni, negli
esercizi e nelle prove: D1 per intervalli e ricerca, D2 per inserimenti
crescenti, D3a–D3f, D4 e D5 per cancellazioni indipendenti, D6 per record con
codici testuali. Ogni funzione restituisce un nuovo `BTreeDidattico`
indipendente; i casi di cancellazione ripartono dallo stato dichiarato. Il
dato associato alla chiave intera `x` è la stringa `f"dato-{x}"`.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from btree_modello_u19 import BTreeDidattico, NodoBTree


def _foglia(coppie):
    """Restituisce una foglia del B-tree con le coppie ordinate date."""
    return NodoBTree(list(coppie), [])


def _coppie_intere(*chiavi):
    """Restituisce le coppie `(chiave, f"dato-{chiave}")` per le chiavi date."""
    return [(chiave, f"dato-{chiave}") for chiave in chiavi]


def costruisci_d1():
    """Restituisce il B-tree D1: radice interna con otto associazioni.

    Lo stato stabile del B-tree ha grado minimo 2, radice `[10 | 20]`, figli
    `[5 | 6 | 7]`, `[12 | 17]`, `[30]` e altezza 1. La visita ordinata del
    B-tree produce le chiavi `[5, 6, 7, 10, 12, 17, 20, 30]`.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        _coppie_intere(10, 20),
        [
            _foglia(_coppie_intere(5, 6, 7)),
            _foglia(_coppie_intere(12, 17)),
            _foglia(_coppie_intere(30)),
        ],
    )
    albero.dimensione = 8
    albero.controlla_invarianti()
    return albero


def costruisci_d2_finale():
    """Restituisce il B-tree D2 dopo gli inserimenti `1..10` con `t = 2`.

    Lo stato stabile del B-tree ha radice `[4]`, sottoalberi `[2]` con foglie
    `[1]`, `[3]` e `[6 | 8]` con foglie `[5]`, `[7]`, `[9 | 10]`, dieci
    associazioni e altezza 2. La forma canonica del B-tree segue la variante
    con inserimento in foglia e divisioni dal basso del capitolo.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    for chiave in range(1, 11):
        albero.inserisci(chiave, f"dato-{chiave}")
    albero.controlla_invarianti()
    return albero


def _albero_da_radice(radice_voci, foglie_voci, tipo_chiave=int):
    """Assembla un B-tree di altezza 1 dalla radice e dalle foglie date."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=tipo_chiave)
    albero.radice = NodoBTree(list(radice_voci), [_foglia(foglia) for foglia in foglie_voci])
    albero.dimensione = len(radice_voci) + sum(len(foglia) for foglia in foglie_voci)
    albero.controlla_invarianti()
    return albero


def costruisci_d3b_iniziale():
    """Restituisce lo stato iniziale di D3b: prestito dal fratello destro."""
    return _albero_da_radice(_coppie_intere(20), [_coppie_intere(5), _coppie_intere(25, 30)])


def costruisci_d3c_iniziale():
    """Restituisce lo stato iniziale di D3c: prestito dal fratello sinistro."""
    return _albero_da_radice(_coppie_intere(20), [_coppie_intere(5, 10), _coppie_intere(25)])


def costruisci_d3d_iniziale():
    """Restituisce lo stato iniziale di D3d: fusione con il fratello sinistro."""
    return _albero_da_radice(
        _coppie_intere(10, 20),
        [_coppie_intere(5), _coppie_intere(15), _coppie_intere(25)],
    )


def costruisci_d3e_iniziale():
    """Restituisce lo stato iniziale di D3e: fusione fino alla radice foglia."""
    return _albero_da_radice(_coppie_intere(10), [_coppie_intere(5), _coppie_intere(15)])


def costruisci_d4_iniziale():
    """Restituisce lo stato iniziale di D4: fusione propagata fino alla radice.

    Lo stato stabile del B-tree ha grado minimo 2, sette chiavi e altezza 2:
    radice `[40]`, figlio `[20]` con foglie `[10]`, `[30]` e figlio `[60]` con
    foglie `[50]`, `[70]`.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    sinistro = NodoBTree(
        _coppie_intere(20), [_foglia(_coppie_intere(10)), _foglia(_coppie_intere(30))]
    )
    destro = NodoBTree(
        _coppie_intere(60), [_foglia(_coppie_intere(50)), _foglia(_coppie_intere(70))]
    )
    albero.radice = NodoBTree(_coppie_intere(40), [sinistro, destro])
    albero.dimensione = 7
    albero.controlla_invarianti()
    return albero


def costruisci_d5_iniziale():
    """Restituisce lo stato iniziale di D5: prestito fra nodi interni.

    Lo stato stabile del B-tree ha grado minimo 2 e altezza 2: radice `[40]`,
    figlio `[20 | 30]` con foglie `[10]`, `[25]`, `[35]` e figlio `[60]` con
    foglie `[50]`, `[70]`.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    sinistro = NodoBTree(
        _coppie_intere(20, 30),
        [_foglia(_coppie_intere(10)), _foglia(_coppie_intere(25)), _foglia(_coppie_intere(35))],
    )
    destro = NodoBTree(
        _coppie_intere(60), [_foglia(_coppie_intere(50)), _foglia(_coppie_intere(70))]
    )
    albero.radice = NodoBTree(_coppie_intere(40), [sinistro, destro])
    albero.dimensione = 9
    albero.controlla_invarianti()
    return albero


#: Record canonici D6: materiali con codice testuale univoco, descrizione e
#: quantità non negativa. I codici `"007"` e `"7"` sono chiavi distinte del
#: B-tree; l'ordine crescente delle chiavi è `003, 007, 012, 017, 021, 034,
#: 042, 7` secondo l'ordine lessicografico delle stringhe.
RECORD_D6 = (
    ("007", "cavetto USB", 4),
    ("012", "tastiera", 2),
    ("003", "mouse", 6),
    ("017", "webcam", 1),
    ("021", "adattatore", 3),
    ("034", "microfono", 2),
    ("7", "supporto", 5),
    ("042", "cuffie", 4),
)

#: Chiavi di D6 in ordine lessicografico crescente.
CHIAVI_D6_ORDINATE = ["003", "007", "012", "017", "021", "034", "042", "7"]
