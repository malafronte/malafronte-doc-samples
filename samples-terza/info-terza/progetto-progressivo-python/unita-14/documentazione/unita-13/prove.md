# Prove della tappa U13

Mappa dei test di
[`test_oggetti_u13.py`](../../programmi/test_oggetti_u13.py),
diagnosi del difetto emerso durante la rifattorizzazione e modifica breve del
requisito con le parti toccate. Documento di lavoro della milestone M51.

## Esecuzione

Dalla root del progetto:

```powershell
uv sync --frozen
uv run pytest -q
uv run pytest -q programmi/test_oggetti_u13.py
```

La suite cumulativa U5-U13 è la prova della regressione: i programmi delle
tappe precedenti non sono cambiati e i loro test restano gli stessi.

## Mappa dei casi

| Caso | Test | Atteso verificato |
|---|---|---|
| PU13-01 | `test_pu13_01_due_registri_indipendenti` | modificare la prima sessione non cambia la seconda; nessun contenitore condiviso |
| PU13-02 | `test_pu13_02_codici_distinti` | `007` e `7` distinti in memoria, ricerca ed esportazione |
| PU13-03 | `test_pu13_03_totale_zero_e_destinazione_valida` | totale zero accettato e conservato nel round-trip e nel riepilogo |
| PU13-04 | `test_pu13_04_rifiuti_senza_effetti` | duplicato e aggiornamenti invalidi con esito `False` e stato interamente conservato |
| PU13-05 | `test_pu13_05_salvataggio_e_ricarico` | dati equivalenti e ordine conservato dopo salvataggio e nuovo caricamento; nuove istanze |
| PU13-06 | `test_pu13_06_archivio_corrotto_e_guasto` | esito `sintassi` distinto; guasto di scrittura con file precedente identico nei byte e temporaneo eliminato |
| PU13-07 | `test_pu13_07_riepilogo_equivalente` | riepilogo uguale a quello procedurale sullo stesso dataset |
| PU13-08 | `test_pu13_08_snapshot_protetto` | modificare snapshot o record consultati non tocca la sessione |
| PR-13-1 | `test_proprio_sostituzione_indipendente` | la lista passata a `sostituisci_da_lista` resta autonoma anche se il chiamante la modifica |
| PR-13-2 | `test_proprio_conversione_sempre_nuova` | ogni `per_lista()` produce contenitori nuovi, mai gli stessi |
| Modifica breve | `test_modifica_breve_totale_complessivo` | somma dei totali derivata, sessione invariata |

PR-13-1 nasce da un caso che la consegna non elenca ma che la politica di
copia implica: la sostituzione non può lasciare il proprio stato legato alla
lista del chiamante. PR-13-2 verifica la stessa politica sul percorso
opposto, quello delle osservazioni.

## Diagnosi di un difetto emerso durante la rifattorizzazione

**Sintomo.** PR-13-1 falliva: dopo `sostituisci_da_lista(esterna)` e la
modifica di `esterna[0]["totale_cent"]`, la sessione mostrava il valore nuovo.

**Causa.** La prima versione del metodo assegnava la lista ricevuta allo
stato: `self._preventivi = registro`. La classe copiava i contenitori delle
osservazioni ma non quelli delle conversioni in ingresso, quindi due
percorsi della stessa operazione avevano politiche diverse.

**Modifica minima.** Copiare ogni record prima dell'assegnamento, come già
faceva `per_lista()`, e dichiarare la politica di copia nel contratto del
metodo.

**Nuova prova.** PR-13-1 modifica la lista esterna dopo la sostituzione e
controlla lo stato; PU13-08 ripete il controllo sul percorso delle
osservazioni. Il difetto insegna che la politica di copia va verificata su
entrambi i confini della rappresentazione — ingresso e uscita — e non solo su
quello più visibile.

## Modifica breve del requisito

**Requisito aggiunto.** «La sessione deve poter indicare il totale complessivo
dei preventivi in centesimi, per presentarlo accanto al riepilogo per
destinazione.»

**Parti toccate.**

1. `registro_oggetti_u13.py`: nuovo metodo `totale_complessivo_cent()`, che
   somma i `totale_cent` dei record già validati — nessun campo duplicato,
   nessun effetto sullo stato;
2. `registro_cli_u13.py`: il comando `elenco` presenta anche il totale
   complessivo in euro, accanto al riepilogo storico;
3. `test_oggetti_u13.py`: nuovo test `test_modifica_breve_totale_complessivo`
   su sessione vuota e sulla sessione canonica.

**Effetti sulla regressione.** Nessuno: l'operazione è aggiuntiva, i contratti
esistenti non cambiano e la suite cumulativa resta superata. La modifica è
esemplificativa: mostra che il modello accetta estensioni locali senza
ritoccare dominio, persistenza né le funzioni storiche.
