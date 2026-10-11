# Riproducibilità (U12)

Comandi, ambiente e verifiche per ripetere il lavoro di questa tappa su un
altra postazione a partire dai soli materiali pubblici.

## Ambiente ricostruito

| Elemento | Valore verificato |
|---|---|
| Interprete | CPython 3.14.7, dichiarato da `.python-version` e da `requires-python = ">=3.14"` |
| Strumento | uv 0.12.15 |
| Dipendenze | `matplotlib` (grafici U9 e U11) e `pytest` (suite), fissate in `uv.lock` |
| Sistema | Windows 11, esecuzione normale fuori dal debugger |

Dalla root della cartella:

```powershell
uv sync --frozen     # ricostruisce .venv/ dal lock, senza modifiche
uv run pytest -q     # intera suite cumulativa U5-U12
```

`uv sync --frozen` fallisce se il lock non è coerente con `pyproject.toml`: è
il controllo che rende la ricostruzione verificabile e non dipendente dalla
`.venv` dell'autore. Nessun passaggio richiede installazioni globali.

## Comandi della tappa

```powershell
uv run python programmi/registro_cli.py               # sessione sul registro
uv run pytest -q programmi/test_persistenza_u12.py    # solo i test U12
```

La sessione CLI si avvia dalla root della cartella: i percorsi predefiniti —
`dati/unita-12/archivio.json` per l'archivio di lavoro e
`dati/unita-12/esportazione.csv` per l'esportazione — sono relativi a essa.
Per partire dai dati canonici:

```powershell
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/registro_cli.py
```

## Riavvii verificati

| Scenario | Procedura | Esito osservato |
|---|---|---|
| Modifica e salvataggio riusciti | `inserisci`, `salva`, `esci`, poi nuovo avvio e `carica` | record ricostruiti equivalenti: codici, interi, destinazioni, ordine |
| Salvataggio fallito | `inserisci` poi guasto di sostituzione, nuovo avvio e `carica` | l'archivio mostra l'ultimo salvataggio valido; le modifiche perse erano solo in memoria |
| Archivio vuoto | `carica` su `archivio_vuoto.json` | registro vuoto valido, distinto da file assente e da file corrotto |
| Documento corrotto | `carica` su `archivio_sintassi_corrotta.json` | diagnosi di sintassi con riga e colonna, nessun dato caricato |

I due primi scenari sono automatizzati da `test_pu12_09` e `test_pu12_08`; gli
altri da `test_pu12_01`. La sessione CLI reale è documentata nel README della
fotografia.

## Moduli e dipendenze

`registro_cli.py` dipende da `registro_persistenza.py` e da
`registro_dominio.py`; `registro_dominio.py` riunisce la logica già verificata
delle tappe U6-U11 dal modulo storico `spedizione_u5.py`, che resta la CLI
tariffaria U5 con le proprie garanzie. Nessun import ciclico e nessun effetto
all'import: tutti i moduli si possono importare senza domande, stampe né
scritture.

## Limiti

- Un errore di lettura diverso dall'assenza del file non viene classificato e
  si propaga come errore del sistema operativo.
- Il CSV di consultazione non è reversibile verso il documento canonico: non
  contiene `versione_schema`.
- La concorrenza — più processi sullo stesso archivio — non è gestita e non fa
  parte della consegna.
- I tempi delle misure U9 e U11 appartengono alle postazioni che li hanno
  prodotti: qui conta la riproducibilità della procedura, non dei valori.
