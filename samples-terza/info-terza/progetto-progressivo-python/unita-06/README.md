# Raccolta progressiva di programmi — fotografia U6

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 6**: conserva i programmi U1-U5 e aggiunge il totale ricorsivo dei
preventivi con la sua suite. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-05/`](../unita-05/) e [`../unita-07/`](../unita-07/).

## Traguardi della tappa

- seconda implementazione del totale dei preventivi, ricorsiva e confrontabile
  con quella iterativa;
- distinzione fra `quanti` come quantità e l'indice dell'ultimo elemento;
- base, riduzione e ricomposizione dichiarate; lista invariata;
- raccordo con il riepilogo U5 con la conversione euro → centesimi eseguita
  una sola volta.

## Struttura

```text
unita-06/
├── programmi/
│   ├── ... programmi U1-U5 invariati ...
│   ├── spedizione_u5.py            # acquisisce totale_preventivi_ric
│   ├── test_spedizione_u5.py       # suite U5 invariata
│   └── test_totale_ricorsivo_u6.py # suite della tappa
├── documentazione/
│   ├── unita-01/ ... unita-05/ (documenti invariati)
│   └── unita-06/progetto/contratti.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen        # ricostruisce .venv/ dal lock
uv run pytest -q        # suite cumulativa U5+U6
```

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e pytest 9.1.1:

```text
> uv run pytest -q
..........................................                               [100%]
42 passed in 0.06s
```

La suite cumulativa scopre **42 test**: 30 della tappa U5, invariati, e 12
della tappa U6 — sette casi pubblici PR01-PR07, tre casi discriminanti su
ultimo elemento e duplicati, due test di raccordo con U5. Il confronto fra le
due implementazioni del totale è nel test `test_raccordo_u5_u6_conversione_unica`:
`totale_preventivi_ric([300, 900, 500], 3)` vale 1700 centesimi e il riepilogo
U5 di `[3, 9, 5]` euro vale `(3, 17)`, con `1700 == 17 * 100`.

## Differenze rispetto alla tappa precedente

- `programmi/spedizione_u5.py` acquisisce la sezione «Totale ricorsivo» con
  `totale_preventivi_ric`; il resto del modulo, la CLI e la tariffa sono
  invariati;
- nuovo `programmi/test_totale_ricorsivo_u6.py` con 12 test;
- nuova `documentazione/unita-06/progetto/contratti.md` con decomposizione,
  traccia dei frame e regole del confronto fra euro e centesimi.

Le nuove funzioni delle tappe successive entrano nel modulo unico della
raccolta: la suddivisione in moduli per responsabilità è prevista per la tappa
U12 e non viene anticipata.

## Limiti del riferimento

- La funzione assume la precondizione `0 <= quanti <= len(importi_cent)` e non
  valida: la gestione delle eccezioni non è richiesta in questa tappa.
- La profondità massima delle prove pubbliche è di 100 elementi: non serve
  modificare il limite di ricorsione di CPython.
- Nessun file `riflessione.md`: è il documento personale dello studente.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| PR01-PR07 | `uv run pytest -q programmi/test_totale_ricorsivo_u6.py` | Somme esatte e liste invariate |
| Ultimo elemento | casi discriminanti su prefisso n-1 e n | L'ultimo importo è escluso o incluso secondo `quanti` |
| Duplicati e zeri | casi discriminanti su importi ripetuti e zeri | Ogni occorrenza conta, lo zero è un importo valido |
| Raccordo U5-U6 | `test_raccordo_u5_u6_conversione_unica` | 1700 centesimi = 17 euro × 100, conversione una sola volta |
| Regressione U5 | `uv run pytest -q` | 30 test U5 ancora superati |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 6 — Un secondo totale per il confronto*.
- Teoria di riferimento: cap. PY-10 — *Ricorsione*; cap. PY-09 per la pratica
  di test.
