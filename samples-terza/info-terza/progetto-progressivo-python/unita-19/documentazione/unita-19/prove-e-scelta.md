# Prove e scelta - tappa U19

## Casi PU19-01-PU19-10

| Caso | Dato o operazione | Risultato richiesto |
|---|---|---|
| PU19-01 | Registro vuoto | Indice vuoto, intervallo vuoto, `cerca` con `KeyError`, `contiene` con `False` |
| PU19-02 | Codici `007`, `012`, `003` | Stessi codice, destinazione e importo del registro |
| PU19-03 | Codici `007` e `7` | Chiavi distinte consultabili separatamente |
| PU19-04 | Dataset con `007` ripetuto | `ValueError`, sorgente conservata |
| PU19-05 | Query `000`, `999`, `014` | `KeyError` con la politica documentata |
| PU19-06 | Vista e intervalli | Stesso ordine e stesso intervallo; vuoto valido e invertito distinti |
| PU19-07 | Otto codici sintetici | Split avvenuto, voce interna consultabile, invarianti verificati |
| PU19-08 | Inserimento di `021` dopo la costruzione | Vecchia fotografia senza `021`, nuova con `021` |
| PU19-09 | Stesse query su cinque strutture | Esiti equivalenti con 20 righe verificate |
| PU19-10 | Salvataggio, tariffe, coda, BST e hash | Caricamento e contratti precedenti verificati con la novità |

## Tre casi propri

1. **Confine `007` e `7` con intervallo**: i due codici restano distinti
   anche nell'intervallo `007..7`, che li contiene entrambi con `012` in
   mezzo; la conversione in intero li confonderebbe.
2. **Difetto plausibile con oracolo `dict`**: sei codici con confronto di
   ogni voce contro il dizionario di riferimento e fotografia ordinata pari
   all'ordinamento; invarianti verificati alla fine della sequenza.
3. **Ciclo di vita della fotografia**: aggiornamento di `007` da 450 a 500
   centesimi; la fotografia precedente restituisce ancora 450, la nuova 500.

## Scelta motivata del dossier

Per il carico dichiarato — query esatte ripetute con viste ordinate
occasionali — il rapporto motiva la convivenza: l'indice hash U18 serve le
query esatte con costo atteso, l'indice B-tree U19 serve esatte, ordinate e
intervalli con percorso logaritmico e conteggi dichiarati. L'alternativa a
struttura singola perde una delle due proprietà: la scansione non scala, la
lista ordinata paga gli aggiornamenti, il BST degenera senza
ribilanciamento. Il limite del dossier è il modello a blocchi simulato: i
trasferimenti sono conteggi del modello, non misure del supporto.

## Regressione

La suite cumulativa conserva tutte le tappe precedenti con i contratti
mantenuti: tariffe U5, sintesi U7, registro U8, costi U9, viste U10,
ordinamenti U11, persistenza U12, oggetti U13, modello U14, consultazione
U15, coda U16, BST U17 e hash U18. Il conteggio cumulativo dei test è
ricavato dalla nuova suite al momento della consegna.
