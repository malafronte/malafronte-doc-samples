# Unità 11 - sorgenti Python d'esempio (cap. PY-15)

Sorgenti d'esempio dell'Unità 11 del corso di informatica della terza: divide et
impera, MergeSort, QuickSort e confronto delle prestazioni. I file accompagnano
il capitolo PY-15 e le sue quattro parti: fusione e divide et impera, MergeSort,
partizione e QuickSort, confronto degli algoritmi. Come per le altre unità,
questi sorgenti non si distribuiscono come download dal sito: le pagine li
mostrano con `RemoteCode` e citano il percorso di questo repository.

## Mappa dei file

- `esempi/merge_quick_u11.py` - le quattro funzioni canoniche del capitolo:
  `fondi_ordinate`, `merge_sort`, `partiziona_lomuto` e `quick_sort`, con il
  parametro opzionale `chiave` e i contratti distinti fra lista nuova e
  ordinamento sul posto.
- `esempi/conteggi_u11.py` - varianti nominate e strumentate che contano
  confronti, scambi, copie e profondità massima, più le formule
  `confronti_massimi_fusione` e `copie_attese_merge_sort`.
- `esempi/misure_u11.py` - le cinque famiglie di input con le regole di U10,
  ricerche del cap. PY-14, protocollo di misura con `time.perf_counter`,
  contratto unico per procedure in-place e procedure che restituiscono una lista
  nuova, campioni, sintesi a mediana e metadati.
- `esempi/test_esempi_u11.py` - suite deterministica di verifica degli attesi del
  capitolo e delle proprietà dei sorgenti d'esempio.
- `starter-laboratorio/ordinamenti_u11.py` - firme, docstring e contratti delle
  quattro funzioni del LAB-PY-U11, con i corpi da completare in fase L2.
- `starter-laboratorio/conteggi_u11.py` - strumentazione da completare in fase
  L3, con `confronti_massimi_fusione` e `copie_attese_merge_sort` già fornite.
- `starter-laboratorio/dataset_u11.py` - cinque famiglie di input e copie
  indipendenti: **fornito completo**, si usa nelle fasi L4 e L5.
- `starter-laboratorio/ordinamenti_elementari_u11.py` - i quattro ordinamenti
  elementari del cap. PY-14: **modulo di servizio fornito completo** per il
  confronto U10-U11 della fase L8.
- `starter-laboratorio/ricerche_u11.py` - ricerca lineare e dicotomica del cap.
  PY-14: **modulo di servizio fornito completo** per la fase L7.
- `starter-laboratorio/misure_u11.py` - cornice del timer con regione cronometrata
  da completare in fase L5 e misura della sequenza di ricerche da completare in
  fase L7; sintesi, metadati e riga di tabella già forniti.
- `starter-laboratorio/test_ordinamenti_u11.py` - casi pubblici L01-L12 con i
  fallimenti attesi documentati e il caso L12 lasciato da progettare.
- `riferimento-laboratorio/` - le controparti complete e verificate dello
  starter, con il caso L12 compilato e un proprio README.

## Esempi, starter e riferimento del laboratorio

La cartella contiene tre gruppi di file che descrivono tre momenti diversi:

- `esempi/` - i sorgenti completi che accompagnano il capitolo PY-15;
- `starter-laboratorio/` - la baseline **incompleta** del LAB-PY-U11, che
  dichiara di esserlo: i corpi da completare mancano e i test corrispondenti
  falliscono in modo visibile;
- `riferimento-laboratorio/` - la controparte completa dello starter,
  consultabile dopo le fasi L2-L3 come confronto formativo.

Le cartelle del laboratorio contengono **moduli omonimi** - `ordinamenti_u11.py`,
`conteggi_u11.py`, `dataset_u11.py`, `misure_u11.py`, `test_ordinamenti_u11.py` - e
anche `esempi/` usa i nomi `misure_u11.py`. Le tre suite vanno quindi eseguite
**una alla volta**, ciascuna con il proprio percorso: eseguirle insieme in
un'unica chiamata a `pytest` produce una collisione di import, perché il primo
modulo caricato con quel nome copre gli altri. I due moduli di servizio
`ordinamenti_elementari_u11.py` e `ricerche_u11.py` hanno nomi propri proprio per
non collidere con i file omonimi del LAB-PY-U10 quando entrambi finiscono nella
stessa cartella `programmi/` della raccolta dello studente.

## Comandi di esecuzione

I comandi sono indicati per la cartella `unita-11/` di questo repository. Con
`uv` non servono installazioni globali: le dipendenze richieste compaiono nel
comando. Nessun sorgente dell'Unità 11 richiede dipendenze esterne: `random`,
`time` e `sys` appartengono alla libreria standard e il confronto sperimentale si
legge da tabelle testuali. `matplotlib` non è richiesto: il grafico della fase L8
è guidato, ha una tabella equivalente e si produce solo in un progetto locale che
lo installa in modo esplicito.

```powershell
# dimostrazioni dei moduli d'esempio (nessuna dipendenza esterna)
uv run python esempi/merge_quick_u11.py
uv run python esempi/conteggi_u11.py

# dataset e protocollo di misura: tabelle in stdout, nessun file scritto
uv run python esempi/misure_u11.py

# suite di verifica, UNA ALLA VOLTA per la collisione dei nomi dei moduli
uv run --with pytest python -m pytest esempi/test_esempi_u11.py -q
uv run --with pytest python -m pytest riferimento-laboratorio/test_ordinamenti_u11.py -q
uv run --with pytest python -m pytest starter-laboratorio/test_ordinamenti_u11.py -q
```

L'ultima suite è quella dello starter: alla prima esecuzione riporta
**fallimenti attesi** per i corpi ancora da completare e non deve produrre errori
di import né di raccolta. Gli altri due gruppi sono verdi per intero:
`esempi/` ha 137 test deterministici, `riferimento-laboratorio/` ne ha 66. Con lo
starter i soli casi che passano sono quelli sui file forniti completi - famiglie
di input, copie, sintesi, metadati e riga di tabella - per un totale di 6 test,
mentre i restanti 60 falliscono sui `NotImplementedError` delle fasi L2, L3, L5,
L7 e sul caso L12 da progettare.

Per eseguire con l'interprete della stessa serie usata dal corso aggiungere
`--python 3.14` ai comandi precedenti.

## Versioni verificate

- CPython 3.12.13 (e versioni compatibili maggiori);
- pytest, invocato con `uv run --with pytest`;
- Windows 11, esecuzione normale fuori dal debugger.

I sorgenti non usano costrutti successivi a quelli già impiegati nelle unità
precedenti: funzioni, liste, dizionari, tuple, slicing, `random.Random`,
`time.perf_counter` e ricorsione. Le durate stampate appartengono all'ambiente di
chi esegue e non sono riproducibili come valori assoluti.

## Contratti e vocabolario dei conteggi

Le quattro funzioni canoniche hanno contratti **distinti**, che il confronto deve
conservare:

| Funzione | Ingresso, risultato ed effetti | Proprietà della variante canonica |
|---|---|---|
| `fondi_ordinate(sinistra, destra, chiave=None)` | due liste già non decrescenti; nuova lista; ingressi invariati | due indici, a parità prende la sinistra (`<=` fra chiavi); tempo Θ(a+b), spazio Θ(a+b) per il risultato |
| `merge_sort(valori, chiave=None)` | nuova lista, anche per 0/1 elementi; `valori` invariato | slicing delle metà e fusione stabile; caso base `len <= 1` con copia; Θ(n log n) tempo, picco Θ(n) più stack Θ(log n), copie complessive Θ(n log n) |
| `partiziona_lomuto(valori, sinistra, destra, chiave=None)` | intervallo inclusivo non vuoto; modifica solo quello; indice finale del pivot | pivot `valori[destra]`, confronto `<=`, uguali a sinistra; Θ(1) spazio |
| `quick_sort(valori, chiave=None)` | ordinamento sul posto; restituisce `None`; 0/1 elementi senza partizione | sottointervalli `[sinistra, p-1]` e `[p+1, destra]`, pivot escluso; stack Θ(log n) bilanciato, Θ(n) nel peggiore; non stabile |

`chiave=None` significa confronto dei valori stessi; per i record la funzione
produce la chiave senza perdere il record. Nelle versioni didattiche una chiave
costosa può essere ricalcolata durante più confronti, mentre `sorted` la valuta
una sola volta per elemento: le due implementazioni non hanno lo stesso costo
costante.

Eventi contati, con lo stesso vocabolario del capitolo, del laboratorio e delle
schede:

- **confronto fra chiavi**: valutazione effettiva di un operatore di confronto
  (`<`, `>`, `<=`, `>=`, `==`) fra due chiavi, compresa quella falsa che
  interrompe un ciclo. Se l'operatore non viene valutato, il confronto non si
  conta.
- **scambio**: interversione di due posizioni **diverse** della lista. Lo scambio
  con le due posizioni coincidenti non si esegue e non si conta.
- **copia**: assegnamento che scrive un elemento di una sequenza in un'altra
  sequenza o in una nuova posizione della stessa. Comprende le metà prodotte dallo
  slicing, le copie del caso base e le scritture nella lista fusa.
- **profondità massima**: numero massimo di frame ricorsivi contemporaneamente
  attivi, con la chiamata che ordina l'intera lista che vale 1; si registra
  all'ingresso di ogni chiamata, comprese quelle su intervalli di 0 o 1 elemento.
- **sondaggio**: accesso al medio della ricerca dicotomica, ereditato dal cap.
  PY-14. Un sondaggio non è un confronto: può produrne uno, se l'uguaglianza è
  vera, oppure due.

Le versioni strumentate sono **varianti nominate** e non sostituiscono le
funzioni del contratto: il registro dei conteggi è un output aggiuntivo e la
prova di equivalenza è nei test. Le versioni con contatori non vanno cronometrate
per attribuirne il tempo alle versioni ordinarie.

## Formule attese verificate

Le formule valgono per le **versioni qui pubblicate**, non per qualunque
programma portato con lo stesso nome. I test le verificano su `n = 0, 1, 2, 4, 8`
e su casi indipendenti.

| Procedimento | Grandezza attesa | Dove |
|---|---|---|
| `fondi_ordinate` | al più `a + b - 1` confronti con entrambi i lati non vuoti, `0` con un lato vuoto; `a + b` copie | il limite si raggiunge con liste interlacciate; ogni confronto colloca almeno un elemento |
| `merge_sort` | `copie_attese_merge_sort(n)` copie, `2n·log2(n) + n` per `n` potenza di due | somma delle metà, dei risultati di fusione e delle copie del caso base |
| `partiziona_lomuto` | `destra - sinistra` confronti, uno per ogni elemento non pivot | gli scambi sono al più `destra - sinistra + 1` e si compiono solo se le posizioni differiscono |
| `quick_sort` | `copie = 0`, profondità `Θ(log n)` se bilanciata e `n` sui casi sfavorevoli con pivot finale | già ordinato, inverso e soli valori uguali riducono l'intervallo di uno per chiamata |
| `cerca_dicotomica` | da 1 a 2 operatori per sondaggio | contratto del primo indice, ereditato dal cap. PY-14 |

Per `n = 0` tutti i procedimenti qui elencati fanno un numero costante di
operazioni: nessuna formula con `n - 1` si applica al vuoto senza la dichiarazione
`n >= 1`.

## Derivazione e corrispondenza con le altre unità

`esempi/misure_u11.py` riproduce le cinque famiglie di `dataset_u10.py` con la
stessa regola di costruzione e lo stesso seme `20260927`: i dati del confronto
U10-U11 sono quindi gli **stessi** e le due campagne di misura si collegano. La
duplicazione del generatore è intenzionale, perché il LAB-PY-U11 resta
riproducibile senza il materiale del LAB-PY-U10; nessuna funzione di questa
cartella realizza le funzioni della tappa U11 del progetto progressivo -
confronto fra strategie, scelta motivata e relazione - che resta un lavoro
autonomo dello studente senza soluzione integrale pubblica.

Il protocollo è quello del cap. PY-13, parte IV, e della guida «Misurare le
prestazioni di Python»: test di correttezza prima del timer, dataset generati
fuori dalla regione cronometrata, copie separate degli stessi originali,
ripetizioni con campioni grezzi conservati e sintesi a mediana con minimo e
massimo. Il confronto con `sorted` è un confronto con un'**implementazione
concreta** di CPython, non con un algoritmo didattico: la riga della tabella lo
dichiara e la relazione ne discute i limiti.
