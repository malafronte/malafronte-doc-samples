# Prove e regressione — tappa U16

## Casi pubblici verificati

La suite `programmi/test_coda_richieste_u16.py` comprende 18 test: i casi
PU16-01-PU16-09 su entrambe le rappresentazioni della coda, più tre casi
propri motivati. I dati sono soltanto sintetici.

| Caso | Verifica effettuata | Esito |
|---|---|---|
| PU16-01 | Nessuna richiesta: `elabora_prossima` restituisce `None`, registro conservato | superato |
| PU16-02 | Ordine: R01 → `["007", "003"]`, R02 → `["003"]`, R03 → `["007", "012", "003"]` | superato |
| PU16-03 | Interleaving: R01/R02 accodate, R01 elaborata, R03 accodata; residuo `["R02", "R03"]` | superato |
| PU16-04 | Codici con zeri significativi e importo 0 ammesso dalla soglia ≥ 0 | superato |
| PU16-05 | Sostituzione: stesso client con `CodaDequeU16` e `CodaConcatenataU16`, esiti identici e `IndexError` sul vuoto | superato |
| PU16-06 | Richiesta invalida rifiutata prima dell'accodamento; contenuto e dimensione conservati | superato |
| PU16-07 | Registro vuoto: richieste valide producono tuple vuote e si completano in ordine | superato |
| PU16-08 | Uno, vuoto, reinserimento: estrazione dell'unica richiesta e nuovo inserimento corretto | superato |
| PU16-09 | Conservazione: dati, ordine e schema dell'archivio invariati dalla consultazione | superato |

## Casi propri motivati

1. **Confine della soglia** (`test_caso_proprio_confine_della_soglia`): la
   soglia 450 uguale al totale di `007` lo ammette insieme a `003`. Il caso
   fissa il confine `>=` di `PoliticaSoglia` già studiato in U15.
2. **Difetto plausibile** (`test_caso_proprio_difetto_plausibile_conserva_la_richiesta`):
   un criterio che restituisce `"sì"`/`"no"` invece di `bool` fa sollevare
   `TypeError` durante il calcolo; la richiesta **resta al fronte** e la coda
   conserva entrambi gli elementi. Il caso verifica la sequenza fronte,
   calcolo, estrazione.
3. **Richiesta ripetuta** (`test_caso_proprio_richiesta_ripetuta`): due
   richieste con lo stesso codice `R01` e criteri diversi sono valori distinti,
   vengono elaborate entrambe nell'ordine di arrivo e producono esiti diversi.

## Diagnosi di due difetti verificati durante lo sviluppo

- **Estrazione prima del calcolo**: la versione iniziale del servizio estraeva
  la richiesta e poi calcolava l'esito; un criterio difettoso perdeva la
  richiesta. La prova del caso proprio 2 cattura il difetto: la modifica minima
  inverte le due fasi, e la richiesta resta disponibile al fronte.
- **Ispezione della coda vuota**: `pendenti()` su `CodaDequeU16` richiede
  l'ispezione della rappresentazione interna, mentre la coda concatenata
  espone `per_lista()`; la differenza è documentata come strumento di prova e
  non fa parte del contratto pubblico della coda.

## Regressione U5-U15 (PU16-10)

La suite cumulativa copre i contratti mantenuti dalle tappe precedenti: i
criteri U15 non cambiano firma né comportamento, `seleziona_codici` conserva le
proprie promesse e la suite U5-U15 supera per intero.

```text
> uv run --frozen pytest -q
........................................................................ [ 39%]
........................................................................ [ 79%]
......................................                                   [100%]
182 passed in 0.82s
```

**182 test**: 164 delle tappe U5-U15 più 18 della tappa U16. La regressione è
stata eseguita ricostruendo l'ambiente dal lock con `uv sync --frozen`, come
dichiarato nel README della fotografia.

## Limiti dichiarati

Le richieste pendenti sono stato in memoria: la persistenza della coda è
un'estensione con schema separato e prove proprie. La suite verifica il dominio
senza CLI; l'esecuzione reale del punto di avvio è documentata nel README con
il dataset pubblicato, identica con le due rappresentazioni.
