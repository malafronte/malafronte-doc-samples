"""Dimostrazione delle ricerche sul B-tree D1 — Unità 19 (cap. PY-35).

Lo script ricostruisce il B-tree D1 con tutte le coppie, esegue le cinque
query canoniche del capitolo (`20`, `17`, `15`, `4`, `40`) con la ricerca
strumentata e stampa per ciascuna percorso dei nodi del B-tree, esito e
contatori. Mostra inoltre il caso del B-tree vuoto e di una radice foglia
singola. Esecuzione dalla cartella `unita-19`:

```powershell
uv run python esempi/dimostrazione_ricerca_u19.py
```

Ambiente: CPython sul computer.
"""

from btree_modello_u19 import BTreeDidattico
from dati_btree_u19 import costruisci_d1


def main():
    """Esegue le query canoniche su D1 e stampa percorsi ed esiti."""
    albero = costruisci_d1()
    print("D1: radice [10 | 20], figli [5 | 6 | 7], [12 | 17], [30]")
    for query in (20, 17, 15, 4, 40):
        esito = albero.ricerca_con_conteggi(query)
        print(
            f"query {query}: trovato={esito.trovato} dato={esito.dato} "
            f"nodi={esito.nodi} confronti={esito.confronti} "
            f"(ordine={esito.confronti_ordine}, uguaglianza={esito.confronti_uguaglianza})"
        )
    vuoto = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    print(f"vuoto: altezza={vuoto.altezza()} contiene(1)={vuoto.contiene(1)}")
    singolo = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    singolo.inserisci(10, "dato-10")
    print(f"radice foglia: altezza={singolo.altezza()} cerca(10)={singolo.cerca(10)!r}")


if __name__ == "__main__":
    main()
