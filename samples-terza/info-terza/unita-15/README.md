# Unità 15 — Componenti intercambiabili

Riferimenti didattici CPython 3.14 per OOP-05, OOP-06, OOP-07.
Sono distinti dal progetto autonomo dei preventivi: nessuna soluzione di M55–M57.

## Ambiente ed esecuzione

Dalla cartella `unita-15`, con uv già installato:

```powershell
uv sync --locked
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run python esempi/client_orologi_u15.py
uv run python esempi/mro_cooperativa_u15.py
uv run python esempi/cli_rapporto_u15.py
```

Gli import fra esempi sono fra moduli nella stessa directory; pytest dichiara i percorsi
nel manifest, senza alterazioni di `sys.path`. I file non aprono interazioni all'import.

## Manifest dei ruoli

| File/cartella | Ruolo e pagina |
|---|---|
| `esempi/orologi_base_u15.py`, `orologi_derivati_u15.py`, `client_orologi_u15.py` | OOP-05 A–D, F–H: stato, specializzazioni, client |
| `esempi/mro_cooperativa_u15.py`, `factory_ereditata_u15.py` | OOP-05 E: esempi autonomi |
| `esempi/politiche_duck_u15.py`, `politiche_abc_u15.py`, `politiche_protocol_u15.py` | OOP-06 A–G: tre organizzazioni dello stesso contratto |
| `esempi/soglia_algoritmi_u15.py` | OOP-06 H: scansione e confine dicotomico |
| `esempi/rilevazioni_u15.py`, `contratti_esportazione_u15.py` | OOP-07 A–C: modello e interfaccia |
| `esempi/esportatori_u15.py`, `servizio_rapporto_u15.py`, `cli_rapporto_u15.py` | OOP-07 C–E: salvataggio e punto di avvio |
| `esempi/controllore_adattatori_u15.py` | OOP-07 H, ESP-07: sola simulazione CPython |
| `tests/` | Contratti, round-trip, guasti deterministici; simulazioni, non prove hardware |
| `soluzioni/` | Soluzioni formative delle due raccolte U15 |
| `dati/` | Fixture sintetiche; `007` identifica una fonte, duplicati ammessi |
| `diagrammi/` | Sorgenti UML modificabili |
| `laboratorio/starter/` | Lavoro incompleto deliberato; separato dai riferimenti e dalla suite |
| `esp32/README.md` | Confine hardware e informazioni ancora necessarie |

La scrittura preserva il file precedente se fallisce prima della sostituzione riuscita.
Non promette durabilità contro perdita di alimentazione né sincronizzazione fra processi.
Le directory mancanti causano OSError; non sono create implicitamente.

## Dataset e casi invalidi

`dati/rilevazioni.csv` e `dati/rilevazioni.json` contengono lo stesso dataset
sintetico di OOP-07 A: quattro letture, ordine e duplicati conservati. I parser
sono spiegati in OOP-07 D. `dati/casi-invalidi/valore-testuale.csv` produce
ValueError nella conversione numerica; `valore-booleano.json` produce ValueError
nella validazione del modello, perché il bool è escluso dal dominio.

## Starter e diagnostica

`uv run pytest laboratorio/starter/tests -q` esegue lo starter **incompleto**:
esito iniziale previsto 1 passato, 3 fallimenti con NotImplementedError.
La suite ordinaria raccoglie solo `tests/`; le prove dello starter si avviano
separatamente, dopo ciascuna fase descritta nel suo README.

`diagnostica/contrasto_protocol.py` dimostra intenzionalmente una firma
incompatibile. Va aperto con Pylance basic nell'editor per confrontare controllo
statico ed esecuzione; non è un programma di riferimento corretto. La diagnostica
autoriale ty è documentata nel capitolo, senza attribuirla a Pylance.
`verifiche/estrai_blocchi.py` prepara prove autoriali dalle fence delle pagine:
richiede pagine e directory nuova di uscita come argomenti e non modifica i sorgenti.
