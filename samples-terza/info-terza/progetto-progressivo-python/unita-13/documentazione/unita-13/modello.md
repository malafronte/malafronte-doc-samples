# Modello a oggetti del registro — U13

Specifica del comportamento conservato, dello stato, degli invarianti e
dell'interfaccia della classe `RegistroPreventivi` di
[`registro_oggetti_u13.py`](../../programmi/registro_oggetti_u13.py).
Documento di lavoro della milestone M49, affiancato da
[`confronto.md`](confronto.md) e [`prove.md`](prove.md).

## Comportamento conservato

La variante non cambia né i dati né gli esiti già accertati:

- record con `codice` stringa a zeri significativi, `destinazione` fra `locale`
  e `nazionale`, `totale_cent` intero non negativo in centesimi;
- schema JSON canonico `{"versione_schema": 1, "preventivi": [...]}`, CSV di
  consultazione con le stesse colonne, tariffe, riepiloghi, viste e politiche
  di persistenza U12 invariati;
- rifiuti senza effetti parziali: un inserimento, un aggiornamento o una
  sostituzione non riusciti lasciano la sessione esattamente com'era;
- esito booleano dichiarato per inserimento, aggiornamento ed eliminazione:
  `False` significa «nessuna modifica avvenuta», non un errore di runtime.

## Stato della sessione e invarianti

Lo **stato** di una sessione è la lista dei preventivi inseriti o caricati
durante la sessione stessa. L'**invariante** è quello già verificato da
`valida_registro`: ogni record è nel dominio e i codici sono unici con
confronto esatto, quindi `"007"` e `"7"` restano due preventivi distinti.

Gli invarianti si conservano perché ogni modifica passa dalle operazioni di
`registro_dominio.py`, che validano il candidato completo prima di ogni
scrittura. La classe non aggiunge campi duplicati: conteggi e totali si
derivano dai record quando servono.

## Responsabilità

| Componente | Responsabilità | Che cosa non fa |
|---|---|---|
| `registro_oggetti_u13.py` | conserva lo stato della sessione, offre le operazioni, decide la politica di copia | non legge né scrive file, non stampa |
| `registro_dominio.py` | schema, validazione, operazioni sulle liste | non conserva stato di sessione |
| `registro_persistenza.py` | JSON canonico, salvataggio protetto, CSV | non conosce la classe |
| `registro_cli_u13.py` | interazione, modifiche pendenti, presentazione degli esiti | non contiene regole di dominio |

La dipendenza va in una sola direzione: la classe usa il dominio, la CLI usa
classe e persistenza, nessun modulo importa la CLI.

## Interfaccia della classe

| Operazione | Contratto |
|---|---|
| `RegistroPreventivi()` | istanza vuota, stato proprio, nessun contenitore condiviso fra istanze |
| `numero()` | intero: quanti preventivi contiene la sessione |
| `inserisci(codice, destinazione, totale_cent)` | `True` se aggiunge in coda; `False` senza effetti con dati fuori dominio o codice già presente |
| `aggiorna(codice, destinazione, totale_cent)` | `True` se sostituisce destinazione e totale del codice; `False` senza effetti con codice assente o dati non ammessi |
| `elimina(codice)` | `True` se rimuove il record; `False` se il codice è assente |
| `cerca(codice)` | copia del record del codice, oppure `None`; la copia è indipendente dallo stato |
| `per_lista()` | lista nuova di record nuovi, nell'ordine della sessione: conversione esplicita verso persistenza e funzioni storiche |
| `sostituisci_da_lista(registro)` | `True` sostituendo l'intero stato con una lista valida; `False` senza effetti se anche un solo record non è ammesso |
| `riepilogo_per_destinazione()` | contratto storico del riepilogo, applicato allo stato senza esporlo |
| `totale_complessivo_cent()` | somma dei totali in centesimi, derivata dai record (modifica breve) |

## Scelte di modellazione

- **La classe è quella del registro, non quella del preventivo.** Il requisito
  chiede un'entità con stato utile: lo stato della sessione è la lista dei
  preventivi. Un oggetto `Preventivo` con tre campi invariabili aggiungerebbe
  un passaggio di conversione senza cambiare comportamento osservabile: il
  record resta un dizionario e la classe del singolo preventivo andrebbe
  giustificata separatamente, come richiede la consegna.
- **I rifiuti sono booleani dichiarati.** Le eccezioni di dominio sono
  strumento dell'Unità 14: qui gli esiti coincidono con quelli già verificati
  e il confronto prima/dopo resta diretto.
- **Le osservazioni restituiscono copie.** `cerca()` e `per_lista()` producono
  dizionari nuovi: nessun alias del chiamante raggiunge i contenitori interni
  e la politica di copia è verificata dai casi PU13-08 e PR-13-1, PR-13-2.
