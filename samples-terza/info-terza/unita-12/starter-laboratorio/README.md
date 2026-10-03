# Starter del LAB-PY-U12 — archivio materiali di laboratorio

Questa è una **baseline incompleta, dichiarata tale**, e non la soluzione del laboratorio. `dominio_archivio_u12.py` presenta firme, docstring e contratti di validazione, conversione e CRUD con i corpi che sollevano `NotImplementedError` e nominano la fase di completamento; `persistenza_archivio_u12.py` espone i contratti di caricamento e salvataggio con le due funzioni di servizio `_valida_intestazione` e `_valida_raccolta` già fornite; `cli_archivio_u12.py` contiene menu, righe di presentazione e normalizzazione della conferma **completi**, con il coordinamento di `main` da completare; `test_archivio_u12.py` contiene i casi pubblici L01-L11 e lascia L12 come caso da progettare. Il primo esito atteso è una suite con fallimenti chiari sui corpi mancanti, non un difetto della copia.

## I file dello starter

| File | Contenuto | Stato |
|---|---|---|
| `dominio_archivio_u12.py` | `valida_materiale`, `cerca_materiale`, `inserisci_materiale`, `modifica_materiale`, `elimina_materiale` | corpi da completare in L2 |
| `dominio_archivio_u12.py` | `riga_a_materiale`, `materiale_a_riga` | corpi da completare in L3 e L4 |
| `dominio_archivio_u12.py` | `riepilogo_archivio` | fornita completa |
| `persistenza_archivio_u12.py` | `carica_materiali` | corpo da completare in L3 |
| `persistenza_archivio_u12.py` | `salva_materiali` | corpo da completare in L4 |
| `persistenza_archivio_u12.py` | `_valida_intestazione`, `_valida_raccolta` | fornite complete |
| `cli_archivio_u12.py` | `mostra_menu`, `riga_materiale`, `righe_situazione`, `normalizza_conferma` | fornite complete |
| `cli_archivio_u12.py` | `main` | corpo da completare in L5, da affinare in L6 e L7 |
| `test_archivio_u12.py` | casi pubblici L01-L12 | L12 da progettare |
| `dati-ingresso/` | cinque archivi di prova, byte-esatti | forniti, **da non modificare** |

## Le fixture di `dati-ingresso/`

| File | Contenuto | Primo esito atteso |
|---|---|---|
| `archivio_materiali.csv` | intestazione e due record con virgola, virgolette doppie, accento e zeri iniziali | caricamento dei due record con `quantita` intera |
| `archivio_vuoto.csv` | la sola intestazione | lista vuota e riepilogo a zero |
| `archivio_con_bom.csv` | come il canonico, con i byte `EF BB BF` iniziali | stesso caricamento del canonico grazie a `utf-8-sig` |
| `archivio_intestazione_errata.csv` | manca la colonna `quantita` | `ValueError` che nomina la colonna mancante |
| `archivio_duplicati.csv` | il codice `007` ripetuto | `ValueError` che nomina il duplicato |

I file sono UTF-8 con terminatore `LF` e senza BOM, salvo dove dichiarato: sono byte-esatti e il repository li protegge dalle conversioni di fine riga. Non si scrive in questa cartella durante la sessione: le prove di scrittura usano le copie di lavoro in `dati/unita-12/lavoro/`.

## Dove copiare i file

I sorgenti sono nel [repository degli esempi](https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-terza/info-terza/unita-12/starter-laboratorio) e mostrati nella pagina del [LAB-PY-U12](/info-terza/laboratori/laboratorio-python/unita-12-archivio-persistente/). Copiarli nella raccolta esistente `raccolta-programmi`, non in un nuovo progetto:

```text
raccolta-programmi/
├── programmi/
│   ├── dominio_archivio_u12.py      <- corpi da completare in L2, L3 e L4
│   ├── persistenza_archivio_u12.py  <- corpi da completare in L3 e L4
│   ├── cli_archivio_u12.py          <- main da completare in L5
│   └── test_archivio_u12.py         <- casi pubblici L01-L12
├── dati/
│   └── unita-12/
│       ├── ingresso/                <- le cinque fixture, copiate e non modificate
│       └── lavoro/                  <- archivio della sessione e copie di prova
└── documentazione/
    └── unita-12/
        ├── schema-e-contratti.md
        ├── sessioni-e-diagnosi.md
        └── verifica.md
```

Ordine di copia:

1. Creare `dati/unita-12/ingresso/`, `dati/unita-12/lavoro/` e `documentazione/unita-12/` nell'editor o nel file system, perché nessun programma le crea al posto dello studente.
2. Copiare i quattro file di `programmi/` e le cinque fixture in `ingresso/`.
3. Eseguire subito la suite e registrare il primo esito atteso: 33 fallimenti per `NotImplementedError` e 2 superati, con i corpi forniti.
4. Non copiare i file di `riferimento-laboratorio/` durante la sessione: il riferimento si legge dopo le fasi L2-L3, come confronto formativo.

Non eseguire `uv init` né `git init` dentro `programmi/`: l'ambiente è quello della raccolta, con la `.venv` e `uv` già adottati. Le firme, i contratti e i casi pubblici non vanno modificati: la suite descrive comportamenti attesi e si estende soltanto con il caso L12. `riepilogo_archivio`, `_valida_intestazione`, `_valida_raccolta`, `mostra_menu`, `riga_materiale`, `righe_situazione` e `normalizza_conferma` sono forniti completi e verificati: si usano, non si riscrivono. Gli `import` già dichiarati nei moduli incompleti sono quelli necessari ai corpi da completare.

## Da quale cartella eseguire

Dalla root di `raccolta-programmi`:

```powershell
uv run python --version
uv run python programmi/cli_archivio_u12.py dati/unita-12/lavoro/archivio.csv
uv run --with pytest python -m pytest programmi/test_archivio_u12.py -q
```

Le suite dello starter e del riferimento hanno moduli omonimi e si eseguono in **processi distinti**, ciascuna dalla propria cartella: non lanciare `pytest` sulla radice di un repository che contenga entrambe le copie.

## Confronto con il riferimento

Il [riferimento formativo](https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-terza/info-terza/unita-12/riferimento-laboratorio) contiene gli stessi quattro file con i corpi completati e una suite identica, che supera tutti i casi. Lo si confronta **dopo** il tentativo: il valore del lavoro sta nel contratto rispettato, non nella copia del corpo. Le differenze ammesse riguardano la forma interna dei corpi; firme, esiti, eccezioni e messaggi di diagnosi restano quelli del contratto.
