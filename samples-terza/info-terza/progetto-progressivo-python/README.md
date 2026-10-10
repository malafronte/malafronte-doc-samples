# Codice completo del progetto progressivo Python

Raccolta delle **versioni complete di riferimento** della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito info-terza, per le tappe U1-U15. Ogni cartella `unita-NN/` è la
**fotografia completa** della raccolta dello studente al termine di quella
unità: contiene tutti i programmi raggiunti fino a lì, la documentazione, la
configurazione dell'ambiente e le prove.

Le fotografie sono cumulative e autonome: una cartella copiata altrove si
esegue con i soli comandi del proprio README, senza dipendere dalle altre. La
duplicazione dei piccoli sorgenti fra una fotografia e la successiva è
deliberata: permette il confronto diretto dei due stati senza usare commit, tag
o branch di Git.

Questi sorgenti sono **una possibile realizzazione completa**, con scelte
motivate e limiti dichiarati: non sostituiscono progettazione, prove,
spiegazione e modifica del lavoro dello studente. Gli altri progetti autonomi e
le prove sommative mantengono il proprio regime di soluzioni.

## Indice delle tappe

| U | Traguardo della tappa | Milestone | Incremento principale | Sorgenti principali | Prove |
|---|---|---|---|---|---|
| [1](unita-01/) | Raccolta iniziale | M0-M5 | Progetto `uv`, tre programmi, flusso sorgente-processo | `01_hello.py`, `02_benvenuto.py`, `03_messaggio_multiriga.py` | output esatti verificati |
| [2](unita-02/) | Tempo di trasferimento | M6-M10 | Input, conversioni, f-string | `trasferimento_dati.py` | casi P1-P9 + 2 propri |
| [3](unita-03/) | Preventivo di spedizione | M11-M15 | Selezione, validazione con priorità | `preventivo_spedizione.py` | casi P01-P19 + 4 propri |
| [4](unita-04/) | Gioco a tentativi | M16-M20 | Ciclo, stato, limite, annullamento | `indovina_numero.py` | casi P01-P15 + 3 propri |
| [5](unita-05/) | Funzioni e test | M21-M27 | Funzioni pure, pytest, liste di preventivi | `spedizione_u5.py`, `test_spedizione_u5.py` | SP01-SP22, SP-L01-SP-L06 |
| [6](unita-06/) | Totale ricorsivo | M28-M30 | Ricorsione su `quanti`, confronto con U5 | `spedizione_u5.py`, `test_totale_ricorsivo_u6.py` | PR01-PR07 + discriminanti |
| [7](unita-07/) | Tabelle di sintesi | M31-M33 | Coppie, normalizzazione, sopra-media | `spedizione_u5.py`, `test_sintesi_u7.py` | PU01-PU09 + 3 propri |
| [8](unita-08/) | Registro di record | M34-M36 | Record, codici univoci, riepiloghi | `spedizione_u5.py`, `test_registro_u8.py` | PU8-01-PU8-09 + 3 propri |
| [9](unita-09/) | Analisi del costo | M37-M39 | Conteggi, misure, dossier | `analisi_costi_u9.py`, `grafico_costi_u9.py`, `test_analisi_u9.py` | PU9-01-PU9-08 |
| [10](unita-10/) | Viste ordinate | M40-M42 | Inserimento stabile, ricerca dicotomica | `spedizione_u5.py`, `test_viste_u10.py` | PU10-01-PU10-08 + 2 propri |
| [11](unita-11/) | Strategie a confronto | M43-M45 | MergeSort, primo indice, esperimento | `confronto_ordinamenti_u11.py`, `test_ordinamenti_u11.py` | PU11-01-PU11-08 + 2 propri |
| [12](unita-12/) | Persistenza ed errori | M46-M48 | Moduli, JSON, guasti, riavvii | `registro_dominio.py`, `registro_persistenza.py`, `registro_cli.py`, `test_persistenza_u12.py` | PU12-01-PU12-10 + 3 propri |
| [13](unita-13/) | Dalla soluzione procedurale agli oggetti | M49-M51 | Classe di sessione, conversioni esplicite, snapshot protetti | `registro_oggetti_u13.py`, `registro_cli_u13.py`, `test_oggetti_u13.py` | PU13-01-PU13-08 + 2 propri |
| [14](unita-14/) | Oggetti robusti e modello dati | M52-M54 | Valore frozen, raccolta responsabile, eccezioni di dominio | `registro_modello_u14.py`, `registro_cli_u14.py`, `test_modello_u14.py` | PU14-01-PU14-08 + 2 propri |
| [15](unita-15/) | Componenti intercambiabili | M55-M57 | Criteri di consultazione, client stabile, variante breve | `registro_consultazione_u15.py`, `consultazione_cli_u15.py`, `test_consultazione_u15.py` | PU15-01-PU15-08 + 3 propri |

I numeri di milestone corrispondono a quelli della pagina del progetto: U1-M0-M5,
U2-M6-M10, U3-M11-M15, U4-M16-M20, U5-M21-M27, U6-M28-M30, U7-M31-M33,
U8-M34-M36, U9-M37-M39, U10-M40-M42, U11-M43-M45, U12-M46-M48, U13-M49-M51,
U14-M52-M54, U15-M55-M57.

## Come si leggono le fotografie

- **Comandi**: ogni README riporta i comandi verificati per la propria cartella,
  a partire da `uv sync --frozen` e `uv run pytest -q`.
- **Sessioni reali**: gli output documentati sono quelli realmente osservati
  sulla postazione indicata in ciascun README, compresi i limiti intenzionali
  degli errori U2-U5.
- **Differenze**: la sezione «Differenze rispetto alla tappa precedente» elenca
  i soli file nuovi o modificati: il confronto ordinario si fa leggendola e
  affiancando le due cartelle.
- **Prove**: la mappa delle prove indica come si verifica ogni requisito. Le
  suite di test cumulano i casi storici e quelli nuovi: `uv run pytest -q`
  esegue tutti i test della fotografia.

I programmi di laboratorio citati dagli alberi del progetto non sono duplicati
qui: i materiali canonici degli starter e dei laboratori restano nelle cartelle
`unita-01` … `unita-15` di `samples-terza/info-terza/` e vengono collegati dalle
pagine del sito.

## Convenzioni

- CPython 3.14, `uv` come gestore dell'ambiente, `pytest` per le suite da U5 e
  `matplotlib` per i grafici da U9.
- Codice con costrutti già trattati a quella tappa del corso: U1-U4 non
  introducono funzioni, eccezioni o test automatici; la suddivisione in moduli
  per responsabilità è della tappa U12.
- Nessuna cronologia Git simulata, nessuna riflessione personale finta, nessuna
  sessione di debugger mai svolta: quegli artefatti sono lavoro dello studente.
- I dati sono soltanto sintetici; le durate misurate appartengono alla
  postazione che le ha prodotte e non sono valori di accettazione.
