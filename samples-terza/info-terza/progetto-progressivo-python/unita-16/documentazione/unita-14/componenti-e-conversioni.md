# Componenti, conversioni e raccordo con CLI, CSV e JSON — U14

Responsabilità della raccolta, proiezioni esplicite e integrazione con
persistenza e interazione. Documento di lavoro della milestone M53,
affiancato da [`contratti-e-rappresentazione.md`](contratti-e-rappresentazione.md).

## Responsabilità individuali e responsabilità dell'insieme

Il **valore** `Preventivo` controlla i propri campi: non può conoscere le
altre istanze e rifiuta alla costruzione ogni candidato fuori dominio. La
**raccolta** `RegistroPreventivi` mantiene le regole che vedono l'intero
insieme: unicità dei codici, ordine, sostituzione atomica dell'intero stato.
Un duplicato è quindi un errore della raccolta (`CodiceDuplicato`), un dato
fuori dominio è un errore del valore (`DatoNonAmmesso`): le due diagnosi non
si confondono e la CLI le presenta distintamente.

## API della raccolta

| Operazione | Risultato ed effetti |
|---|---|
| `inserisci(codice, destinazione, totale_cent)` | costruisce il valore e lo aggiunge in coda; restituisce il valore creato; rifiuta con eccezione e nessun effetto |
| `aggiorna(codice, destinazione, totale_cent)` | costruisce e valida il candidato completo, poi sostituisce il valore nella posizione del codice; ordine invariato |
| `elimina(codice)` | rimuove il valore del codice; `CodiceAssente` se manca |
| `per_codice(codice)` | valore del codice oppure `None`; confronto esatto |
| `per_destinazione(destinazione)` | tupla dei valori della destinazione, nell'ordine (modifica breve) |
| `preventivi()` | snapshot: tupla protetta di valori frozen |
| `per_lista()` | proiezione: lista nuova di record nuovi dello schema |
| `sostituisci_da_lista(registro)` | sostituzione atomica dell'intero stato; eccezione senza effetti sul primo problema |
| `riepilogo_per_destinazione()` | contratto storico, applicato alla proiezione |

## Proiezioni esplicite verso CSV e JSON

Le conversioni sono operazioni nominate — `per_lista()`,
`record_da_preventivo()`, `preventivo_da_record()` — non l'esportazione
opaca degli attributi: nessun `vars()`, nessun `pickle`, nessun oggetto del
modello che si serializza da solo. `registro_persistenza.py` non cambia:
riceve e restituisce liste di record e mantiene schema JSON canonico,
salvataggio protetto e CSV di consultazione.

La dipendenza va in una sola direzione: modello ← persistenza non esiste, è
la CLI a comporre le due mediante le proiezioni. Il round-trip è verificato
in PU14-06: valori, tipi e documento coincidono dopo salvataggio e
ricostruzione, con nuove istanze.

## Raccordo con la CLI

`registro_cli_u14.py` è il **confine degli errori**: traduce le eccezioni di
dominio in messaggi e decide gli esiti della sessione. Nessun `except`
indiscriminato — ciascuna eccezione ha la propria diagnosi — e nessuna regola
di dominio vive nell'interazione. I comportamenti di sessione restano quelli
già verificati: inizializzazione con `carica`, modifiche pendenti solo per le
operazioni riuscite, salvataggio esplicito, EOF gestito.

## Effetti sugli alias, in sintesi

- I valori sono frozen: chi ne conserva uno non può modificarlo.
- `aggiorna` sostituisce il valore: il riferimento precedente resta valido e
  invariato, la raccolta espone il valore nuovo.
- `per_lista()` produce record nuovi: la loro modifica non tocca la raccolta.
- `preventivi()` produce una tupla: né il contenitore né gli elementi sono
  modificabili dal ricevente.
