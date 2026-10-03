# Riferimento formativo del LAB-PY-U12 — archivio materiali di laboratorio

Questa cartella contiene la **controparte completa** dello starter del LAB-PY-U12: gli stessi quattro moduli con i corpi implementati e la stessa suite dei casi pubblici L01-L12. Si legge **dopo** il tentativo personale, come confronto formativo: il valore del lavoro sta nel contratto rispettato e nei controlli eseguiti, non nella copia del corpo.

## I file del riferimento

| File | Contenuto |
|---|---|
| `dominio_archivio_u12.py` | validazione di schema, tipi e domini; conversione riga/record; ricerca per indice, inserimento, aggiornamento ed eliminazione; `riepilogo_archivio` |
| `persistenza_archivio_u12.py` | `carica_materiali` con politica tutto-o-niente e `salva_materiali` con il protocollo del temporaneo |
| `cli_archivio_u12.py` | menu `match/case`, flag delle modifiche, conferma `s/n`, EOF in ogni domanda e codici di uscita 0/1/2 |
| `test_archivio_u12.py` | suite identica a quella dello starter: con il riferimento supera tutti i casi |

Il testo dei docstring, le firme e i contratti coincidono con quelli dello starter: le sole differenze sono i corpi e la dimostrazione sotto guardia di `dominio_archivio_u12.py` e `persistenza_archivio_u12.py`.

## Comandi verificati

Esecuzione dalla root di questa cartella, con l'interprete del corso:

```powershell
uv run --python 3.14 python --version
uv run --python 3.14 --with pytest python -m pytest test_archivio_u12.py -q
uv run --python 3.14 python dominio_archivio_u12.py
uv run --python 3.14 python persistenza_archivio_u12.py ..\starter-laboratorio\dati-ingresso\archivio_materiali.csv
```

Versioni della verifica: CPython 3.14.7, `uv` 0.12.15, pytest 9.1.1. Esito della suite: **53 superati**, compresi 18 casi di EOF nei campi e nelle conferme, con e senza modifiche pendenti. La dimostrazione di `persistenza_archivio_u12.py` riscrive l'archivio in una copia `.copia.csv`, confronta i byte con l'originale e la rimuove: la fixture d'ingresso non viene modificata. Le fixture di `dati-ingresso/` sono quelle dello starter - una sola fonte, come per la suite - e si leggono dalla cartella di origine senza copiarle nel riferimento.

## Cosa il riferimento mostra rispetto allo starter

| Tema | Scelta del riferimento |
|---|---|
| Validazione | un solo controllo per campo, `bool` escluso dagli interi, messaggi che nominano campo e valore |
| Conversione | numero di campi, conversione di `quantita` e validazione del record sono **controlli separati**, ciascuno con la propria diagnosi e il riferimento della riga |
| Ricerca | l'indice 0 è un risultato come gli altri: la funzione restituisce `None` per gli assenti e i chiamanti confrontano esplicitamente con `None` |
| Aggiornamento | il candidato si costruisce e si valida per intero prima di sostituire il record trovato: nessun aggiornamento parziale |
| Caricamento | lista temporanea, `utf-8-sig` che accetta il BOM d'ingresso, `newline=""`, `strict=True`, righe fisiche vuote ignorate e distinte dai record con campi vuoti, unicità dei codici |
| Salvataggio | validazione integrale, `tempfile.NamedTemporaryFile` con `delete=False` nella stessa directory, scrittura con `lineterminator="\n"`, chiusura, `Path.replace`, pulizia del temporaneo con `add_note` sul residuo senza mascherare l'errore primario |
| CLI | `match/case` sulle scelte, flag aggiornato solo su mutazione riuscita e azzerato solo su salvataggio riuscito, uscita `0` con salvataggio condizionato, EOF dichiarato in qualunque domanda senza scrittura implicita |
| Guasti simulati | i test intercettano la scrittura del temporaneo e `Path.replace`: la destinazione resta invariata e nessun messaggio di successo precede la sostituzione |

## Limiti dichiarati

Il protocollo del temporaneo protegge dai guasti di scrittura di un singolo processo: non è una transazione e non protegge da interruzioni elettriche, errori hardware o scritture concorrenti. La CLI gestisce un solo operatore alla volta e non usa blocchi di file: la modifica puntuale di un record binario appartiene al [cap. PY-21](/info-terza/corso/python/moduli-persistenza-errori/21-file-binari-accesso-posizione/). Nessun contenuto di questo riferimento è richiesto per completare il progetto autonomo dell'Unità 12, che ha requisiti e regime propri.
