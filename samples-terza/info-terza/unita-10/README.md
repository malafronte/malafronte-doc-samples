# Unità 10 - sorgenti Python d'esempio (cap. PY-14)

Sorgenti d'esempio dell'Unità 10 del corso di informatica della terza: ricerche
e ordinamenti elementari. I file accompagnano il capitolo PY-14 e le sue quattro
parti: ricercare una chiave, costruire quattro ordinamenti elementari, record e
criteri di ordinamento, analisi e prima sperimentazione. Come per le altre
unità, questi sorgenti non si distribuiscono come download dal sito: le pagine
li mostrano con `RemoteCode` e citano il percorso di questo repository.

## Mappa dei file

- `esempi/ricerche_u10.py` - contratto canonico della ricerca per il **primo
  indice** con `cerca_lineare`, `cerca_dicotomica` iterativa e
  `cerca_dicotomica_ricorsiva` su estremi, più le varianti di contratto
  `contiene`, `cerca_un_indice`, `cerca_tutti_gli_indici` e
  `posizione_di_inserimento`.
- `esempi/ordinamenti_u10.py` - i quattro ordinamenti elementari col contratto
  comune: `insertion_sort`, `selection_sort`, `bubble_sort` e
  `bubble_sort_ottimizzato`, più l'approfondimento `bubble_sort_ultimo_scambio`.
- `esempi/record_u10.py` - ordinamento di record con funzione chiave
  (`insertion_sort_chiave`, `selection_sort_chiave`, `bubble_sort_chiave`),
  criterio composto `(totale_cent, codice)`, viste ordinate del registro
  sintetico e forme idiomatiche `sorted` / `list.sort`.
- `esempi/conteggi_u10.py` - varianti nominate e strumentate che contano
  confronti, scambi, spostamenti e sondaggi, con le formule attese per `n`
  piccoli.
- `esempi/misure_u10.py` - costruzione deterministica delle cinque famiglie di
  input e protocollo di misura con `time.perf_counter`, copie fuori dal timer,
  ripetizioni, sintesi a mediana e metadati.
- `esempi/test_esempi_u10.py` - suite deterministica di verifica degli attesi
  del capitolo e delle proprietà dei sorgenti d'esempio.
- `starter-laboratorio/ordinamenti_u10.py` - firme, docstring e contratti dei
  quattro ordinamenti del LAB-PY-U10, con i corpi da completare in fase L2.
- `starter-laboratorio/conteggi_u10.py` - strumentazione da completare in fase
  L4, con `formule_attese` già fornita.
- `starter-laboratorio/dataset_u10.py` - cinque famiglie di input e copie
  indipendenti: **fornito completo**, si usa in fase L5.
- `starter-laboratorio/misure_u10.py` - cornice del timer con regione
  cronometrata da completare in fase L6; sintesi, metadati e riga di tabella
  già forniti.
- `starter-laboratorio/test_ordinamenti_u10.py` - casi pubblici L01-L12 con i
  fallimenti attesi documentati e il caso L12 lasciato da progettare.
- `riferimento-laboratorio/` - le cinque controparti complete e verificate
  dello starter, con il caso L12 compilato.

## Esempi, starter e riferimento del laboratorio

La cartella contiene tre gruppi di file che descrivono tre momenti diversi:

- `esempi/` - i sorgenti completi che accompagnano il capitolo PY-14;
- `starter-laboratorio/` - la baseline **incompleta** del LAB-PY-U10, che
  dichiara di esserlo: i corpi da completare mancano e i test corrispondenti
  falliscono in modo visibile;
- `riferimento-laboratorio/` - la controparte completa dello starter,
  consultabile dopo le fasi L2-L3 come confronto formativo.

Le cartelle del laboratorio contengono **moduli omonimi** - `ordinamenti_u10.py`,
`conteggi_u10.py`, `dataset_u10.py`, `misure_u10.py` e `test_ordinamenti_u10.py` -
e anche `esempi/` usa i nomi `misure_u10.py`. Le tre suite vanno quindi
eseguite **una alla volta**, ciascuna con il proprio percorso: eseguirle insieme
in un'unica chiamata a `pytest` produce una collisione di import, perché il
primo modulo caricato con quel nome copre gli altri. La stessa regola vale nella
raccolta dello studente, dove un solo gruppo di file per volta viene copiato in
`programmi/`.

## Comandi di esecuzione

I comandi sono indicati per la cartella `unita-10/` di questo repository. Con
`uv` non servono installazioni globali: le dipendenze richieste compaiono nel
comando. Nessun sorgente dell'Unità 10 richiede dipendenze esterne: `random` e
`time` appartengono alla libreria standard e il confronto sperimentale si legge
da tabelle testuali.

```powershell
# dimostrazioni dei moduli d'esempio (nessuna dipendenza esterna)
uv run python esempi/ricerche_u10.py
uv run python esempi/ordinamenti_u10.py
uv run python esempi/record_u10.py
uv run python esempi/conteggi_u10.py

# dataset e protocollo di misura: tabelle in stdout, nessun file scritto
uv run python esempi/misure_u10.py

# suite di verifica, UNA ALLA VOLTA per la collisione dei nomi dei moduli
uv run --with pytest python -m pytest esempi/test_esempi_u10.py -q
uv run --with pytest python -m pytest riferimento-laboratorio/test_ordinamenti_u10.py -q
uv run --with pytest python -m pytest starter-laboratorio/test_ordinamenti_u10.py -q
```

L'ultima suite è quella dello starter: alla prima esecuzione riporta
**fallimenti attesi** per i corpi ancora da completare e non deve produrre errori
di import né di raccolta. Gli altri due gruppi sono verdi per intero:
`esempi/` ha 188 test deterministici, `riferimento-laboratorio/` ne ha 114. Con
lo starter i soli casi che passano sono quelli sui file forniti completi -
famiglie di input, copie, sintesi, metadati e riga di tabella - per un totale di
6 test.

Per eseguire con l'interprete della stessa serie usata dal corso aggiungere
`--python 3.14` ai comandi precedenti.

## Versioni verificate

- CPython 3.12.13 (e versioni compatibili maggiori);
- pytest, invocato con `uv run --with pytest`;
- Windows 11, esecuzione normale fuori dal debugger.

I sorgenti non usano costrutti successivi a quelli già impiegati nelle unità
precedenti: funzioni, liste, dizionari, tuple, `random.Random`, `time.perf_counter`
e `functools` non richiesto. Le durate stampate appartengono all'ambiente di chi
esegue e non sono riproducibili come valori assoluti.

## Contratti e vocabolario dei conteggi

Il contratto canonico delle ricerche restituisce il **primo indice** della chiave
cercata oppure `None`, senza modificare l'argomento. La ricerca dicotomica
prosegue nella metà sinistra anche dopo una corrispondenza: è questa la ragione
per cui il caso `[1, 3, 3, 3, 8]` con bersaglio `3` dà `1` e non `2`. La variante
«un indice qualsiasi» (`cerca_un_indice`) può terminare al primo medio ed è un
contratto diverso, non una scorciatoia dello stesso.

Il contratto degli ordinamenti didattici modifica **sul posto** una `list` e
restituisce `None`. Le forme standard `sorted` e `list.sort` sono introdotte
dopo il procedimento esplicito e hanno effetti diversi: la prima produce una
lista nuova, la seconda modifica e restituisce `None`.

Eventi contati, con lo stesso vocabolario del capitolo, del laboratorio e delle
schede:

- **confronto fra chiavi**: valutazione effettiva di un operatore di confronto
  fra due chiavi. Se l'operatore non viene valutato - perché un cortocircuito lo
  salta - il confronto non si conta.
- **scambio**: interversione di due posizioni della lista.
- **spostamento**: assegnamento che trasla di una posizione un elemento durante
  l'inserimento.
- **sondaggio**: accesso al medio della ricerca dicotomica. Un sondaggio non è
  un confronto: può produrne uno, se l'uguaglianza è vera, oppure due.

Le versioni strumentate sono **varianti nominate** e non sostituiscono le
funzioni del contratto: il registro dei conteggi è un output aggiuntivo e la
prova di equivalenza è nei test. Le versioni con contatori non vanno
cronometrate per attribuirne il tempo alle versioni ordinarie.

## Formule attese verificate

Le formule valgono per le **versioni qui pubblicate**, non per qualunque
programma portato con lo stesso nome. I test le verificano su `n = 0, 1, 2, 4`
e su casi indipendenti.

| Procedimento | Confronti fra chiavi | Dove |
|---|---|---|
| `selection_sort` | `n(n-1)/2` | ogni disposizione, fino a `n-1` scambi |
| `bubble_sort` | `n(n-1)/2` | ogni disposizione, compreso il già ordinato |
| `bubble_sort_ottimizzato` | `n(n-1)/2` peggiore, `n-1` per `n >= 1` sul già ordinato | arresto a passata senza scambi |
| `insertion_sort` | `n-1` per `n >= 1` sul già ordinato, `n(n-1)/2` sull'inverso | spostamenti, mai scambi |
| `cerca_lineare` | fino a `n` confronti `==` | un elemento esaminato per sondaggio |
| `cerca_dicotomica` | da 1 a 2 operatori per sondaggio | `n = 0` lavoro costante, altrimenti Θ(log n) sondaggi per `n` crescente |

Per `n = 0` tutti i procedimenti qui elencati fanno un numero costante di
operazioni: nessuna formula con `n - 1` si applica al vuoto senza la dichiarazione
`n >= 1`.

## Derivazione e corrispondenza con le altre unità

`esempi/record_u10.py` riprende il registro sintetico dei preventivi già usato
nel capitolo PY-12 con campi `codice`, `destinazione` e `totale_cent`: i codici
restano stringhe con zeri iniziali significativi e gli importi restano interi in
centesimi. Nessuna funzione di questa cartella realizza le funzioni della tappa
autonoma del progetto progressivo - `vista_per_codice`, `cerca_per_codice`,
`vista_per_totale` - né il documento `confronto_consultazioni.md`: quella tappa è
un lavoro autonomo dello studente e il corso non ne pubblica una soluzione
integrale.

`esempi/misure_u10.py` applica il protocollo del capitolo PY-13, parte IV, e
della guida alle misure: test di correttezza prima del timer, dataset generati
fuori dalla regione cronometrata, copie separate degli stessi originali,
ripetizioni con campioni grezzi conservati e sintesi a mediana con minimo e
massimo. Le cinque famiglie di input sono quelle che l'Unità 11 estenderà al
confronto con MergeSort e QuickSort: la matrice qui presente non è un confronto
definitivo di tutti gli ordinamenti.
