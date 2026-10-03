# Raccolta progressiva di programmi — fotografia U2

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 2**: conserva i programmi U1 e aggiunge il calcolatore del tempo di
trasferimento con la sua documentazione. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso: mostra una possibile realizzazione completa, non la
cronologia che ogni studente deve costruire con i propri commit.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. La fotografia precedente è in
[`../unita-01/`](../unita-01/), quella successiva in [`../unita-03/`](../unita-03/).

## Traguardi della tappa

- programma sequenziale con acquisizione, conversioni motivate, calcolo e
  presentazione separati;
- formule del modello a velocità costante applicate senza arrotondamenti
  intermedi, con due cifre decimali soltanto nella stampa;
- casi P1-P9 verificati con esecuzioni reali e due casi validi aggiuntivi
  motivati;
- limiti dichiarati: casi di conversione fallita e dato fuori dominio non
  intercettati, come previsto dalla consegna U2.

## Struttura

```text
unita-02/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
├── programmi/
│   ├── 01_hello.py
│   ├── 02_benvenuto.py
│   ├── 03_messaggio_multiriga.py
│   └── trasferimento_dati.py
└── documentazione/
    ├── unita-01/
    │   └── flusso-sorgente-processo.md
    └── unita-02/
        ├── specifica.md
        └── casi-di-prova.md
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen          # ricostruisce .venv/ dal lock
uv run python --version   # Python 3.14.7
uv run python programmi/01_hello.py
uv run python programmi/02_benvenuto.py
uv run python programmi/03_messaggio_multiriga.py
uv run python programmi/trasferimento_dati.py
```

I programmi U1 si eseguono con gli output documentati nel
[`README di U1`](../unita-01/README.md). Il nuovo programma legge tre righe di
input: nelle sessioni seguenti i valori digitati compaiono dopo il prompt,
uno per riga.

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e uv 0.12.15. Caso P1:

```text
> uv run python programmi/trasferimento_dati.py
Dimensione in MB interi, zero ammesso: 150
Velocità in MB/s, punto decimale, minimo 0.01: 2.5
Preparazione in secondi interi, zero ammesso: 10
Dimensione: 150 MB
Velocità: 2.5 MB/s
Preparazione: 10 secondi
Tempo di trasferimento: 60.00 secondi
Tempo totale: 70.00 secondi
Tempo totale: 1.17 minuti
```

Caso P4, dove l'arrotondamento avviene solo nella stampa:

```text
> uv run python programmi/trasferimento_dati.py
Dimensione in MB interi, zero ammesso: 1
Velocità in MB/s, punto decimale, minimo 0.01: 3
Preparazione in secondi interi, zero ammesso: 0
Dimensione: 1 MB
Velocità: 3.0 MB/s
Preparazione: 0 secondi
Tempo di trasferimento: 0.33 secondi
Tempo totale: 0.33 secondi
Tempo totale: 0.01 minuti
```

Caso P6, limite di divisione per zero:

```text
> uv run python programmi/trasferimento_dati.py
Dimensione in MB interi, zero ammesso: 150
Velocità in MB/s, punto decimale, minimo 0.01: 0
Preparazione in secondi interi, zero ammesso: 10
Traceback (most recent call last):
  ...
  File "programmi/trasferimento_dati.py", line 23, in <module>
    trasferimento_s = dimensione_mb / velocita_mb_s
ZeroDivisionError: division by zero
```

La tabella completa di atteso e osservato per tutti gli undici casi è in
[`documentazione/unita-02/casi-di-prova.md`](documentazione/unita-02/casi-di-prova.md).

## Differenze rispetto alla tappa precedente

- nuovo file `programmi/trasferimento_dati.py`: primo programma con `input`,
  conversioni `int` e `float` e f-string con specificatore `:.2f`;
- nuova `documentazione/unita-02/` con `specifica.md` e `casi-di-prova.md`;
- i programmi U1, l'ambiente e la documentazione U1 sono invariati.

## Limiti del riferimento

- Il programma non verifica i domini e non recupera dalle conversioni
  fallite: `if` e `try/except` sono costrutti delle tappe successive. I casi
  P6-P9 documentano questi limiti, come richiede la consegna U2.
- Non è presente `documentazione/unita-02/riflessione.md`: quel documento è la
  riflessione personale dello studente su una previsione smentita e non viene
  sostituita da un testo fittizio del riferimento.
- Nessuna cronologia Git è inclusa: i tre commit della tappa U2 sono lavoro
  dello studente.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| Casi P1-P5 | Esecuzione con gli input della tabella | I tre risultati coincidono con l'atteso, due cifre decimali |
| Casi P6-P8 | Esecuzione con input non conformi | `ZeroDivisionError` o `ValueError` nelle righe indicate |
| Caso P9 | Esecuzione con dimensione negativa | Risultati negativi stampati senza diagnosi |
| Due casi aggiuntivi | Esecuzione con E1 e E2 | Atteso e osservato coincidono |
| Nessun arrotondamento intermedio | Confronto del caso P4 | `0.33` e `0.01` derivano dai valori non formattati |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 2 — Calcolatore del tempo di trasferimento*.
- Teoria di riferimento: cap. PY-02 — *Valori, tipi, nomi ed espressioni* e
  cap. PY-03 — *Input, output e validazione*.
- Guida operativa: *Guida al debugger* nelle guide `dev-tools` del sito.
