# Unità 12 - sorgenti Python d'esempio (cap. PY-16, PY-17, PY-18)

Sorgenti d'esempio dell'Unità 12 del corso di informatica della terza: moduli e
organizzazione del progetto, file, stream, byte e codifiche, eccezioni, diagnosi
e date. Questa versione del README accompagna il **primo blocco** dei materiali
(PY-16-PY-18); le cartelle del laboratorio, delle applicazioni e della
distribuzione locale arrivano con i blocchi successivi e verranno aggiunte a
questa mappa.

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
- `esempi/test_esempi_u12.py` - suite deterministica degli attesi dei capitoli
  del primo blocco e delle proprietà delle fixture.
- `dati/testi/frase_senza_bom.txt` e `dati/testi/frase_con_bom.txt` - **stesso
  testo** in UTF-8, senza e con la firma iniziale `EF BB BF`. Il testo contiene
  un accento precomposto (`è` = `U+00E8`), un accento combinante
  (`e` + `U+0300`) e una `U+FEFF` **interna**, per verificare che i due codec
  differiscano solo sull'inizio della sequenza.
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
  PY-16-PY-18; ogni frammento deliberatamente errato mostrato nei capitoli è
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
nel comando. Nessun sorgente del primo blocco richiede dipendenze esterne:
`random`, `datetime`, `subprocess` e `pathlib` appartengono alla libreria
standard.

```powershell
# dimostrazioni dei moduli d'esempio (nessuna dipendenza esterna)
uv run --python 3.14 python esempi/utilita_u12.py
uv run --python 3.14 python esempi/codifiche_u12.py
uv run --python 3.14 python esempi/eccezioni_date_u12.py

# la CLI dimostrativa chiede la scelta dal menu (0 termina)
uv run --python 3.14 python esempi/demo_import_u12.py

# suite di verifica del primo blocco
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
`datetime` e `timedelta` introdotti dal cap. PY-18. I test non usano
`date.today()`: ogni data di riferimento è scritta nel test.

## Contratti e convenzioni del primo blocco

| Elemento | Convenzione |
|---|---|
| `valore_magazzino(articoli)` | lista di record già validi con `quantita` e `prezzo_centesimi` interi non negativi; risultato intero in **centesimi**; nessun I/O; nessuna modifica all'argomento; la validazione con `raise` arriva dopo il cap. PY-18 |
| Codice di dominio | funzioni senza `input` né `print`; il coordinatore `main()` tiene la sessione e sceglie messaggi e recupero |
| Avvio | la guardia `if __name__ == "__main__"` è l'unico avvio automatico: all'import non partono domande |
| Nuovi testi | UTF-8 **senza BOM**; la fixture `frase_con_bom.txt` è un ingresso esterno deliberato |
| BOM | `utf-8` conserva la firma iniziale come `U+FEFF`; `utf-8-sig` la omette **solo all'inizio**; nessuna rimozione indiscriminata di `U+FEFF` |
| Date | `data_iso` impone esattamente `AAAA-MM-GG` con cifre ASCII prima di `date.fromisoformat`, separando formato e calendario; forme compatte e settimanali rifiutate; `datetime.strptime` solo con formato esplicito; convenzione 29 febbraio → 1° marzo negli anni non bisestili |
| Errori | classi mirate; `ValueError` per formato non convertibile e per dominio violato, con diagnosi distinte; un argomento di tipo sbagliato resta un `TypeError`, cioè un difetto di programmazione, non «dato non valido» |
| Fixture | file sintetici in `dati/`, mai sovrascritti dagli esperimenti; le copie di lavoro appartengono a chi esegue; il `.gitattributes` dell'unità esclude `dati/**` dalla conversione dei terminatori di riga, perché le verifiche confrontano byte esatti |
