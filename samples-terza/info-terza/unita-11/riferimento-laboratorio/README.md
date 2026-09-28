# Riferimento del LAB-PY-U11

Controparti complete e verificate dello starter del LAB-PY-U11 - Estendere e
verificare il confronto. Si leggono **dopo** le fasi L2-L3, come confronto
formativo: le scelte di dettaglio non sono l'unica soluzione possibile e il
confronto riguarda invariante della fusione, condizioni di scambio della
partizione, ordine delle chiamate ricorsive e confini delle regioni cronometrate.

| File | Contenuto |
|---|---|
| `ordinamenti_u11.py` | `fondi_ordinate`, `merge_sort`, `partiziona_lomuto`, `quick_sort` completi |
| `conteggi_u11.py` | le quattro varianti strumentate complete, con le formule attese |
| `dataset_u11.py` | cinque famiglie di input, identico allo starter |
| `ordinamenti_elementari_u11.py` | i quattro ordinamenti del cap. PY-14, identico allo starter |
| `ricerche_u11.py` | ricerca lineare e dicotomica, identico allo starter |
| `misure_u11.py` | protocollo di misura completo, comprese le due regioni cronometrate |
| `test_ordinamenti_u11.py` | la stessa suite pubblica, con il caso L12 compilato e motivato |

La suite del riferimento è verde per intero: 66 test. Con lo starter gli stessi
casi danno 6 passaggi e 60 fallimenti attesi, tutti sui `NotImplementedError`
delle fasi dichiarate.

Esecuzione dalla cartella `unita-11/`, **una suite alla volta** per la collisione
dei nomi dei moduli:

```powershell
uv run --with pytest python -m pytest riferimento-laboratorio/test_ordinamenti_u11.py -q
```

Il caso L12 del riferimento è un esempio di caso progettato, non la soluzione
obbligatoria: la consegna chiede un caso proprio che discrimini un difetto non
ancora coperto, con la previsione dei contatori e la spiegazione di che cosa
distingue.
