# Contratti e carico del confronto - tappa U19

## Dossier di scelta degli indici del registro

La tappa confronta le consultazioni del registro su una stessa fotografia
dei preventivi: query esatte per codice, viste ordinate e intervalli con
limiti testuali. Il confronto integra l'adattatore B-tree di riferimento,
costruito dopo il caricamento della stessa proiezione pubblica del
registro. La consultazione e il rapporto sono il lavoro dello studente
(M68); il costruttore dell'albero è fornito. Il modello del registro e
l'interfaccia precedente mantengono i propri contratti.

## Fotografia del registro e ciclo di vita

Ogni indice è costruito sulla tupla restituita dalla proiezione pubblica
`preventivi()` del modello U14, letta **dopo il caricamento**
dell'archivio. Una modifica del registro richiede una **nuova costruzione**
degli indici; le vecchie fotografie conservano i valori immutabili
precedenti. La prova PU19-08 verifica i due indici costruiti prima e dopo
l'inserimento di `021`. Questa scelta evita di imporre una manutenzione
dinamica completa del B-tree: le cancellazioni dinamiche nel dossier sono
simulazioni o ricostruzioni con il proprio costo.

## Chiavi stringa: dominio, ordine e validazione

| Aspetto | Regola dichiarata |
|---|---|
| Dominio della chiave | Stringa non vuota, come il campo `codice` dello schema del registro |
| Validazione | Riusata dal modello: `valida_chiave` richiama `valida_dominio_record` sul campo `codice` |
| Errori di chiave | Tipo diverso da `str` → `TypeError`; stringa vuota → `ValueError`; entrambi prima di ogni effetto |
| Ordine delle chiavi | Lessicografico; `"007"` e `"7"` sono chiavi diverse |
| Dati associati | Valori `Preventivo` immutabili; la chiave coincide con il campo `codice` |

## Contratto del confronto

| Operazione | Risultato | Effetto | Errore |
|---|---|---|---|
| Query esatta per codice | Record `Preventivo` completo | Nessuno | Assente → `KeyError` |
| Vista ordinata | Coppie in ordine lessicografico | Nessuno | — |
| Intervallo chiuso | Coppie fra gli estremi inclusi | Nessuno | Invertito → `ValueError` |
| Ricostruzione dopo modifica | Nuovi indici sulla nuova fotografia | Nuovi oggetti | Duplicato in sorgente → `ValueError` |

## Strutture e ruoli

| Struttura | Ruolo nel rapporto | Preparazione | Query |
|---|---|---|---|
| Scansione di lista | Riferimento lineare | Copia della fotografia | Filtro sequenziale |
| Lista ordinata con `bisect` | Riferimento ordinato | Ordinamento `O(n log n)` | Dicotomica e tratto |
| Indice BST U17 | Query ordinate in memoria interna | Inserimenti senza ribilanciamento | Potatura d'intervallo |
| Indice hash U18 | Query esatte con costo atteso | Tabella con crescita per raddoppio | Catena selezionata |
| Indice B-tree U19 | Query esatte, ordinate e intervalli | Inserimenti con divisioni dal basso | Percorso con conteggi |

## Carico dichiarato del rapporto

Il rapporto `confronta` usa i codici dell'archivio canonico con le query
esatte `007`, `012`, `999` e l'intervallo `003..012`. La preparazione di
ciascun indice è registrata separatamente dalle interrogazioni; gli esiti
sono verificati contro `dict` e `sorted` con filtro prima di ogni misura.
I conteggi del B-tree distinguono nodi visitati e confronti fra chiavi; i
trasferimenti di blocchi appartengono al modello dichiarato del dossier.

## Colonne e perimetro del rapporto

Il CSV contiene `fase,struttura,query,esito,atteso,coerente,tempo_s,confronti,
nodi,blocchi,modello,cache`: cinque righe di preparazione e venti di query.
La durata `tempo_s` misura il costruttore di ciascun indice, incluse copie e
validazioni; la proiezione dei dati e la scrittura del CSV restano esterne.
Con indici già costruiti e senza misure fornite, la durata resta vuota e il
modello dichiara che la preparazione non è stata cronometrata.

La scansione conta uguaglianze; la dicotomica strumentata conta confronti
`<` e `==`; l'hash conta uguaglianze nella catena, escludendo il calcolo
dell'hash; il BST conta nodi con la propria API pubblica, senza inventare
confronti; il B-tree conta nodi e confronti. Per gli alberi il modello usa
un nodo per blocco e cache reinizializzata a ogni query: inizialmente vuota
oppure con la sola radice residente. Gli intervalli conservano gli esiti
verificati ma dichiarano i propri costi non strumentati. Ogni campo metrico
vuoto significa non misurato; uno zero indica un conteggio realmente nullo.
