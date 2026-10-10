# Contratti e scelte dei componenti — U15

Requisiti della variazione, promesse dei componenti e confronto fra
organizzazioni possibili per
[`registro_consultazione_u15.py`](../../programmi/registro_consultazione_u15.py).
Documento di lavoro della milestone M55, affiancato da
[`prove-e-regressione.md`](prove-e-regressione.md) e dal
[`diagramma.puml`](diagramma.puml) aggiornato nella revisione.

## Variazione scelta

**Famiglia: politiche di consultazione.** Il registro deve poter rispondere a
domande diverse — quali preventivi sono locali, quali raggiungono una soglia
di importo — senza moltiplicare il codice del client. Il cambiamento
osservabile richiesto dalla consegna è esplicito:

| Aspetto | Contenuto |
|---|---|
| collaboratore sostituibile | il criterio di consultazione, ricevuto dal client |
| chiamata che resta uguale | `seleziona_codici(registro, criterio)` e il ciclo su `ammette` |
| promesse che permettono il riuso | risultato esattamente `bool`, nessun effetto, configurazione immutabile, decisione deterministica |

Il dataset di consultazione resta quello pubblicato — `007/locale/450`,
`012/nazionale/0`, `003/locale/1200` — e l'archivio canonico del registro non
cambia: la consultazione legge, non scrive.

## Contratto comune del criterio

`ammette(preventivo) -> bool`, con:

- **dati ammessi**: un valore `Preventivo` già validato dal modello U14;
- **risultato**: esattamente un `bool`, non un valore «veritiero»;
- **effetti**: nessuno su preventivo e raccolta; determinismo per la stessa
  configurazione;
- **errori**: `ErroreConfigurazione` alla costruzione per configurazioni non
  ammesse — prima di ogni uso e di ogni effetto;
- **invarianti**: la configurazione è stabile dopo la costruzione.

Il client `seleziona_codici` promette lista nuova di codici nell'ordine della
raccolta, identità di dominio conservata (`"007"` resta `"007"`), registro
invariato, vuoto senza chiamate al criterio, `TypeError` su un risultato che
non è esattamente `bool` senza risultati parziali.

## Confronto fra due organizzazioni possibili

**Organizzazione A — famiglia per ereditarietà.** Una classe base `Criterio`
dichiara `ammette` astratto; le politiche la derivano e il client riceve
sempre un `Criterio`. Vantaggi: la famiglia è nominale e visibile; la
completezza si controlla alla costruzione delle classi derivate. Limiti:
ogni nuovo criterio deve dichiarare la derivazione — anche un oggetto già
esistente, o una semplice funzione, diventa inutilizzabile senza un
adattatore — e la specializzazione qui non aggiunge stato né codice comune
da riusare.

**Organizzazione B — componenti autonomi con duck typing e composizione
(scelta adottata).** Le politiche sono classi indipendenti che offrono
`ammette`; il client riceve il collaboratore dal punto di avvio e lo usa
attraverso le operazioni del contratto. Vantaggi: qualunque classe compatibile
è integrabile senza dichiarazioni — la variante breve `PoliticaSogliaEsclusiva`
lo dimostra — la configurazione vive nel costruttore del componente e la
scelta concreta è esplicita in `consultazione_cli_u15.py`. Limiti: la
compatibilità di firma e significato non è dichiarata al linguaggio; la
verifica è affidata al contratto scritto e alle prove condivise.

La **dichiarazione con `ABC` o `Protocol`** è la variante statica
dell'organizzazione A: `ABC` aggiungerebbe il controllo di completezza alla
costruzione, `Protocol` renderebbe esplicita la struttura al verificatore dei
tipi senza derivazione. Sono strumenti già studiati nei capitoli OOP-05 e
OOP-06; questa realizzazione li omette perché la famiglia è piccola, il
contratto è documentato e le prove condivise verificano il comportamento — la
scelta è motivata dai requisiti, non da un divieto di usare quegli strumenti.

## Sintesi delle scelte

- **Composizione**: il client riceve il criterio; non lo costruisce né lo
  cerca — la scelta concreta è nel punto di avvio (PU15-08).
- **Duck typing documentato**: il contratto di `ammette` è scritto sopra e
  verificato dalla suite condivisa; la guardia sul `bool` esatto rende
  osservabile il difetto più plausibile.
- **Configurazione validata alla costruzione**: un criterio non ammesso non
  esiste (PU15-06), quindi nessun effetto sul registro può precedere
  l'errore.
