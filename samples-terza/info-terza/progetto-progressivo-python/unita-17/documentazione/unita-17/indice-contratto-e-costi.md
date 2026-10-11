# Contratto e costi dell'indice — tappa U17

## Fotografia del registro e ciclo di vita

L'indice di consultazione è costruito su una **fotografia** dei preventivi del
registro: la tupla restituita dalla proiezione pubblica `preventivi()` del
modello U14, letta **dopo il caricamento** dell'archivio. L'indice così
costruito risponde a più interrogazioni senza essere ricostruito e conserva
l'associazione fra ogni codice e il record del momento della costruzione.

Il ciclo di vita è esplicito. Una modifica del registro — inserimento,
aggiornamento o eliminazione — richiede una **nuova costruzione** dell'indice;
la vecchia fotografia continua a rappresentare i dati precedenti, perché i
valori `Preventivo` sono immutabili e l'indice non condivide con il registro
né contenitori mutabili né aggiornamenti. La prova PU17-07 verifica i due
indici costruiti prima e dopo l'aggiornamento di `007` da 450 a 500 centesimi:
il primo restituisce ancora 450, il secondo 500, e il codice `"007"` resta
identico in entrambi. Questa scelta rende verificabili coerenza e costo senza
introdurre una sincronizzazione automatica fra due raccolte.

## Chiavi stringa: dominio, ordine e validazione

Il BST didattico del capitolo PY-33 usa chiavi intere; l'indice adotta la
**variante dichiarata a chiavi stringa**, perché i codici del registro sono
stringhe con zeri significativi e non ammettono conversioni.

| Aspetto | Regola dichiarata |
|---|---|
| Dominio della chiave | Stringa non vuota, come il campo `codice` dello schema del registro |
| Validazione | Riusata dal modello: `valida_chiave` richiama `valida_dominio_record` sul campo `codice` |
| Errori di chiave | Tipo diverso da `str` → `TypeError`; stringa vuota → `ValueError`; entrambi prima di ogni effetto |
| Ordine | Lessicografico di Python fra stringhe: `"003"` < `"007"` < `"012"` |
| Codici di lunghezza diversa | `"007"` e `"7"` sono chiavi diverse e `"007"` precede `"7"`; `"10"` precede `"9"` |
| Costo dei confronti | Proporzionale ai testi confrontati; il conteggio dei nodi esaminati non include questo costo |

L'equivalenza fra ordine lessicografico e ordine numerico richiede che tutti
i codici abbiano la stessa lunghezza: con lunghezze diverse la regola resta
quella lessicografica, come verificato dal caso proprio 1 della suite.

## Contratto dell'indice

Le operazioni di `IndiceBSTU17` dichiarano dati ammessi, risultato, effetti
ed errori; la struttura ad albero del capitolo PY-33 è riprodotta nel modulo
`indice_bst_u17.py`, perché la fotografia della raccolta resta autonoma.

| Operazione | Contratto |
|---|---|
| `costruisci_indice(sorgente)` | Indice costruito sulla sequenza di `Preventivo`; duplicati e record non ammessi rifiutati **prima** di consegnare qualsiasi struttura |
| `len(indice)` | Numero dei codici presenti |
| `contiene(codice)` | `True` oppure `False`; indice vuoto → `False`; chiave fuori dominio → errore anche sul vuoto |
| `cerca(codice)` | Record associato; codice assente → `KeyError` |
| `inserisci(codice, record)` | Nuova associazione fra codice e record; duplicato → `ValueError` senza effetti; chiave e `record.codice` devono coincidere |
| `aggiorna(codice, record)` | Sostituisce il record del codice; assente → `KeyError`; forma e dimensione invariate |
| `rimuovi(codice)` | `True` se il codice viene eliminato, `False` se è assente; gli altri record restano associati ai propri codici |
| `minimo()`, `massimo()` | Codice estremo in ordine lessicografico; indice vuoto → `IndexError` |
| `inordine()` | Lista nuova dei codici in ordine lessicografico crescente: la vista ordinata dell'indice |
| `voci_ordinate()` | Lista nuova di coppie `(codice, record)` in ordine crescente |
| `intervallo(minimo, massimo)` | Lista nuova di coppie nell'intervallo chiuso, estremi inclusi; nessun risultato → `[]`; `minimo > massimo` → `ValueError` |
| `altezza()` | Altezza in archi, con il sottoalbero vuoto pari a -1 |
| `controlla_invarianti()` | Strumento diagnostico su struttura, ordine, dimensione e associazioni; violazione → `AssertionError` |

La raccolta principale dei preventivi resta un **registro per posizione**:
l'ordine di inserimento, le proiezioni per lista e la persistenza non
richiedono l'albero, e costruire l'indice dentro il registro legherebbe due
responsabilità distinte. L'indice è una vista separata, consultabile senza
modificare la raccolta.

## Costi delle operazioni

L'altezza `h` è contata in archi e ogni percorso massimo contiene `h + 1`
nodi; sul vuoto le operazioni elementari costano `O(1)`. Un nodo risulta
esaminato quando la sua chiave viene letta per decidere un'operazione: la
visita di un collegamento vuoto appartiene alla traccia di controllo e non
viene contata, e la radice inserita per prima esamina 0 nodi.

| Operazione | Costo in funzione di `h` e `n` | Valori osservati dalla suite |
|---|---|---|
| Costruzione da `n` record | `O(n · (h + 1))`, un inserimento per record | 21 nodi per 7 codici crescenti, 10 per 7 codici mescolati |
| Ricerca esatta | `O(h + 1)` | 7 nodi su catena crescente, 3 su forma bilanciata |
| Ricerca di un codice assente | `O(h + 1)` | 7 nodi contro 3, fino al collegamento vuoto |
| Intervallo chiuso con `k` risultati | `O(h + k)` | il taglio dei sottoalberi fuori intervallo evita la scansione completa |
| `inordine()` e `voci_ordinate()` | `O(n)` | una visita inordine, lista nuova |
| `minimo()` e `massimo()` | `O(h + 1)` | discesa lungo un solo bordo |
| `inserisci`, `aggiorna`, `rimuovi` | `O(h + 1)` | la cancellazione con due figli aggiunge la ricerca del successore |
| `altezza()` e `controlla_invarianti()` | `O(n)` | strumenti diagnostici, fuori dalle misure delle operazioni |

I due costi restano **separati**: la costruzione si misura con
`misura_costruzione`, che restituisce l'indice e i nodi esaminati dagli
inserimenti, e ogni interrogazione con `misura_ricerca`, che restituisce i
nodi esaminati e il record trovato oppure `None`. La suite PU17-09 confronta
le stesse sette chiavi in due ordini di inserimento: la sequenza crescente
produce altezza 6 e 21 nodi esaminati nella costruzione, quella mescolata
altezza 2 e 10 nodi, e le ricerche di `"007"` costano 7 nodi contro 3. La
degenerazione dipende dall'ordine di inserimento; il bilanciamento mantenuto
da una struttura apposita offre una garanzia diversa da quella probabilistica
dell'ordine casuale.

## Perché un BST per questa consultazione

Il requisito della tappa è rispondere a **più interrogazioni** — ricerche
esatte e intervalli chiusi — su una fotografia già caricata, con i codici in
ordine. Le alternative confrontate sono:

| Organizzazione | Ricerca esatta | Intervallo chiuso | Aggiornamento |
|---|---|---|---|
| Scansione lineare della raccolta | `O(n)` per interrogazione | `O(n)` con ordinamento dei risultati | nessun costo aggiuntivo |
| Lista ordinata più ricerca dicotomica | `O(log n)` | `O(log n + k)` | `O(n)` per ogni inserimento in posizione |
| BST costruito dopo il caricamento | `O(h + 1)` | `O(h + k)` | `O(h + 1)` per inserimento e cancellazione |

Il BST mantiene l'ordine come proprietà della struttura e rende gli estremi
dell'intervallo raggiungibili con due discese; la scansione lineare ripete il
costo su ogni interrogazione e la lista ordinata trasforma ogni modifica in
uno spostamento di posizioni. La scelta si giustifica finché `h` resta
contenuto: con sette codici il confronto è didattico, con raccolte ampie la
degenerazione rende preferibili strutture bilanciate.

## Estensioni dichiarate

L'indice aggiornato a ogni operazione CRUD del registro è un'estensione con
operazioni coordinate e prove proprie: richiede di propagare ogni modifica
alla struttura e di verificare la coerenza in ogni momento. In modo analogo
restano estensioni il bilanciamento dell'albero, la persistenza dell'indice
su file e le statistiche sui confronti primitivi fra caratteri.
