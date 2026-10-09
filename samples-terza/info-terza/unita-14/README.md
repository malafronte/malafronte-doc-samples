# Unità 14 - sorgenti Python d'esempio (cap. OOP-03 e OOP-04)

Sorgenti d'esempio dell'**Unità 14** del corso di informatica della terza:
oggetti robusti, composizione e modello dati. Contengono proprietà e
invarianti su più campi, attributi di classe e di istanza, metodi di
classe e statici, rappresentazioni, uguaglianza, dataclass, eccezioni di
dominio, l'applicazione completa delle prenotazioni di aule con CSV e CLI,
il confronto del magazzino con proprietà e raccolta composta e il
controllore simulato con sensore e attuatore.

Come per le altre unità, questi sorgenti non si distribuiscono come download
dal sito: le pagine li mostrano con `RemoteCode` e citano il percorso di
questo repository.

## Mappa dei file

### `esempi/`

- `volume_audio_base_u14.py` - **proprietà e dati derivati** (OOP-03 B):
  `VolumeAudio` a un campo, livello intero 0–100 e silenzio calcolato.
- `volume_audio_u14.py` - **invariante su più campi** (OOP-03 C):
  livello e limite con `0 <= livello <= limite_massimo <= 100`;
  `configura` valida tutta la coppia prima delle scritture.
- `colori_espliciti_u14.py` - **metodi e modello dati esplicito** (OOP-03 E–G):
  `ColoreRGB` con factory nero/bianco, proiezione in tupla, regola statica,
  `str`, `repr` e confronto di tutte le componenti fra istanze dello stesso tipo.
- `colori_modello_dati_u14.py` - **dataclass e valori** (OOP-03 H–I):
  `ColoreRGBDataclass` mutabile e `ColoreRGB` frozen; `SchedaColori`
  con default indipendente e `DiarioFrozen` con contenuto mutabile.
- `palette_composizione_u14.py` - **relazioni e delega** (OOP-04 A–C):
  `Palette` copia il contenitore, condivide colori frozen e cerca per valore;
  `PannelloAudio` compone un volume proprio e aggrega una palette esterna.

I moduli seguenti restano disponibili per le attività autonome e i confronti
storici. Non sono prerequisiti nascosti dei nuovi esempi introduttivi:

- `limiti_proprieta_u14.py` - **applicazione alternativa di proprietà e invarianti**:
  `Limiti` con lettura, scrittura controllata, `ampiezza` derivata e
  l'operazione completa `imposta`; ogni rifiuto lascia lo stato intatto.
- `attributi_metodi_u14.py` - **classe/istanza e applicazione alle durate**:
  `Scheda` con dato di classe e la `SchedaCondivisa` difettosa, `Durata`
  con factory `da_minuti` e validatore statico confrontato con la funzione
  di modulo.
- `misure_modello_dati_u14.py` - **applicazione alle misure**, compreso il
  problema algoritmico T10: `MisuraEsplicita` con `__str__`/`__repr__`/`__eq__`,
  `MisuraDataclass` con `__post_init__`, `MisuraFrozen`, la
  `SchedaMisurazioni` con `default_factory`, il `DiarioFrozen` che mostra
  il limite di `frozen` e la `MisuraCheStampa` difettosa.
- `eccezioni_dominio_u14.py` - **prima eccezione di dominio** (OOP-03 J):
  `DisponibilitaInsufficiente` e la funzione pura `richiedi_unita`, con il
  chiamante che conserva il valore dopo il rifiuto.
- `intervalli_u14.py` - **l'intervallo semiaperto** (OOP-04 D):
  valore frozen con `durata_min` derivata e `sovrapposto_a` derivato per
  casi.
- `prenotazioni_u14.py` - **il registro delle prenotazioni** (OOP-04 E):
  `Prenotazione` frozen, `CodiceDuplicato`, `ConflittoPrenotazione` e
  `RegistroPrenotazioni` con registra, lotto, cerca, annulla, modifica,
  proiezioni e riepilogo.
- `csv_prenotazioni_u14.py` - **persistenza delle prenotazioni** (OOP-04
  G): schema dichiarato, conversioni con riferimenti di riga, importazione
  a lotto e esportazione con temporaneo.
- `cli_prenotazioni_u14.py` - **menu in memoria** (OOP-04 G): riepilogo,
  registrazione, annullamento, modifica, import/export CSV e uscita che
  non afferma di salvare; orari `HH:MM` con `24:00` solo come confine.
- `articolo_proprieta_u14.py` - **Articolo con proprietà e DatiArticolo**
  (OOP-03 K): osservazione di sola lettura, valore derivato e snapshot
  frozen; la validazione resta `valida_dati_articolo`.
- `magazzino_composto_u14.py` - **la raccolta composta** (OOP-04):
  `Magazzino` con unicità, inserimento che ricostruisce, proiezioni
  protette e modifica che conserva l'identità.
- `persistenza_magazzino_u14.py` - **raccordo CSV/JSON** con le politiche
  storiche U12/U13: `utf-8-sig` in ingresso, UTF-8 senza BOM in uscita,
  temporaneo e sostituzione finale, JSON `{"versione_schema": 1}`.
- `cli_magazzino_u14.py` - **stesso menu funzionale U12/U13** con la nuova
  delega al `Magazzino`.
- `controllore_simulato_u14.py` - **sensore, attuatore e controllore**
  (OOP-04 H): sequenza deterministica 18/20/22, esaurimento e lettura
  invalida senza aggiornamenti prematuri.

### `tests/`

Suite `pytest` che deriva gli attesi dai contratti pubblicati:
`PROP-`/`CLASSE-`/`METODI-`/`REPR-`/`EQ-`/`DATA-`/`ECC-` sugli esempi
concettuali, `PREN-01`…`PREN-14` sul registro e sulla persistenza, la
regressione funzionale del magazzino contro i valori storici U12/U13, il
controllore simulato e i casi discriminanti delle soluzioni formative.
`test_revisione_contratti_u14.py` aggiunge controlli su factory ore/minuti,
`str` conservato nella dataclass, valore `Soglia`, quoting CSV, indipendenza
degli inventari, ripristino del lotto e politiche di esposizione dei dati.
`test_volume_colori_palette_u14.py` verifica i nuovi contratti: confini,
booleani e tipi estranei, candidato completo, mutazione e alias,
uguaglianza su ogni componente, default, frozen e copie, ricerca in
posizione zero, volumi indipendenti e delega ai collaboratori.

### `dati/`

- `prenotazioni_canoniche.csv` - PR-01/PR-02/PR-04 della sequenza canonica;
- `prenotazioni_lotto_conflitto.csv` - lotto che fallisce dopo un primo
  candidato valido (fixture sintetica);
- `magazzino_canonico.csv` - i due articoli canonici 007/012.

### `soluzioni/`

- `esercizi_base_u14.py` - riferimenti eseguibili delle schede di base il
  cui prodotto è codice (E01-E06, T01-T08, X01-X04), con le varianti
  difettose marcate.
- `problemi_algoritmici_u14.py` - riferimenti eseguibili degli otto
  problemi T09-T14 e X05-X06.

### `laboratorio/`

Starter del **LAB-PY-U14**: contratti dichiarati, validatori e valori da
completare con `TODO`/`NotImplementedError` e tre test pubblici iniziali.
**Non** contiene il gestore risolto né una suite completata; i test dello
starter falliscono finché le fasi non sono svolte ed è il comportamento
atteso. Per questo non fanno parte di `testpaths`.

## Ambiente e comandi

CPython 3.14 sul computer, da questa directory.

```powershell
uv sync --group dev
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run python esempi/prenotazioni_u14.py
uv run python esempi/volume_audio_base_u14.py
uv run python esempi/volume_audio_u14.py
uv run python esempi/colori_espliciti_u14.py
uv run python esempi/colori_modello_dati_u14.py
uv run python esempi/palette_composizione_u14.py
uv run python esempi/cli_prenotazioni_u14.py
```

La suite non richiede modifiche a `sys.path`: `pyproject.toml` dichiara i
percorsi dei moduli per `pytest`. I moduli delle soluzioni dipendono dagli
esempi in `esempi/`: per eseguirli direttamente si dichiara la ricerca in
quel percorso nella sessione di shell, senza toccare i sorgenti.

```powershell
$env:PYTHONPATH = "esempi"
uv run python soluzioni/esercizi_base_u14.py
uv run python soluzioni/problemi_algoritmici_u14.py
```

Lo starter del laboratorio si esegue dalla sua directory, in un processo
separato:

```powershell
cd laboratorio
uv run pytest test_kit_starter.py -q   # fallisce finché le fasi non sono svolte
```

## Note di lettura

- Gli esempi concettuali non importano dalle applicazioni complete:
  ciascuno è eseguibile con le sole definizioni del proprio punto della
  lezione.
- Le varianti **deliberatamente difettose** sono marcate nel nome e nella
  docstring (`SchedaCondivisa`, `MisuraCheStampa`, `LimitiRicorsivo`,
  `AttivitaParziale`, `RegistroVisiteErrato`, `BigliettoPerCodice`,
  `PuntoSenzaControlli`): non fanno parte dei programmi validi.
- Il layout di questa unità segue il manifest del piano didattico U14
  (`tests/`, `soluzioni/`, `laboratorio/`), leggermente diverso da quello
  storico di `unita-13` (`test/`, `esercizi/`): la differenza è dichiarata
  qui per evitare ambiguità.
- La regressione del magazzino non importa i moduli U13: confronta le
  sequenze pubblicate in OOP-02 sez. J con i valori attesi storici, senza
  manipolare `sys.path` fra progetti diversi.
