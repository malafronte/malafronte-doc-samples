# Unità 12 - sorgenti Python d'esempio (cap. PY-16 … PY-19)

Sorgenti d'esempio dell'Unità 12 del corso di informatica della terza: moduli e
organizzazione del progetto, file, stream, byte e codifiche, eccezioni, diagnosi,
date, percorsi, file di testo e analisi delle parole. Questa versione del README
accompagna i **primi due blocchi** dei materiali (PY-16-PY-19); le cartelle del
laboratorio, delle applicazioni e della distribuzione locale arrivano con i
blocchi successivi e verranno aggiunte a questa mappa.

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
- `esempi/test_esempi_u12.py` - suite deterministica degli attesi dei capitoli
  PY-16-PY-19 e delle proprietà delle fixture.
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

## Esempi, errori intenzionali, starter e riferimento

La cartella contiene allo stato attuale un solo gruppo di file:

- `esempi/` - sorgenti **completi e corretti** che accompagnano i capitoli
  PY-16-PY-19; ogni frammento deliberatamente errato mostrato nei capitoli è
  isolato e commentato nei listati della pagina, e **non** si trova in questi
  file: la dimostrazione ordinaria non si interrompe;
- `dati/` - fixture sintetiche di riferimento, **in sola lettura**: gli
  esperimenti degli esercizi si fanno su copie, mai sovrascrivendo l'originale.

Le cartelle `starter-laboratorio/`, `riferimento-laboratorio/`,
`applicazioni-librerie/` e `distribuzione-locale/` non esistono ancora: il
README verrà aggiornato quando quei materiali entreranno nei blocchi
successivi, mantenendo la distinzione fra codice corretto, errori intenzionali,
starter incompleto e riferimento.

## Comandi di esecuzione

I comandi sono indicati per la cartella `unita-12/` di questo repository. Con
`uv` non servono installazioni globali: l'interprete e le dipendenze compaiono
nel comando. Nessun sorgente dei primi due blocchi richiede dipendenze esterne:
`random`, `datetime`, `subprocess`, `os`, `tempfile` e `pathlib` appartengono
alla libreria standard.

```powershell
# dimostrazioni dei moduli d'esempio (nessuna dipendenza esterna)
uv run --python 3.14 python esempi/utilita_u12.py
uv run --python 3.14 python esempi/codifiche_u12.py
uv run --python 3.14 python esempi/eccezioni_date_u12.py
uv run --python 3.14 python esempi/analisi_testo_u12.py
uv run --python 3.14 python esempi/percorsi_testo_u12.py

# la CLI dimostrativa chiede la scelta dal menu (0 termina)
uv run --python 3.14 python esempi/demo_import_u12.py

# la CLI dell'analisi riceve il percorso del file (0 ok, 1 errore, 2 uso)
uv run --python 3.14 python esempi/cli_testo_u12.py dati/testi/analisi_canonica.txt

# suite di verifica dei primi due blocchi
uv run --python 3.14 --with pytest python -m pytest esempi/test_esempi_u12.py -q
```

La suite è **una**: non ci sono ancora moduli omonimi fra `esempi/`, starter e
riferimento. Quando compariranno, le suite andranno eseguite una alla volta,
ciascuna con il proprio percorso, per la collisione dei nomi dei moduli.

## Versioni verificate

- CPython **3.14.7**, serie 3.14 usata dal corso;
- pytest 9.1.1, invocato con `uv run --with pytest`;
- Windows 11, esecuzione normale fuori dal debugger.

I sorgenti non usano costrutti successivi a quelli già impiegati nelle unità
precedenti, più `try`/`except`/`else`/`finally`, `raise` e i tipi `date`,
`datetime` e `timedelta` introdotti dal cap. PY-18 e le API di file e percorsi
(`open`, `with`, `pathlib`, `os.getenv`) introdotte dal cap. PY-19. I test non
usano `date.today()`: ogni data di riferimento è scritta nel test.

## Contratti e convenzioni dei primi due blocchi

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
