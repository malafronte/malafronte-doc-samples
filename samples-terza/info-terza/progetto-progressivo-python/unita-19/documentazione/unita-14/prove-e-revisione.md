# Prove e revisione della tappa U14

Mappa dei test di
[`test_modello_u14.py`](../../programmi/test_modello_u14.py), diagnosi del
difetto emerso nella revisione e modifica breve del requisito con le parti
toccate. Documento di lavoro della milestone M54.

## Esecuzione

Dalla root del progetto:

```powershell
uv sync --frozen
uv run pytest -q
uv run pytest -q programmi/test_modello_u14.py
```

La suite cumulativa U5-U14 è la prova della regressione: nessun programma
delle tappe precedenti è cambiato.

## Mappa dei casi

| Caso | Test | Atteso verificato |
|---|---|---|
| PU14-01 | `test_pu14_01_uguaglianza_per_contenuto` | eq per contenuto, `is` distinto da `==`, campi distinti disuguali |
| PU14-02 | `test_pu14_02_zeri_codici_distinti` | totale zero e codici `007`/`7` distinti in ricerca, ordinamento ed esportazione |
| PU14-03 | `test_pu14_03_modifica_invalida_senza_effetti` | ultimo campo invalido: stato completo e ordine invariati |
| PU14-04 | `test_pu14_04_duplicato_e_sessioni` | duplicato con esito dichiarato; sessioni indipendenti |
| PU14-05 | `test_pu14_05_snapshot_e_alias` | snapshot protetto; effetti degli alias come documentato |
| PU14-06 | `test_pu14_06_salvataggio_e_ricostruzione` | valori, tipi e documento equivalenti; stesso JSON e stessa versione schema |
| PU14-07 | `test_pu14_07_corrotto_e_salvataggio_fallito` | politiche U12 conservate; nessuna perdita e nessun successo falso |
| PU14-08 | `test_pu14_08_risultati_storici` | riepilogo e viste uguali alla versione procedurale sullo stesso dataset |
| PR-14-1 | `test_proprio_sostituzione_atomica` | duplicati nella sostituzione rifiutano l'intera operazione |
| PR-14-2 | `test_proprio_dati_derivati_aggiornati` | le proprietà derived seguono lo stato senza duplicarlo |
| Modifica breve | `test_modifica_breve_per_destinazione` | selezione per destinazione validata, ordinata e protetta |

PR-14-1 nasce dal vincolo «tutto valido oppure nessun effetto» esteso alla
sostituzione dell'intero stato: il controllo dei duplicati deve precedere
l'assegnamento. PR-14-2 verifica che le proprietà non siano campi nascosti da
sincronizzare.

## Diagnosi di un difetto emerso nella revisione

**Sintomo.** Una prova di mutazione esterna — aggiungere un elemento alla
lista restituita da `preventivi()` — modificava la raccolta.

**Causa.** La prima versione restituiva direttamente il contenitore interno
(`return self._preventivi`). I valori frozen proteggono i campi degli
elementi, **non il contenitore che li raccoglie**: la distinzione fra
immutabilità del valore e protezione dello snapshot non era stata applicata
al percorso di lettura principale.

**Modifica minima.** Restituire `tuple(self._preventivi)` e dichiarare nel
contratto che lo snapshot è una tupla di valori frozen.

**Nuova prova.** PU14-05 controlla il tipo dello snapshot, l'impossibilità di
assegnare ai campi e la protezione della proiezione `per_lista()`; PR-14-1
ripete il controllo sul percorso della sostituzione. Il difetto insegna che
la protezione degli snapshot va verificata sul contenitore e sugli elementi,
come richiede il caso PU14-05.

## Modifica breve del requisito

**Requisito aggiunto.** «La raccolta deve poter elencare i preventivi di una
destinazione, per presentazioni e riepiloghi mirati.»

**Parti toccate.**

1. `registro_modello_u14.py`: nuovo metodo `per_destinazione(destinazione)`,
   con validazione della destinazione prima della ricerca e risultato come
   tupla protetta nell'ordine della raccolta;
2. `test_modello_u14.py`: nuovo test `test_modifica_breve_per_destinazione`
   con selezione multipla, selezione vuota e destinazione non ammessa;
3. questo documento, con la mappa aggiornata.

**Effetti sulla regressione.** Nessuno: l'operazione è aggiuntiva, la
rappresentazione interna non cambia e la suite cumulativa resta superata. La
scelta del risultato come tupla riusa la politica di protezione già adottata
per `preventivi()`: una modifica breve deve estendere il modello senza
aprire eccezioni alle sue regole.
