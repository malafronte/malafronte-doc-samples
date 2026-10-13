# Contratti e scelta della struttura — tappa U16

## Richieste di consultazione

`RichiestaConsultazione(codice, criterio)` è un valore immutabile che
descrive **che cosa consultare**. Il `codice` è una stringa non vuota che
identifica la richiesta; il `criterio` espone `ammette(preventivo) -> bool` e
`descrizione() -> str`, lo stesso contratto dei criteri intercambiabili della
tappa U15. Una richiesta invalida viene rifiutata **prima** dell'accodamento:
tipo errato → `TypeError`, campo fuori dominio → `ValueError`, in entrambi i
casi la coda e la sua dimensione restano inalterate.

## Coda FIFO e contratto comune

Il contratto della coda elenca `accoda`, `estrai`, `fronte`, `vuota` e `len`:
l'accodamento colloca dopo tutti i pendenti, l'estrazione e il fronte agiscono
sulla richiesta in attesa da più tempo, sul vuoto le ultime due sollevano
`IndexError` e conservano lo stato. Gli elementi escono nell'ordine di arrivo e
la dimensione coincide con il numero di richieste pendenti.

## Scelta della rappresentazione

Le due rappresentazioni confrontate sono `CodaDequeU16`, costruita su
`collections.deque` con `append` e `popleft`, e `CodaConcatenataU16`, costruita
sulla catena di nodi con accodamento in coda e rimozione in testa. Il
confronto segue le operazioni richieste dal servizio.

| Operazione del servizio | `CodaDequeU16` | `CodaConcatenataU16` |
|---|---|---|
| Accodamento della richiesta | `O(1)` con `append` | `O(1)` con il riferimento alla coda |
| Lettura del fronte | `O(1)` con `[0]` | `O(1)` con la testa |
| Estrazione | `O(1)` con `popleft` | `O(1)` con l'avanzamento della testa |
| Dimensione | `O(1)` | `O(1)` con il contatore |
| Riferimenti aggiuntivi | gestiti dal modulo `collections` | un riferimento per nodo più gli estremi |

La raccolta principale dei preventivi resta un **registro per posizione**: le
operazioni richieste dal progetto — inserimento nell'ordine dei codici,
consultazione per criterio, proiezione per lista — non richiedono la catena di
nodi, e trasformare il registro in una lista concatenata sarebbe un uso non
pertinente della struttura. La coda delle richieste è il punto in cui la
struttura lineare si giustifica: le richieste pendenti si accodano, si
osservano al fronte ed estraggono nell'ordine di arrivo.

## Servizio e politica di errore

`ServizioConsultazione(coda)` riceve la rappresentazione come collaboratore e
prende i dati del registro **nel momento dell'elaborazione**: la stessa
richiesta può essere elaborata su registri diversi senza essere modificata.
L'esito `EsitoConsultazione` associa alla richiesta il codice, la descrizione
del criterio applicato e la tupla dei codici ammessi, nell'ordine del registro.

La sequenza di elaborazione è **fronte, calcolo, estrazione**: se il calcolo
solleva un'eccezione, la richiesta resta al fronte e può essere riprovata;
l'estrazione avviene soltanto a calcolo riuscito. Con coda vuota
`elabora_prossima` restituisce `None` e conserva lo stato. Il contratto
appartiene al servizio e si distingue dall'estrazione primitiva della coda,
che non conosce il criterio né il registro.

## Estensioni dichiarate

La persistenza della coda richiede uno schema separato e prove proprie: le
richieste pendenti di questa tappa sono stato in memoria. L'eventuale
priorità fra richieste, la ripetizione di un'esecuzione non riuscita e la
cronologia delle elaborazioni sono estensioni con contratto aggiuntivo.
