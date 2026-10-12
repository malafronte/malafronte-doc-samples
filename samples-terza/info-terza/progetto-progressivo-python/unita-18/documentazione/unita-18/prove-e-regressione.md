# Prove e regressione - tappa U18

## Casi PU18-01–PU18-12

| Caso | Dato o operazione | Risultato richiesto |
|---|---|---|
| PU18-01 | Registro vuoto | Indice vuoto, `cerca` con `KeyError`, `contiene` con `False` |
| PU18-02 | Codice `007` | Zeri conservati, record `007/locale/450`, hash 47671 |
| PU18-03 | Codici `012`, `003`, `017` in collisione | Tre associazioni consultabili separatamente |
| PU18-04 | Dataset con `007` ripetuto | `ValueError`, sorgente conservata |
| PU18-05 | Tre query nella stessa fotografia | Record corretti, registro e indice conservati |
| PU18-06 | Query `999` | `KeyError` senza confondersi con un valore valido |
| PU18-07 | Dodici codici sintetici | Capacità 20, dodici voci, associazioni conservate |
| PU18-08 | Inserimento di `021` dopo la costruzione | Vecchia fotografia senza `021`, nuova con `021` |
| PU18-09 | Salvataggio e caricamento | Codici e valori conservati; indice ricostruito dopo il caricamento |
| PU18-10 | Stesse query su hash, BST e scansione | Stesso record sulle query esatte ammesse |
| PU18-11 | Tariffe, formato euro, coda U16 | Esiti di regressione U5–U16 conservati |
| PU18-12 | Conteggi e carico | Confronti nella catena, carico `3 / m`, fotografia di tre voci |

## Tre casi propri

1. **Confine `007` e `7`**: i due codici sono chiavi diverse e restano
   consultabili separatamente; la conversione in intero li confonderebbe.
2. **Difetto plausibile con oracolo `dict`**: rimozione di `017`, inserimento
   di `042` e confronto di ogni voce con il dizionario di riferimento;
   invarianti verificati alla fine della sequenza.
3. **Ciclo di vita della fotografia**: aggiornamento di `007` da 450 a 500
   centesimi; la fotografia precedente restituisce ancora 450, la nuova 500.

## Regressione

La suite `programmi/test_indice_hash_u18.py` (15 test) copre i dodici casi
pubblici e i tre casi propri. La regressione delle tappe precedenti usa i
contratti reali: tariffe U3/U5, formato degli importi, coda di richieste U16
con elaborazione nell'ordine di arrivo, schema JSON e CSV U12. La suite
cumulativa U5–U18 si esegue con `uv run pytest -q programmi/` dalla root del
progetto.

## Confronto con la tappa U17

La fotografia U18 conserva tutti i programmi U1–U17 invariati e aggiunge
`programmi/indice_hash_u18.py`, `programmi/indice_cli_u18.py` e
`programmi/test_indice_hash_u18.py` con questa documentazione. Le differenze
rispetto all'indice BST sono la ricerca esatta senza intervalli, la crescita
per raddoppio oltre la soglia 1.0 e la fotografia ordinata come vista di
presentazione. Il punto di avvio `indice_cli_u18.py` indirizza le query
d'intervallo allo strumento della tappa precedente.
