# Errori e recupero (U12)

Politica degli errori del registro persistente: ogni classe di problema ha una
diagnosi distinta, il caricamento è **tutto valido oppure nessun archivio** e
il salvataggio non annuncia mai un successo che non è avvenuto.

## Classi di errore

| Classe | Quando | Esito di `carica_archivio` | Recupero |
|---|---|---|---|
| Assente | il file non esiste | `(None, "assente", ...)` | si parte da registro vuoto, oppure si carica un altro file |
| Sintassi | il parser JSON rifiuta il testo | `(None, "sintassi", riga e colonna)` | il file va corretto a mano o sostituito; nessun dato viene interpretato |
| Struttura | JSON valido ma fuori schema | `(None, "struttura", campo)` | si corregge il documento secondo [`schema-e-dati.md`](schema-e-dati.md) |
| Dominio | struttura valida ma valori non ammessi o codici duplicati | `(None, "dominio", campo e valore)` | si correggono i dati; la diagnosi nomina campo e valore |

La distinzione fra **sintassi** e **struttura** è centrale: PU12-06 riguarda un
documento che il parser non riesce a leggere — per esempio una chiave senza
virgolette — e la diagnosi riporta riga e colonna del parser; PU12-07 riguarda
un documento che il parser legge ma che non ha la forma dello schema. La
validazione di struttura non è quella del parser: sono due passaggi diversi.

Un errore di lettura diverso dall'assenza del file — per esempio permessi
insufficienti — non viene classificato: è un errore del sistema operativo e si
propaga. Nessun `except Exception` viene usato come rimedio ordinario.

## Salvataggio che preserva il file precedente

Procedura di `salva_archivio`:

1. costruzione del documento e del testo JSON in memoria;
2. scrittura su un file **temporaneo** nella cartella di destinazione;
3. sostituzione del file di destinazione con il temporaneo.

Se la scrittura o la sostituzione falliscono: il file precedente resta
**identico nei byte**, il temporaneo viene eliminato, il risultato è `False` e
nessun messaggio di successo viene mostrato. Le modifiche restano disponibili
in memoria: il guasto distrugge il salvataggio, non il lavoro della sessione.

I guasti si provocano in modo **deterministico** nei test intercettando le
operazioni interne `_scrivi_temporaneo` e `_sostituisci_file`: non si usano i
permessi della cartella, che dipendono dal programma in esecuzione. I test
`test_pu12_08` e `test_pu12_08_bis` confrontano i byte del file prima e dopo il
guasto e controllano che il temporaneo non resti sulla cartella.

## Modifiche pendenti, uscita e EOF

- La sessione nasce **non inizializzata** (`registro = None`), non come
  archivio vuoto. Prima di consultare, modificare, salvare o esportare si
  esegue `carica`: un archivio valido inizializza il registro; un file
  assente inizializza una lista vuota senza scrivere; un primo caricamento invalido
  lascia la sessione non inizializzata e il file invariato. Così `salva`
  prima del caricamento non può cancellare un archivio già presente.
- Un ricaricamento invalido conserva il registro già inizializzato: nessun
  risultato parziale sostituisce i dati in memoria.
- Ogni inserimento, aggiornamento ed eliminazione **riuscito** rende pendente
  il salvataggio; un'operazione rifiutata non lo rende pendente.
- `carica` con modifiche pendenti viene **rifiutato**, senza perdere i record
  né azzerare l'avviso. Si può salvare e poi ricaricare, oppure uscire
  confermando la perdita. Un salvataggio fallito mantiene questa protezione.
- `esci` con modifiche pendenti chiede conferma e **non salva in silenzio**;
  con `n` la sessione prosegue.
- La fine dell'input (EOF) — su qualunque punto di lettura — termina la
  sessione con un messaggio esplicito e nessun salvataggio automatico: le
  modifiche non salvate restano solo in memoria.

I dieci test `test_cli_*` di `test_persistenza_u12.py` verificano le sessioni
complete con input predisposti, le domande e i byte dei file: inizializzazione,
rifiuti, ricaricamento, salvataggio fallito, EOF e svuotamento intenzionale
dopo il caricamento. Si affiancano ai test delle API di dominio e persistenza.

## Riavvio e ripristino

Dopo un salvataggio riuscito il riavvio ricostruisce lo stato equivalente:
stessi codici con zeri iniziali, stessi interi in centesimi, stesse
destinazioni, stesso ordine. Il confronto fra stato a fine sessione e stato
dopo il riavvio è dimostrato da `test_pu12_09`, che salva, carica in un
registro nuovo e confronta i record. Se il salvataggio fallisce, il riavvio
ricarica l'ultimo archivio valido: è il file a fare da punto di ripristino e
per questo va preservato.
