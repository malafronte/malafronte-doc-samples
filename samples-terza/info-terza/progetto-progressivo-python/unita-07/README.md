# Raccolta progressiva di programmi — fotografia U7

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 7**: conserva i programmi U1-U6 e aggiunge le coppie
`(destinazione, totale_cent)` con le funzioni di sintesi. È il riferimento di
confronto della [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-06/`](../unita-06/) e [`../unita-08/`](../unita-08/).

## Traguardi della tappa

- nuova rappresentazione a lista di tuple con destinazione normalizzata e
  totale in centesimi;
- `normalizza_destinazione`, `preventivi_sopra_media` e `matrice_riepilogo`
  con effetti e casi vuoti dichiarati;
- preparazione dei dati dalle spedizioni, con conversione euro → centesimi
  eseguita una sola volta;
- raccordo con le rappresentazioni U5 e U6 verificato dai test.

## Struttura

```text
unita-07/
├── programmi/
│   ├── ... programmi U1-U6 invariati ...
│   ├── spedizione_u5.py            # acquisisce la sezione U7
│   ├── test_spedizione_u5.py       # suite U5 invariata
│   ├── test_totale_ricorsivo_u6.py # suite U6 invariata
│   └── test_sintesi_u7.py          # suite della tappa
├── documentazione/
│   ├── unita-01/ ... unita-06/ (documenti invariati)
│   └── unita-07/progetto/contratti.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen        # ricostruisce .venv/ dal lock
uv run pytest -q        # suite cumulativa U5+U6+U7
```

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e pytest 9.1.1:

```text
> uv run --frozen pytest -q
.........................................................                [100%]
57 passed in 0.08s
```

La suite cumulativa scopre **57 test**: 30 U5, 12 U6 e 15 U7 — i casi
PU01-PU09, tre casi propri e tre regressioni sul confronto esatto fra interi.
Il raccordo canonico della tappa è verificato
da `test_pu02_preparazione_e_analisi_del_canonico` e
`test_pu07_raccordo_u5_u6_u7`: importi U5 `[3, 9, 5]`, coppie U7
`[("locale", 300), ("nazionale", 900), ("locale", 500)]`, sopra-media
`[("nazionale", 900)]`, riepilogo `([2, 1], [800, 900])` e totale U6 pari a
1700 centesimi, uguale a `17 * 100`.

## Differenze rispetto alla tappa precedente

- `programmi/spedizione_u5.py` acquisisce la sezione «Coppie e tabelle di
  sintesi»: `normalizza_destinazione`, `prepara_coppie`,
  `preventivi_sopra_media` e `matrice_riepilogo`;
- nuovo `programmi/test_sintesi_u7.py` con 15 test, di cui due di raccordo;
- nuova `documentazione/unita-07/progetto/contratti.md` con la mappa delle
  rappresentazioni e le regole sulle unità.

La CLI U5 resta senza normalizzazione implicita: la normalizzazione appartiene
alla preparazione U7 e non modifica il contratto della CLI.

## Limiti del riferimento

- Le funzioni di analisi ricevono coppie già normalizzate: i valori fuori
  precondizione si identificano come tali e non sono gestiti. Il rifiuto di
  `estero` si verifica con `errore_dati_spedizione`, come nel test PU09.
- Nessuna promessa di identità per le stringhe normalizzate o per le tuple
  immutabili condivise: il contratto promette liste nuove per i risultati.
- Nessun file `riflessione.md`: è il documento personale dello studente.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU01-PU06 | `uv run pytest -q programmi/test_sintesi_u7.py` | Analisi esatte su vuoto, media, duplicati e alias |
| PU07 raccordo | stesso comando | 1700 centesimi = 17 euro × 100, conversione una sola volta |
| PU08 normalizzazione | stesso comando | `" nazionale "` e `"NAZIONALE"` → `"nazionale"`, originali conservati |
| PU09 regressione | `uv run pytest -q` | 57 test complessivi superati, `estero` rifiutato dal validatore |
| Casi propri PR-1, PR-2, PR-3 | stesso comando | Indipendenza dei risultati, duplicati, conversione singola |
| Regressioni del sopra-media | `uv run pytest -q programmi/test_sintesi_u7.py` | Confronto esatto con totali grandi, duplicati e scarti di un centesimo |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 7 — Tabelle di sintesi dei preventivi*.
- Teoria di riferimento: cap. PY-11 — *Stringhe, liste e tuple*; cap. PY-09
  per la pratica di test.
