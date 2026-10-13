# Raccolta progressiva di programmi - fotografia U19

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 19**: conserva i programmi U1-U18 e aggiunge il **dossier di
scelta degli indici del registro** - adattatore B-tree di riferimento a
chiavi stringa con grado minimo 2, consultazione con conteggi, viste
ordinate e intervalli, confronto verificato delle consultazioni con rapporto
riproducibile e scelta motivata - oltre alla documentazione dei contratti e
del carico e al diagramma aggiornato. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-18/`](../unita-18/).

## Traguardi della tappa

- **indice B-tree per codice** `IndiceBTreeU19`: il B-tree del capitolo
  PY-35 è riprodotto nel progetto e adattato a **chiavi stringa** con grado
  minimo 2, con i codici `007`, `012` e `003` conservati come stringhe;
- **validazione riusata** dal modello del registro: `valida_chiave`
  richiama `valida_dominio_record` sul campo `codice`, senza duplicare regole
  né diagnosi;
- **ricerca esatta, viste ordinate e intervalli**: `cerca` restituisce il
  record del codice, `fotografia_ordinata` le coppie in ordine lessicografico,
  `intervallo` le coppie fra gli estremi; la ricerca strumentata documenta
  percorso, nodi e confronti;
- **costruzione dopo il caricamento**: l'indice è costruito sulla proiezione
  pubblica `preventivi()` del registro e risponde a più interrogazioni sulla
  stessa fotografia;
- **punto di avvio di confronto** `confronto_cli_u19.py` separato dalle
  strutture, che costruisce scansione, lista ordinata, BST, hash e B-tree
  sulla stessa fotografia, verifica l'equivalenza e salva il CSV;
- **costi separati**: `ricerca_con_conteggi` conta nodi e confronti con la
  regola dichiarata, e la suite PU19-09 confronta preparazione e
  interrogazioni;
- **prove** dei casi PU19-01-PU19-10 più tre casi propri motivati, con
  regressione U5-U18 verificata dalla suite cumulativa.

## Struttura

```text
unita-19/
├── programmi/
│   ├── ... programmi U1-U18 invariati ...
│   ├── indice_btree_u19.py       # B-tree e indice per codice
│   ├── confronto_cli_u19.py      # punto di avvio: confronta dopo il caricamento
│   ├── test_indice_btree_u19.py  # suite della tappa (13 test)
├── dati/unita-12/ (fixture invariate, dataset 007/012/003)
├── risultati/unita-19/ (CSV del confronto verificato)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-18/ (documenti invariati)
│   ├── unita-19/
│       ├── contratti-e-carico.md  # contratto, varianti e carico
│       ├── prove-e-scelta.md      # casi, difetti plausibili, scelta
│       ├── diagramma.puml         # UML aggiornato con l'indice
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync                                         # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U19
uv run pytest -q programmi/test_indice_btree_u19.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/confronto_cli_u19.py fotografia cerca 007 cerca 999 confronta
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run pytest -q
230 passed in 0.53s
```

**230 test**: 217 delle tappe U5–U18 più 13 della tappa U19 — i casi
PU19-01–PU19-10, i tre casi propri motivati e i controlli sugli invarianti
dell'indice. La sola suite della tappa riporta 13 test superati. Le
interrogazioni reali con il dataset pubblicato, sulla stessa fotografia:

```text
> uv run python programmi/confronto_cli_u19.py fotografia cerca 007 cerca 999 statistiche
fotografia caricata: 3 preventivi, indici costruiti: 5 strutture
fotografia -> [003/locale/1200, 007/locale/450, 012/nazionale/0]
lista-ordinata -> 007/locale/450
scansione -> 007/locale/450
bst -> 007/locale/450
hash -> 007/locale/450
b-tree -> 007/locale/450
lista-ordinata -> assente
scansione -> assente
bst -> assente
hash -> assente
b-tree -> assente
statistiche -> codici 3, altezza 0
interrogazioni eseguite: 4
```

## Differenze rispetto alla fotografia U18

I file U1-U18 restano invariati; la tappa U19 aggiunge i due moduli
dell'indice e del confronto, il punto di avvio, la suite e i tre documenti
di `documentazione/unita-19/`. La regressione verificata riguarda i contratti
mantenuti: modello U14, persistenza U12, tariffe U3/U5, ordine della raccolta,
coda U16, indice BST U17 e indice hash U18 non cambiano firma né
comportamento, e la suite U5-U18 supera per intero. I limiti dichiarati:
ogni indice rappresenta la fotografia del momento della costruzione e ogni
modifica del registro richiede una nuova costruzione; il B-tree del capitolo
PY-35 è riprodotto nel progetto con chiavi stringa per mantenere la
fotografia autonoma; le cancellazioni dinamiche del B-tree nel dossier sono
simulazioni o ricostruzioni, e i trasferimenti di blocchi sono conteggi del
modello dichiarato.
