# Unità 9 — sorgenti Python d'esempio (cap. PY-13)

Sorgenti d'esempio dell'Unità 9 del corso di informatica della terza: analisi
dei costi di un algoritmo. I file accompagnano il capitolo PY-13 e le sue
quattro parti: costruire una funzione di costo, notazioni e ordini di
crescita, memoria e costo ammortizzato, misurare e discutere i risultati.
Come per le altre unità, questi sorgenti non si distribuiscono come download
dal sito: le pagine li mostrano con `RemoteCode` e citano il percorso di
questo repository.

## Mappa dei file

- `esempi/conteggi_scansioni.py` — riepiloghi a una e due scansioni con lo
  stesso contratto, scansione con arresto `contiene_zero`, variante con
  soglia del problema svolto I e versioni strumentate che contano visite,
  addizioni e confronti.
- `esempi/conteggi_cicli.py` — conteggi esatti dei cicli: attraversamenti
  consecutivi e indipendenti, coppie `i < j`, interno a tre giri fissi,
  dimezzamenti, raddoppiamenti, n ripetizioni del dimezzamento e visita di
  una matrice rettangolare, con la tabella dei conteggi costruita in memoria.
- `esempi/confronto_fibonacci.py` — le tre varianti canoniche di Fibonacci
  (diretta, iterativa, con memoria esplicita) con i conteggi C, D e S e le
  addizioni dell'iterativa; più fattoriale e Hanoi con i conteggi di
  moltiplicazioni, ingressi, frame e mosse in output.
- `esempi/capacita_dinamica.py` — simulazione del modello didattico della
  capacità dinamica: capacità iniziale 1, raddoppio quando pieno, copie e
  scritture contate, tabella degli otto accodamenti e limiti della somma
  geometrica su m accodamenti.
- `esempi/misure_u9.py` — i tre esperimenti di misura di riferimento
  (scansioni equivalenti e arresto anticipato, tre varianti di Fibonacci,
  conteggi dei cicli) con timer `time.perf_counter`, cinque ripetizioni,
  campioni conservati e tabelle testuali senza file di output.
- `esempi/grafici_u9.py` — grafici con matplotlib: sei famiglie di crescita
  da dati teorici dichiarati, visite di una e due scansioni, durate reali da
  campioni misurati; esportazione PNG con `fig.savefig` e senza `plt.show()`.
- `esempi/test_esempi_u9.py` - suite deterministica di verifica degli attesi
  del capitolo e delle proprietà dei sorgenti d'esempio.
- `starter-laboratorio/analisi_u9.py` - interfacce di analisi del LAB-PY-U9:
  `riepilogo_due_scansioni` completa, `riepilogo_una_scansione` e
  `conta_coppie` da completare, strumentazione di Fibonacci fornita.
- `starter-laboratorio/test_analisi_u9.py` - casi pubblici L01-L12 con i
  fallimenti attesi documentati e il caso L12 lasciato da progettare.
- `starter-laboratorio/misure_u9.py` - cornice del timer: regione cronometrata
  e raccolta dei campioni da completare, sintesi e tabella già impostate.
- `starter-laboratorio/grafici_u9.py` - cornice del grafico con serie,
  etichette, legenda e salvataggio da completare.
- `riferimento-laboratorio/` - le quattro controparti complete e verificate
  dello starter, con il caso L12 compilato.

## Esempi, starter e riferimento del laboratorio

La cartella contiene tre gruppi di file che descrivono tre momenti diversi:

- `esempi/` - i sorgenti completi che accompagnano il capitolo PY-13;
- `starter-laboratorio/` - la baseline **incompleta** del LAB-PY-U9, che dichiara di esserlo: i corpi da completare mancano e i test corrispondenti falliscono in modo visibile;
- `riferimento-laboratorio/` - la controparte completa dello starter, consultabile dopo le fasi L2-L3 come confronto formativo.

Le due cartelle del laboratorio contengono **moduli omonimi** - `analisi_u9.py`, `test_analisi_u9.py`, `misure_u9.py`, `grafici_u9.py` - e anche `esempi/` usa i nomi `misure_u9.py` e `grafici_u9.py`. Le tre suite vanno quindi eseguite **una alla volta**, ciascuna con il proprio percorso: eseguirle insieme in un'unica chiamata a `pytest` produce una collisione di import, perché il primo modulo caricato con quel nome copre gli altri. La stessa regola vale nella raccolta dello studente, dove un solo gruppo di file per volta viene copiato in `programmi/`.

## Comandi di esecuzione

I comandi sono indicati per la cartella `unita-09/` di questo repository. Con
`uv` non servono installazioni globali: le dipendenze richieste compaiono
nel comando. Nella raccolta dello studente gli stessi file si eseguono dalla
cartella `programmi/` del progetto didattico, dove `matplotlib` è dichiarata
fra le dipendenze con `uv add matplotlib`.

```powershell
# dimostrazioni dei moduli d'esempio (nessuna dipendenza esterna)
uv run python esempi/conteggi_scansioni.py
uv run python esempi/conteggi_cicli.py
uv run python esempi/confronto_fibonacci.py
uv run python esempi/capacita_dinamica.py

# esperimenti di misura: tabelle in stdout, nessun file scritto
uv run python esempi/misure_u9.py

# grafici: creare prima la cartella figure_u9, il programma non la crea
uv run --with matplotlib python esempi/grafici_u9.py

# suite di verifica, UNA ALLA VOLTA per la collisione dei nomi dei moduli
uv run --with pytest --with matplotlib python -m pytest esempi/test_esempi_u9.py -q
uv run --with pytest --with matplotlib python -m pytest riferimento-laboratorio/test_analisi_u9.py -q
uv run --with pytest --with matplotlib python -m pytest starter-laboratorio/test_analisi_u9.py -q
```

L'ultima suite è quella dello starter: alla prima esecuzione riporta **fallimenti attesi** per i corpi ancora da completare, e non deve produrre errori di import né di raccolta. Gli altri due gruppi sono verdi per intero: `esempi/` ha 105 test deterministici, `riferimento-laboratorio/` ne ha 21.

Per eseguire con l'interprete della stessa serie usata dal corso aggiungere
`--python 3.14` ai comandi precedenti, per esempio
`uv run --python 3.14 --with pytest --with matplotlib python -m pytest esempi/test_esempi_u9.py -q`.

I grafici vengono scritti in `figure_u9/` con i nomi
`06-crescite-conteggi.png`, `visite-scansioni.png` e
`07-scansioni-misure.png`, allineati agli asset del piano dell'Unità 9. Le
immagini generate non sono conservate in questo repository: le figure
definitive vivono accanto al capitolo nel sito e si rigenerano con il comando
sopra.

## Versioni verificate

- CPython 3.14.7 e CPython 3.12.13;
- pytest 9.1.1;
- matplotlib 3.11.2;
- Windows 11, esecuzione normale fuori dal debugger.

I sorgenti non usano costrutti successivi a quelli già impiegati nelle unità
precedenti: funzionano con le versioni dichiarate e con quelle compatibili
maggiori. Le durate stampate da `misure_u9.py` appartengono all'ambiente di
chi esegue e non sono riproducibili come valori assoluti.

## Ipotesi del modello di costo

Ogni esempio dichiarà unità contata e ipotesi nella propria docstring; il
modello comune è il seguente.

- Le operazioni su numeri di dimensione limitata hanno costo unitario: si
  contano visite, addizioni, confronti, passi di dimezzamento, celle
  visitate, scritture, copie, chiamate e frame, non byte né istruzioni
  dell'interprete.
- Il conteggio del corpo di un ciclo non include la valutazione finale falsa
  della guardia: serve una colonna distinta per contarla.
- Per Fibonacci: C è il numero di ingressi, D il massimo dei frame
  simultanei con il primo frame a profondità 1, S le nuove scritture nella
  memoria. La memoria NUOVA parte dalle sole basi `{0: 0, 1: 1}`; la memoria
  GIÀ POPOLATA è uno stato diverso e i due esperimenti non si aggregano. Le
  addizioni della versione con memoria coincidono con S; quelle
  dell'iterativa canonica dell'Unità 6 valgono `max(0, n - 1)`.
- Per Hanoi le mosse accodate alla lista sono OUTPUT: i suoi elementi sono
  Θ(2^n), mentre lo stack dei frame resta Θ(n). Per il fattoriale con base
  n = 0 si hanno n moltiplicazioni, n + 1 ingressi e n + 1 frame.
- Per la capacità dinamica il modello è didattico: sequenza vuota con
  capacità 1, scrittura di un riferimento per inserimento, raddoppio e copia
  dei riferimenti presenti quando la sequenza è piena, un'unità di costo per
  copia. Non descrive la formula di crescita di CPython, che adotta dettagli
  propri. I limiti `copie < 2m` e `costo < 3m` valgono sull'intera sequenza
  di m accodamenti: il singolo passo può essere lineare.
- Per le misure: `time.perf_counter()` con due letture e differenza in
  secondi, regione cronometrata limitata alle sole chiamate studiate, K
  chiamate per lotto quando una singola chiamata è troppo breve, cinque
  ripetizioni con tutti i campioni conservati, mediana come elemento centrale
  dei campioni ordinati e minimo/massimo come variabilità descrittiva, non
  come intervallo di confidenza.

Le funzioni ordinarie e quelle strumentate hanno contratti diversi: le
versioni con contatori non vanno cronometrate per attribuirne il tempo alle
versioni ordinarie. Nessun contatore è globale: si azzera a ogni esecuzione.
Ogni modulo è importabile senza stampe né misure: le dimostrazioni stanno nel
`main` protetto dalla guardia di avvio.

## Derivazione dai sorgenti delle unità precedenti

`esempi/confronto_fibonacci.py` deriva da
`unita-08/esempi/fibonacci_memoria_u8.py` per `fibonacci_mem`,
`fibonacci_diretto`, `fibonacci_iter`, `fibonacci_mem_osservata`,
`fibonacci_diretto_osservato` e `memoria_delle_basi`, e dalle versioni
canoniche dell'Unità 6 per `fibonacci_iter` e `hanoi`: le operazioni
rilevanti sono identiche agli originali. Le funzioni aggiuntive del file sono
`fibonacci_iter_osservata` (conteggio delle addizioni dell'iterativa),
`fattoriale`, `fattoriale_osservato` e `hanoi_osservato`, dichiarate con lo
stesso modello di C, D e S.
