# Dossier di analisi — costo di riepilogo e consultazione (U9)

Oggetto dell'analisi: le implementazioni effettivamente usate dalla raccolta,
`riepilogo_per_destinazione(registro)` e `cerca_preventivo(registro, codice)`,
nella versione di `programmi/spedizione_u5.py`. Le funzioni di produzione non
sono state modificate per l'analisi: le varianti strumentate vivono in
`programmi/analisi_costi_u9.py`.

## Modello di costo

| Elemento | Dichiarazione |
|---|---|
| Dimensione `n` | numero dei record del registro |
| Lunghezza dei codici `L` | 6 caratteri in tutti i dataset generati; il costo di un confronto fra codici si considera costante e i codici sono stringhe con zeri iniziali |
| Operazione contata — riepilogo | **visita** di un record: lettura dell'elemento e aggiornamento dei due accumulatori; si contano separatamente le visite e gli aggiornamenti (2 per record) |
| Operazione contata — consultazione | **confronto** fra codici nella scansione con arresto |
| Casi studiati | riepilogo su registro di `n` record; consultazione con codice presente in prima posizione, in ultima posizione, assente |
| Spazio | riepilogo: due record di accumulo, indipendenti da `n`; consultazione: nessuno spazio aggiuntivo; stack costante, versioni iterative |
| Variante | nessuna: il progetto non prescrive modifiche algoritmiche e il codice resta com'è |

## Previsione scritta prima delle misure

Sulla base del codice: il riepilogo attraversa tutti gli `n` record una
volta, quindi le visite valgono `n` e gli aggiornamenti `2n`; la sua durata
cresce in modo proporzionale a `n`, più un costo fisso della chiamata
(costruzione dei due gruppi iniziali) che su `n = 0` è l'unica voce presente.
La scansione con arresto confronta i codici fino al primo indovinato: il primo
record costa 1 confronto, l'ultimo e l'assente ne costano `n`. Con `n` piccoli
il costo fisso pesa più della scansione; al crescere di `n` le due operazioni
si distinguono per costanti, non per forma di crescita.

## Distinzione fra conteggio e tempo

Il **conteggio** è esatto e indipendente dalla macchina: `visite = n`,
`aggiornamenti = 2n`, `confronti = 1 / n / n` secondo la posizione. Il
**tempo** è una misura empirica sulla postazione indicata: dipende
dall'interprete, dal carico della macchina e dalla costante di ogni
operazione. Nessuna delle due grandezze dimostra da sola un ordine di
crescita: la prima lo deriva dal codice, la seconda lo mostra su tre
dimensioni.

Caso di riferimento PU9-03: sul registro con codici `["007", "008", "009"]` la
scansione con arresto produce **1 / 3 / 3 confronti** per le ricerche `007`,
`009` e assente. Il dato vale per questa variante con arresto, non è un
requisito di qualunque implementazione corretta.

## Protocollo sperimentale

1. **Generazione deterministica**: `genera_registro(n)` costruisce codici
   numerici a sei cifre, destinazioni alternate e totali da 0 a 600 centesimi,
   senza casualità. Lo stesso `n` produce sempre lo stesso registro.
2. **Correttezza prima del timer**: per ogni dimensione i risultati delle
   varianti strumentate sono confrontati con quelli delle funzioni di
   produzione e i conteggi con le formule del modello; la misura parte solo se
   i controlli superano.
3. **Regioni cronometrate**: `time.perf_counter`, due letture e differenza,
   sole chiamate studiate dentro la regione; generazione, stampe e grafico
   restano fuori.
4. **Lotti e ripetizioni**: 20 chiamate per lotto, 5 ripetizioni, campione
   singolo = tempo medio per chiamata; tutti i campioni sono conservati in
   [`risultati/unita-09/misure_u9.json`](../../../risultati/unita-09/misure_u9.json).
5. **Stessi dati per le procedure confrontate**: ogni operazione usa le stesse
   istanze di registro delle altre.

## Campioni misurati

Postazione: Windows 11, CPython 3.14.7 (uv 0.12.15), AMD Ryzen 7 8845HS,
esecuzione normale fuori dal debugger. Durate in millisecondi per chiamata.

| Operazione | n | Operazioni contate | Min | Mediana | Max |
|---|---:|---|---:|---:|---:|
| riepilogo per destinazione | 100 | 100 visite | 0,0131 | 0,0132 | 0,0138 |
| ricerca, ultima posizione | 100 | 100 confronti | 0,0038 | 0,0038 | 0,0039 |
| ricerca, codice assente | 100 | 100 confronti | 0,0037 | 0,0037 | 0,0040 |
| riepilogo per destinazione | 1.000 | 1.000 visite | 0,1242 | 0,1248 | 0,1445 |
| ricerca, ultima posizione | 1.000 | 1.000 confronti | 0,0343 | 0,0344 | 0,0364 |
| ricerca, codice assente | 1.000 | 1.000 confronti | 0,0334 | 0,0454 | 0,0555 |
| riepilogo per destinazione | 10.000 | 10.000 visite | 1,2901 | 1,3345 | 1,3879 |
| ricerca, ultima posizione | 10.000 | 10.000 confronti | 0,3368 | 0,3450 | 0,4239 |
| ricerca, codice assente | 10.000 | 10.000 confronti | 0,3151 | 0,3321 | 0,4240 |

La tabella è l'equivalente del grafico
[`risultati/unita-09/costi_u9.png`](../../../risultati/unita-09/costi_u9.png),
prodotto da `programmi/grafico_costi_u9.py` a partire dagli stessi campioni.

## Consultazioni ripetute

Sul registro di 10.000 record, una sequenza di `q = 10` consultazioni con
codici distribuiti nel registro costa **1.675 confronti complessivi**: la
somma dei costi delle singole query, con la preparazione del registro
separata e non conteggiata. Se le consultazioni fossero molte di più, la
scelta saggia sarebbe costruire una struttura d'indice — estensione
selezionabile del progetto, non richiesta dal nucleo.

## Conclusione: che cosa è provato e che cosa è osservato

**Provato dal codice e dai conteggi**: il riepilogo visita ogni record una
volta (`n` visite, `2n` aggiornamenti); la scansione con arresto confronta da
1 a `n` codici secondo la posizione e `n` per un assente; nessuna delle due
procedure modifica il registro; il riepilogo usa spazio costante.

**Osservato sulle misure**: le mediane crescono da 0,013 ms a 1,33 ms per il
riepilogo e da 0,004 ms a 0,33 ms per la ricerca quando `n` passa da 100 a
10.000; il riepilogo costa circa quattro volte la ricerca sulla stessa
dimensione, differenza dovuta alle costanti — due scritture per record contro
un solo confronto.

**Non dedotto dai dati**: un ordine di crescita. Tre dimensioni e una
mediana non dimostrano una complessità asintotica: la proporzionalità a `n`
deriva dal codice, i tempi la rendono plausibile su questa macchina. Non si
estendono le conclusioni a macchine diverse, a `n` non sperimentati o a
codici di lunghezza diversa da `L = 6`.

## Limiti dell'esperimento

- Solo tre dimensioni sostenibili: `n` molto più grandi non sono stati
  misurati e non servono agli obiettivi didattici.
- Una sola postazione, nessuna ripetizione su altri ambienti: i tempi non sono
  valori di accettazione e non vanno confrontati con soglie assolute.
- La variante strumentata e quella ordinaria hanno la stessa struttura, ma
  non si attribuisce il tempo della prima alla seconda: i due ruoli restano
  separati.
- La lunghezza dei codici è fissata a `L = 6`: crescerebbe `L`, il costo dei
  confronti crescerebbe con essa e andrebbe dichiarato come parametro.

## Regressione

La suite U5-U8 è stata rieseguita dopo l'analisi senza modifiche ai contratti:
Nella fotografia U9, `uv run pytest -q` riporta 78 test superati, dei quali
9 di questa tappa. Le
funzioni di produzione sono invariate e i risultati sono controllati prima dei
tempi, come richiesto dalla milestone M38.
