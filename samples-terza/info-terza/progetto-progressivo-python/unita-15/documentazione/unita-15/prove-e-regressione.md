# Prove e regressione della tappa U15

Suite condivisa e test specifici di
[`test_consultazione_u15.py`](../../programmi/test_consultazione_u15.py),
casi propri motivati, diagnosi del difetto emerso e variante breve con le
parti toccate. Documento di lavoro della milestone M57.

## Esecuzione

Dalla root del progetto:

```powershell
uv sync --frozen
uv run pytest -q
uv run pytest -q programmi/test_consultazione_u15.py
```

## Suite condivisa e test specifici

La **suite condivisa** verifica le promesse del contratto comune su entrambe
le implementazioni principali, con parametrizzazione: lista nuova, ordine
della raccolta conservato, registro invariato, ripetibilità
(`test_promise_comuni`), vuoto valido senza chiamate al criterio
(`test_pu15_01_vuoto_valido`). I **test specifici** verificano la semantica di
ciascuna regola: `test_pu15_04_risultati_specifici` fissa gli attesi dei due
criteri sul dataset pubblicato e `test_pu15_08_nuova_implementazione` quelli
della variante. La distinzione è la stessa della teoria: le promesse comuni
rendono i componenti sostituibili, gli attesi specifici distinguono le regole.

## Mappa dei casi pubblici

| Caso | Test | Atteso verificato |
|---|---|---|
| PU15-01 | `test_pu15_01_vuoto_valido` | selezione vuota coerente, stato conservato, nessuna chiamata inutile |
| PU15-02 | `test_pu15_02_e_05_invarianti` | `007` conserva gli zeri; totale zero ammesso dalla soglia 0 |
| PU15-03 | `test_pu15_03_sostituzione` | due implementazioni, stessa chiamata, promesse comuni |
| PU15-04 | `test_pu15_04_risultati_specifici` | locale → `["007", "003"]`; soglia ≥ 500 → `["003"]`; attesi della variante |
| PU15-05 | `test_pu15_02_e_05_invarianti` | record, ordine e identità di dominio conservati; risultato mutabile protetto |
| PU15-06 | `test_pu15_06_configurazione_invalida` | `ErroreConfigurazione` prima di ogni effetto sul registro |
| PU15-07 | `test_pu15_07_guasto_senza_successo` | guasto in scansione: stato conservato, nessun risultato parziale, nessun successo |
| PU15-08 | `test_pu15_08_nuova_implementazione` | nuova implementazione integrata dallo stesso client, modifiche circoscritte |
| PU15-09 | `uv run pytest -q` | regressione U5-U14: 159 test cumulativi superati |
| PU15-10 | intera suite | dominio provabile senza CLI né file; UML in `diagramma.puml` |

## Casi propri motivati

- **Confine** (`test_proprio_confine_della_soglia`): la soglia 450 ammette
  `007` con `PoliticaSoglia` e lo esclude con `PoliticaSogliaEsclusiva`;
  1200 è ammesso dalla soglia uguale. Il confine incluso/escluso è la
  differenza minima fra due regole apparentemente simili.
- **Difetto plausibile** (`test_proprio_difetti_plausibili`): due criteri con
  decisione corretta ma risultato di tipo sbagliato — testo `"sì"`/`"no"` e
  interi `1`/`0`. Il difetto è plausibile perché entrambi i valori sono
  utilizzabili in un `if`: la guardia sul `bool` esatto e la prova lo rendono
  visibile.
- **Conservazione dello stato** (`test_proprio_ripetibilita_e_stato`): due
  consultazioni consecutive sullo stesso criterio producono gli stessi codici
  e la proiezione `per_lista()` resta identica: la consultazione non ha
  effetti cumulativi nascosti.

## Diagnosi di un difetto emerso

**Sintomo.** Un criterio che restituiva `"no"` per gli esclusi includeva
comunque tutti i preventivi.

**Causa.** Il client usava `if ammesso:` — la verità del valore, non il
`bool` atteso. Una stringa non vuota è «veritiera»: il difetto di tipo
diventava un difetto di risultato senza alcuna eccezione.

**Modifica minima.** Introdurre la guardia `type(ammesso) is not bool` con
`TypeError`, come nel client degli esempi U15, e dichiarare la promessa nel
contratto.

**Nuova prova.** `test_proprio_difetti_plausibili` riproduce entrambe le
varianti del difetto; la suite condivisa verifica che i criteri corretti
superino la stessa guardia. La lezione è che il tipo del risultato è una
promessa del contratto, non un dettaglio: la verità di un valore non
sostituisce il tipo dichiarato.

## Variante breve e parti toccate

**Variante.** `PoliticaSogliaEsclusiva`: la stessa soglia con confronto
strettamente maggiore. Il caso PU15-08 mostra l'integrazione di una nuova
implementazione tramite il contratto.

**Parti toccate.**

1. `registro_consultazione_u15.py`: nuova classe con la stessa interfaccia e
   la stessa validazione della configurazione — nessuna modifica al client;
2. `consultazione_cli_u15.py`: la sola scelta concreta accoglie
   `soglia-esclusiva`; il resto del punto di avvio è invariato;
3. `test_consultazione_u15.py`: attesi specifici della variante nei test di
   confine e di nuova implementazione;
4. `diagramma.puml`: terzo componente nella famiglia dei criteri.

**Effetti sulla regressione.** Nessuno: il client, il modello U14, la
persistenza e le funzioni storiche non cambiano; la suite cumulativa resta
superata. Il diff della variante è circoscrito al componente e alla scelta
del punto di avvio, come richiede PU15-08.

## Strategia di regressione

La regressione U5-U14 si verifica con la suite cumulativa: i contratti
conservati — schema, tariffe, riepiloghi, viste, persistenza — hanno i propri
test storici, che non sono stati toccati. Gli adattamenti interni della tappa
sono nulli: la consultazione è aggiuntiva e lavora sulle proiezioni già
verificate del modello U14.
