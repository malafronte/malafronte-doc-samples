# Unità 12 - sorgenti Python d'esempio (cap. PY-16 … PY-22)

Sorgenti d'esempio dell'Unità 12 del corso di informatica della terza: moduli e
organizzazione del progetto, file, stream, byte e codifiche, eccezioni, diagnosi,
date, percorsi, file di testo, analisi delle parole, record su CSV e JSON,
magazzino persistente, record binari a posizione calcolata e distribuzione
locale di una libreria personale. Questa versione del README accompagna i
**primi quattro blocchi** dei materiali (PY-16-PY-22); le cartelle del
laboratorio e delle applicazioni grafiche arrivano con i blocchi successivi e
verranno aggiunte a questa mappa.

Come per le altre unità, questi sorgenti non si distribuiscono come download dal
sito: le pagine li mostrano con `RemoteCode` e citano il percorso di questo
repository.

## Mappa dei file

- `esempi/utilita_u12.py` - modulo **riusabile** senza I/O: `valore_magazzino`
  calcola in centesimi il valore complessivo di un inventario già in memoria,
  con la precondizione dei campi dichiarata nel contratto.
- `esempi/demo_import_u12.py` - CLI dimostrativa che importa `utilita_u12`:
  genera un inventario riproducibile con `random.Random(7)` e lo presenta in due
  modi diversi **senza duplicare il calcolo**. `input` e `print` vivono solo in
  `main()`, sotto la guardia `if __name__ == "__main__"`.
- `esempi/codifiche_u12.py` - confronti di `str`, `bytes` e `bytearray` **in
  memoria**: codepoint contro byte UTF-8, accento precomposto contro
  combinante, firma `EF BB BF` e comportamento dei codec `utf-8` e `utf-8-sig`.
- `esempi/eccezioni_date_u12.py` - funzioni pure con `raise`, propagazione su due
  chiamate, registro di `try`/`except`/`else`/`finally`, giorni fra due date,
  anni compiuti con la convenzione del 1° marzo per il 29 febbraio, parsing con
  `datetime.strptime` e coordinatore `main()` con recupero ed EOF.
- `esempi/percorsi_testo_u12.py` - dimostrazioni di **percorsi e file di testo**
  (cap. PY-19): `Path` e radici di lavoro, variabile d'ambiente con default,
  lettura per iterazione/`readline`/`readlines` con EOF e terminatore, effetti
  di `w`, `a` e `x` su un file di prova, primi byte del file e diagnosi delle
  aperture. Gli esperimenti di scrittura usano una cartella temporanea.
- `esempi/analisi_testo_u12.py` - **analizzatore di testo** senza I/O di
  presentazione: `conta_parole` (una sola scansione, `casefold().split()`),
  `ordina_frequenze` (parola crescente a parità) e `analizza_file` (apertura
  UTF-8 con `with`, risultato documentato per la CLI).
- `esempi/cli_testo_u12.py` - coordinatore dell'analisi: apre il percorso
  ricevuto da riga di comando, presenta il risultato e traduce gli errori
  attesi in messaggi e codici di uscita (0, 1, 2), sotto la guardia di avvio.
- `esempi/dominio_magazzino_u12.py` - **dominio del magazzino** (cap. PY-20):
  schema dell'articolo, `valida_articolo`, conversioni `riga_a_articolo` e
  `articolo_a_riga`, CRUD con `cerca_articolo`, `inserisci_articolo`,
  `modifica_articolo`, `elimina_articolo`, i totali di `riepilogo_magazzino` e
  la presentazione monetaria `formatta_centesimi`. Nessun I/O.
- `esempi/persistenza_magazzino_u12.py` - **persistenza CSV** del magazzino:
  `carica_articoli` con politica «tutto valido oppure nessun archivio» e
  `salva_articoli` con il protocollo del temporaneo (validazione, temporaneo
  nella stessa directory, chiusura, sostituzione con `Path.replace`).
- `esempi/cli_magazzino_u12.py` - **CLI del magazzino**: menu `match/case`,
  flag delle modifiche pendenti, conferma `s/n` delle eliminazioni, salvataggio
  esplicito, politica dell'EOF e codici di uscita 0/1/2.
- `esempi/json_u12.py` - **serializzazione JSON**: `serializza_articoli` con
  `ensure_ascii=False` e `allow_nan=False`, `deserializza_articoli` con i tre
  controlli separati di sintassi, struttura e dominio, variante `strict` con
  `object_pairs_hook` contro i nomi duplicati, confronto CSV/JSON.
- `esempi/record_binari_u12.py` - **record binari a posizione calcolata**
  (cap. PY-21): `leggi_record_due_byte` e `aggiorna_record_due_byte` su record
  interi senza segno a 16 bit little-endian, offset `i * 2`, controlli di
  dominio **prima** della scrittura puntiforme in `r+b`, e `traccia_seek` che
  mostra `seek` da inizio, posizione corrente e fine. La dimostrazione della
  guardia usa una cartella temporanea: le fixture non vengono toccate.
- `esempi/test_esempi_u12.py` - suite deterministica degli attesi dei capitoli
  PY-16-PY-21, con la matrice MAG-01-MAG-20 del magazzino, le verifiche byte
  esatte dei record binari e le proprietà delle fixture.
- `dati/testi/frase_senza_bom.txt` e `dati/testi/frase_con_bom.txt` - **stesso
  testo** in UTF-8, senza e con la firma iniziale `EF BB BF`. Il testo contiene
  un accento precomposto (`è` = `U+00E8`), un accento combinante
  (`e` + `U+0300`) e una `U+FEFF` **interna**, per verificare che i due codec
  differiscano solo sull'inizio della sequenza.
- `dati/testi/analisi_canonica.txt` - dataset canonico dell'analizzatore
  (`Sole luna sole` / `mare LUNA sole`): totale 6, distinte 3, frequenze
  `sole 3`, `luna 2`, `mare 1`.
- `dati/testi/analisi_parita.txt` - dataset con parità di frequenza
  (`luna sole mare sole luna`): totale 5, la coppia `luna`/`sole` resta
  alfabetica in entrambe le classifiche.
- `dati/testi/analisi_vuota.txt` e `dati/testi/analisi_spazi.txt` - file **da
  zero byte** e file di soli spazi: entrambi danno totale 0 e classifiche
  vuote, senza divisioni o indicizzazioni non valide.
- `dati/testi/analisi_no_newline.txt` - testo canonico **senza il terminatore
  finale**: gli ultimi token restano conteggiati e nessuna riga va persa.
- `dati/testi/analisi_punteggiatura.txt` - `sole sole,`: secondo il contratto
  di tokenizzazione le due parole restano **distinte**.
- `dati/testi/analisi_con_bom.txt` - testo canonico **con** la firma `EF BB BF`:
  con `utf-8` la prima parola diventa `\ufeffsole`, con `utf-8-sig` l'analisi
  coincide con il canonico.
- `dati/testi/byte_incompatibili.txt` - byte `E8` non decodificabili come
  UTF-8: l'apertura riesce e la decodifica fallisce alla lettura.
- `dati/immagini/immagine_originale.bmp` - raster sintetico **BMP 24 bit non
  compresso** (8x8 pixel, 54 byte di intestazione + 192 byte di pixel).
- `dati/immagini/immagine_rinominata.dat` - copia dell'originale con nome ed
  estensione diversi e **byte identici**: il formato non dipende dal nome.
- `dati/immagini/immagine_troncata.bmp` - primi 94 byte dell'originale: la
  firma `BM` e la lunghezza dichiarata nell'intestazione restano leggibili, ma
  i byte effettivi sono meno di quelli dichiarati e la verifica completa fallisce.
- `dati/csv/magazzino_canonico.csv` - archivio canonico del magazzino con
  intestazione esatta `codice,descrizione,quantita,prezzo_centesimi` e i due
  record `007,"Vite, lunga",4,25` e `012,"Caffè ""A""",2,350`: codici con zeri
  iniziali, virgola nel campo, virgolette interne raddoppiate e accento.
  Riscritto dal programma produce **gli stessi byte** (UTF-8 senza BOM, LF).
- `dati/csv/magazzino_con_bom.csv` - stesso contenuto con la firma `EF BB BF`
  iniziale: ammesso in ingresso dal contratto (`utf-8-sig`), mai prodotto in
  uscita.
- `dati/csv/magazzino_quoting.csv` - tre record con campo su **due righe**
  fisiche: 3 record contro 5 righe, per distinguere record e riga del parser.
- `dati/csv/magazzino_schema_errato.csv` - intestazione con colonna mancante:
  il caricamento rifiuta l'intero formato.
- `dati/csv/magazzino_duplicati.csv` - due record con lo stesso codice `007`:
  il caricamento diagnostica il duplicato e non pubblica liste parziali.
- `dati/json/magazzino_canonico.json` - lista dei due articoli canonici in JSON
  (`indent=2`, `ensure_ascii=False`): la rilettura ricostruisce gli stessi
  record con `quantita` e `prezzo_centesimi` interi.
- `dati/json/magazzino_sintassi_errata.json` - documento non valido per il
  parser: `JSONDecodeError` con posizione.
- `dati/json/magazzino_struttura_errata.json` - JSON valido con radice di
  oggetto invece che di lista: diagnosi di struttura.
- `dati/json/magazzino_domini_errati.json` - struttura valida con `"quantita":
  true` nel secondo record: diagnosi di dominio sul campo.
- `dati/binari/record_canonici.bin` - archivio canonico dei record binari:
  tre interi senza segno a due byte little-endian `[10, 500, 65535]`, i byte
  `0A 00 F4 01 FF FF`, lunghezza 6. Nessuna intestazione: il record di indice
  `i` comincia all'offset `i * 2`.
- `dati/binari/record_vuoto.bin` - archivio da zero byte: nessun record
  disponibile, ogni indice è fuori intervallo.
- `dati/binari/record_troncato.bin` - primi **5 byte** del canonico: lunghezza
  dispari, record incompleto, diagnosi senza zero sintetico.
- `distribuzione-locale/autore/` - **progetto autore** della libreria personale
  `utilita_magazzino-u12` (cap. PY-22): layout `src`, package con API pubblica
  `valore_magazzino`, `formatta_centesimi` e `normalizza_codice`, test
  discriminanti, `pyproject.toml` con backend hatchling, `.python-version`,
  `uv.lock` e README con i comandi verificati.
- `distribuzione-locale/consumatore/` - **progetto consumatore** separato:
  dipende dalla wheel prodotta dall'autore, la installa nel proprio ambiente e
  la usa da `usa_utilita.py` senza accesso ai sorgenti dell'autore; il README
  documenta comandi, ricostruzione dell'ambiente e limiti della wheel locale.

## Esempi, errori intenzionali, starter e riferimento

La cartella contiene allo stato attuale tre gruppi di file:

- `esempi/` - sorgenti **completi e corretti** che accompagnano i capitoli
  PY-16-PY-21; ogni frammento deliberatamente errato mostrato nei capitoli è
  isolato e commentato nei listati della pagina, e **non** si trova in questi
  file: la dimostrazione ordinaria non si interrompe;
- `dati/` - fixture sintetiche di riferimento, **in sola lettura**: gli
  esperimenti degli esercizi si fanno su copie, mai sovrascrivendo l'originale;
- `distribuzione-locale/` - i due progetti della filiera del cap. PY-22,
  `autore/` e `consumatore/`, ciascuno con il proprio ambiente e il proprio
  `uv.lock`: il `dist/` dell'autore e le `.venv/` sono artefatti locali e non
  si versionano, come da `.gitignore` del repository.

Le cartelle `starter-laboratorio/`, `riferimento-laboratorio/` e
`applicazioni-librerie/` non esistono ancora: il README verrà aggiornato quando
quei materiali entreranno nei blocchi successivi, mantenendo la distinzione fra
codice corretto, errori intenzionali, starter incompleto e riferimento.

## Comandi di esecuzione

I comandi sono indicati per la cartella `unita-12/` di questo repository. Con
`uv` non servono installazioni globali: l'interprete e le dipendenze compaiono
nel comando. Nessun sorgente dei primi quattro blocchi richiede dipendenze
esterne: `random`, `datetime`, `subprocess`, `os`, `csv`, `json`, `tempfile` e
`pathlib` appartengono alla libreria standard.

```powershell
# dimostrazioni dei moduli d'esempio (nessuna dipendenza esterna)
uv run --python 3.14 python esempi/utilita_u12.py
uv run --python 3.14 python esempi/codifiche_u12.py
uv run --python 3.14 python esempi/eccezioni_date_u12.py
uv run --python 3.14 python esempi/analisi_testo_u12.py
uv run --python 3.14 python esempi/percorsi_testo_u12.py
uv run --python 3.14 python esempi/dominio_magazzino_u12.py
uv run --python 3.14 python esempi/json_u12.py
uv run --python 3.14 python esempi/record_binari_u12.py

# la CLI dimostrativa chiede la scelta dal menu (0 termina)
uv run --python 3.14 python esempi/demo_import_u12.py

# la CLI dell'analisi riceve il percorso del file (0 ok, 1 errore, 2 uso)
uv run --python 3.14 python esempi/cli_testo_u12.py dati/testi/analisi_canonica.txt

# la CLI del magazzino riceve il percorso dell'archivio CSV
# (0 uscita ordinaria, 1 interruzione o archivio non valido, 2 uso)
uv run --python 3.14 python esempi/cli_magazzino_u12.py dati/csv/magazzino_canonico.csv

# suite di verifica dei primi quattro blocchi
uv run --python 3.14 --with pytest python -m pytest esempi/test_esempi_u12.py -q

# filiera della libreria personale: i comandi girano nelle rispettive cartelle
cd distribuzione-locale/autore
uv sync                                     # ambiente proprio e progetto installato in modalità modificabile
uv run pytest tests/ -q                     # suite della libreria
uv build                                    # dist/ con wheel e sdist
cd ../consumatore
uv add ..\autore\dist\utilita_magazzino_u12-0.1.0-py3-none-any.whl
uv run python usa_utilita.py                # import dalla .venv del consumatore
```

La suite di `esempi/` è **una**; quella della libreria vive nel progetto autore
ed è separata. Non ci sono ancora moduli omonimi fra `esempi/`, starter e
riferimento: quando compariranno, le suite andranno eseguite una alla volta,
ciascuna con il proprio percorso, per la collisione dei nomi dei moduli.

## Versioni verificate

- CPython **3.14.7**, serie 3.14 usata dal corso;
- uv **0.12.15**, con backend di build hatchling per il progetto autore;
- pytest 9.1.1, invocato con `uv run --with pytest` (suite di `esempi/`) e come
  dipendenza di sviluppo del progetto autore;
- Windows 11, esecuzione normale fuori dal debugger.

I sorgenti non usano costrutti successivi a quelli già impiegati nelle unità
precedenti, più `try`/`except`/`else`/`finally`, `raise` e i tipi `date`,
`datetime` e `timedelta` introdotti dal cap. PY-18, le API di file e percorsi
(`open`, `with`, `pathlib`, `os.getenv`) introdotte dal cap. PY-19, i moduli
`csv`, `json` e `tempfile` del cap. PY-20 e le operazioni binarie
(`tell`/`seek`, `int.to_bytes`/`int.from_bytes`) del cap. PY-21. I test non
usano `date.today()`: ogni data di riferimento è scritta nel test.

## Contratti e convenzioni dei primi quattro blocchi

| Elemento | Convenzione |
|---|---|
| `valore_magazzino(articoli)` | lista di record già validi con `quantita` e `prezzo_centesimi` interi non negativi; risultato intero in **centesimi**; nessun I/O; nessuna modifica all'argomento; la validazione con `raise` arriva dopo il cap. PY-18 |
| `conta_parole(righe)` | iterabile di stringhe già decodificate attraversato **una volta**; risultato `(totale, frequenze)` con dizionario nuovo; ogni riga passa da `casefold().split()`; nessuna lista accumulata di tutte le parole, nessun I/O |
| `ordina_frequenze(frequenze, decrescente=False)` | lista **nuova** di coppie `(parola, frequenza)`; frequenza crescente o decrescente, **parola sempre crescente a parità**; il dizionario non è mutato; mai `reverse=True` sull'intera coppia |
| `analizza_file(percorso)` | apertura UTF-8 con `with`; risultato `{totale, frequenze, classifica_crescente, classifica_decrescente}`; errori di I/O e di decodifica **propagati** al coordinatore |
| Tokenizzazione | parola = token separato da spazi bianchi, normalizzato con `casefold`; la punteggiatura resta parte della parola (`sole` ≠ `sole,`); estensioni solo dichiarate e verificate con casi discriminanti |
| CLI dell'analisi | `cli_testo_u12.py`: un solo argomento (il percorso); codici di uscita 0/1/2; messaggi distinti per percorso assente, percorso non leggibile e byte non UTF-8; nessun risultato inventato come se il file fosse vuoto |
| Codice di dominio | funzioni senza `input` né `print`; il coordinatore `main()` tiene la sessione e sceglie messaggi e recupero |
| Avvio | la guardia `if __name__ == "__main__"` è l'unico avvio automatico: all'import non partono domande |
| Nuovi testi | UTF-8 **senza BOM**; la fixture `frase_con_bom.txt` è un ingresso esterno deliberato |
| BOM | `utf-8` conserva la firma iniziale come `U+FEFF`; `utf-8-sig` la omette **solo all'inizio**; nessuna rimozione indiscriminata di `U+FEFF` |
| Date | `data_iso` impone esattamente `AAAA-MM-GG` con cifre ASCII prima di `date.fromisoformat`, separando formato e calendario; forme compatte e settimanali rifiutate; `datetime.strptime` solo con formato esplicito; convenzione 29 febbraio → 1° marzo negli anni non bisestili |
| Errori | classi mirate; `ValueError` per formato non convertibile e per dominio violato, con diagnosi distinte; un argomento di tipo sbagliato resta un `TypeError`, cioè un difetto di programmazione, non «dato non valido» |
| Fixture | file sintetici in `dati/`, mai sovrascritti dagli esperimenti; le copie di lavoro appartengono a chi esegue; il `.gitattributes` dell'unità esclude `dati/**` dalla conversione dei terminatori di riga, perché le verifiche confrontano byte esatti |
| Schema del magazzino | campi `codice,descrizione,quantita,prezzo_centesimi` in quest'ordine; `codice` stringa non vuota senza spazi, univoco e a confronto esatto (`007` ≠ `7`); `descrizione` con almeno un carattere non bianco; `quantita` e `prezzo_centesimi` interi non negativi con `bool` escluso; prezzo in **centesimi** |
| `riga_a_articolo(riga, riferimento)` | quattro campi testuali → dizionario nuovo; conversione e dominio separati; `ValueError` con campo e riferimento; nessun risultato parziale. `articolo_a_riga` valida prima di ridurre il record a testo |
| CRUD del magazzino | ricerca: indice oppure `None`, mai `if indice:`; inserimento: copia del record e unicità verificate prima; modifica: candidato validato per intero, codice invariato; eliminazione senza domande, la conferma `s/n` è della CLI |
| `carica_articoli(percorso)` | UTF-8 con o senza BOM (`utf-8-sig`), `newline=""`, lettore `strict=True`; intestazione esatta, righe fisiche vuote ignorate, record e riga fisica distinti nei messaggi; politica **tutto valido oppure nessun archivio**; `FileNotFoundError`, `csv.Error`, `ValueError` e `UnicodeDecodeError` restano distinti |
| `salva_articoli(percorso, articoli)` | validazione integrale, temporaneo nella **stessa directory** (`NamedTemporaryFile` con `delete=False`), scrittura, chiusura, sostituzione con `Path.replace`; UTF-8 senza BOM e `lineterminator="\n"`; su guasto la destinazione resta valida, il temporaneo è rimosso e l'eccezione primaria si propaga |
| JSON | scrittura con `ensure_ascii=False` e `allow_nan=False`, UTF-8 senza BOM; lettura con sintassi (`JSONDecodeError`), struttura e dominio (`ValueError`) separati; nomi duplicati: `json.load` tiene l'ultimo valore, il rifiuto è dell'`object_pairs_hook` esplicito |
| CLI del magazzino | `cli_magazzino_u12.py`: menu 1-6/0; flag `modificato` (`True` solo su mutazione riuscita, `False` solo su salvataggio riuscito); conferma con `strip().casefold()`; EOF segnalato senza scritture implicite; codici di uscita 0/1/2 |
| Record binari | archivio di interi senza segno a **due byte** (16 bit) little-endian, senza intestazione; record di indice `i` all'offset `i * 2`; file canonico `[10, 500, 65535]` = `0A 00 F4 01 FF FF`, lunghezza 6 |
| `leggi_record_due_byte(percorso, indice)` | indice intero non negativo minore del numero di record; struttura verificata sulla lunghezza reale (multipli di 2); record incompleto o indice fuori dominio → `ValueError` con diagnosi, mai zero sintetico; file assente → `FileNotFoundError` |
| `aggiorna_record_due_byte(percorso, indice, valore)` | valore intero 0-65535 e indice validati **prima** della scrittura puntiforme in `r+b` (che non tronca); altri record e lunghezza invariati; nessun aggiornamento parziale su esito negativo; non è un protocollo transazionale |
| `traccia_seek(percorso)` | lista di triple `(operazione, posizione, byte_letti)` con `tell()` dopo ogni operazione: `seek` da inizio, posizione corrente e fine, e `b""` come fine file binario |
| Libreria `utilita_magazzino-u12` | `valore_magazzino` con **validazione esplicita** (interi non negativi, `bool` escluso, diagnosi con posizione e campo); `formatta_centesimi` con conversione centesimi→euro visibile (`800` → `"8,00 €"`, `5` → `"0,05 €"`); `normalizza_codice` elimina gli spazi esterni **senza** sostituire la validazione dell'archivio |
| Filiera di distribuzione | layout `src`, backend hatchling dichiarato, test nel progetto autore, `uv build` produce wheel e sdist; il consumatore è un progetto diverso che dipende dalla **wheel locale** (path + `uv.lock`) e importa il package dalla propria `.venv`, senza `sys.path` né copie dei sorgenti; `dist/` e `.venv/` non si versionano |
