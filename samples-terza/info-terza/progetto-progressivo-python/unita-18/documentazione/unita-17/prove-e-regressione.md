# Prove e regressione — tappa U17

## Casi pubblici verificati

La suite `programmi/test_indice_bst_u17.py` comprende 20 test: i casi
PU17-01-PU17-10 sul dominio dell'indice, più tre casi propri motivati. I dati
sono soltanto sintetici; la regressione di persistenza usa file temporanei.

| Caso | Verifica effettuata | Esito |
|---|---|---|
| PU17-01 | Vista inordine `["003", "007", "012"]`, raccolta `["007", "012", "003"]` conservata, estremi e invarianti | superato |
| PU17-02 | Ricerca esatta: `007` → `locale`/450, `012` → importo 0, zeri significativi conservati | superato |
| PU17-03 | Assenza di `"999"` con `KeyError`; indice vuoto con query vuote, altezza -1 e `IndexError` sugli estremi | superato |
| PU17-04 | Intervallo `["003", "007"]` → record 003 e 007 in ordine; `["007", "007"]` → il solo 007 | superato |
| PU17-05 | Intervallo senza risultati, estremi assenti, estremi invertiti e chiavi invalide secondo il contratto locale | superato |
| PU17-06 | Sorgente con codice ripetuto rifiutata da `costruisci_indice` e da `misura_costruzione`; record non ammesso rifiutato; nessun indice parziale consegnato | superato |
| PU17-07 | Fotografia vecchia a 450 e indice ricostruito a 500 dopo l'aggiornamento; codice `"007"` identico nei due indici | superato |
| PU17-08 | Cancellazione di foglia, nodo con un figlio e nodo con due figli e successore con figlio; associazioni codice-record preservate | superato |
| PU17-09 | Altezza 6 contro 2 e nodi esaminati 21 contro 10 nella costruzione; ricerche 7 contro 3 con costo separato | superato |
| PU17-10 | Regressione: registro e ordini, schema JSON e CSV, tariffe U3/U5 e FIFO della coda U16 | superato |

## Casi propri motivati

1. **Ordine lessicografico di codici di lunghezza diversa**
   (`test_caso_proprio_ordine_lessicografico_di_codici_di_lunghezza_diversa`):
   i codici `"007"` e `"7"` sono chiavi diverse, `"10"` precede `"9"` e il
   minimo dell'indice è `"007"`. Il caso fissa la regola dichiarata dell'ordine
   lessicografico, che con lunghezze diverse non coincide con l'ordine
   numerico.
2. **Difetto plausibile confrontato con un oracolo `dict`**
   (`test_caso_proprio_oracolo_dict_su_operazioni_miste`): una sequenza mista
   di inserimenti, aggiornamenti e cancellazioni viene confrontata, dopo ogni
   modifica, con un oracolo `dict` su dimensione, coppie ordinate e risultati
   delle ricerche. Il difetto temuto è il record trasferito sotto la chiave
   sbagliata: un inordine ordinato da solo non lo rivela.
3. **Fotografia conservata dopo un'eliminazione**
   (`test_caso_proprio_fotografia_conservata_dopo_eliminazione`): dopo
   `elimina("012")` il primo indice conserva ancora `012` e il secondo no; le
   interrogazioni non modificano né l'indice né la raccolta del registro.

## Difetti plausibili che le prove rilevano

Le due mutazioni seguenti sono state applicate al sorgente una alla volta,
osservate sulla suite e poi annullate; documentano quali prove rilevano il
difetto corrispondente.

- **Record del successore non trasferito**: nella cancellazione con due figli,
  la mutazione trasferiva la sola chiave del successore inordine e lasciava il
  record precedente. Il difetto è rilevato da
  `test_pu17_08_cancellazione_con_due_figli_e_successore_con_figlio`, che
  confronta ogni coppia codice-record con il proprio valore sintetico, e dal
  caso proprio 2, che dopo la rimozione di `004` osserva `005` associato al
  record di `004`. La modifica minima trasferisce chiave e record insieme.
- **Estremi dell'intervallo esclusi**: la mutazione sostituiva il confronto
  inclusivo `minimo <= codice <= massimo` con uno stretto. Il difetto è
  rilevato da `test_pu17_04_intervallo_inclusivo_agli_estremi`, che si aspetta
  `003` e `007` nell'intervallo con gli stessi estremi; il caso proprio 1
  controlla inoltre un intervallo con estremi assenti e risultati interni.

## Regressione U5-U16 (PU17-10)

La suite cumulativa copre i contratti mantenuti dalle tappe precedenti: il
modello U14 conserva valori immutabili e proiezioni protette, la persistenza
U12 mantiene schema JSON e CSV, le tariffe U3/U5 restano invariate, l'ordine
della raccolta è quello di inserimento e la coda U16 elabora le richieste
nell'ordine di arrivo.

```text
> uv run --frozen pytest -q
........................................................................ [ 35%]
........................................................................ [ 71%]
..........................................................               [100%]
202 passed in 0.47s
```

**202 test**: 182 delle tappe U5-U16 più 20 della tappa U17. La regressione è
stata eseguita ricostruendo l'ambiente dal lock con `uv sync`, come dichiarato
nel README della fotografia.

## Limiti dichiarati

La suite verifica il dominio dell'indice senza CLI; l'esecuzione reale del
punto di avvio è documentata nel README con il dataset pubblicato. L'indice
rappresenta la fotografia del momento della costruzione: ogni modifica del
registro richiede una nuova costruzione e la coerenza fra le due raccolte non
è sincronizzata automaticamente. I conteggi dei nodi esaminati riguardano le
chiavi lette e non includono il costo dei confronti fra testi.
