# Raccolta progressiva di programmi — fotografia U3

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 3**: conserva i programmi U1-U2 e aggiunge il preventivo di
spedizione con la sua documentazione. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso: una possibile realizzazione completa, non la cronologia
che ogni studente deve costruire con i propri commit.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-02/`](../unita-02/) e [`../unita-04/`](../unita-04/).

## Traguardi della tappa

- regole verbali del listino tradotte in selezioni con `if` / `elif` / `else`;
- validazione dei valori dopo la conversione, con priorità peso →
  destinazione → urgenza e un solo messaggio di errore;
- prove sui confini delle fasce e sulle combinazioni dei supplementi;
- limite di conversione documentato senza `try/except`.

## Struttura

```text
unita-03/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
├── programmi/
│   ├── 01_hello.py
│   ├── 02_benvenuto.py
│   ├── 03_messaggio_multiriga.py
│   ├── trasferimento_dati.py
│   └── preventivo_spedizione.py
└── documentazione/
    ├── unita-01/flusso-sorgente-processo.md
    ├── unita-02/{specifica.md, casi-di-prova.md}
    └── unita-03/{specifica.md, casi-di-prova.md}
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen          # ricostruisce .venv/ dal lock
uv run python --version   # Python 3.14.7
uv run python programmi/preventivo_spedizione.py
```

I programmi delle tappe precedenti si eseguono come documentato nei README di
[`unita-01`](../unita-01/README.md) e [`unita-02`](../unita-02/README.md),
con gli stessi output.

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e uv 0.12.15. Caso P11
(con entrambi i supplementi):

```text
> uv run python programmi/preventivo_spedizione.py
Peso del kit in grammi interi (da 1 a 10000): 500
Destinazione (locale o nazionale): nazionale
Urgenza (s o n): s
Peso: 500 g
Destinazione: nazionale
Urgenza: s
Costo base: 3.00 euro
Supplemento destinazione: 4.00 euro
Supplemento urgenza: 2.00 euro
Totale: 9.00 euro
```

Caso P17 (più valori errati: prevale il primo secondo la priorità):

```text
> uv run python programmi/preventivo_spedizione.py
Peso del kit in grammi interi (da 1 a 10000): 0
Destinazione (locale o nazionale): estero
Urgenza (s o n): forse
Peso non ammesso
```

Caso P19 (limite di conversione):

```text
> uv run python programmi/preventivo_spedizione.py
Peso del kit in grammi interi (da 1 a 10000): mezzo chilo
Destinazione (locale o nazionale): locale
Urgenza (s o n): n
Traceback (most recent call last):
  ...
  File "programmi/preventivo_spedizione.py", line 15, in <module>
    peso_g = int(peso_testo)
ValueError: invalid literal for int() with base 10: 'mezzo chilo'
```

La tabella completa dei diciannove casi pubblici e delle quattro prove
aggiuntive è in
[`documentazione/unita-03/casi-di-prova.md`](documentazione/unita-03/casi-di-prova.md),
compresa la prova di regressione E4 eseguita su una copia temporanea.

## Differenze rispetto alla tappa precedente

- nuovo file `programmi/preventivo_spedizione.py`: primo programma con
  selezioni multiple, validazione con priorità e composizione del prezzo;
- nuova `documentazione/unita-03/` con `specifica.md` e `casi-di-prova.md`;
- i programmi U1-U2, l'ambiente e le documentazioni precedenti sono invariati.

## Limiti del riferimento

- I messaggi di errore sono le tre etichette brevi della specifica
  (`Peso non ammesso`, `Destinazione non ammessa`, `Urgenza non ammessa`):
  sono anche gli esiti del validatore che la tappa U5 riutilizzerà, così i due
  programmi condividono lo stesso contratto di messaggi.
- Non è presente `documentazione/unita-03/riflessione.md`: è la riflessione
  personale dello studente e non viene sostituita da un testo fittizio.
- Nessuna cronologia Git è inclusa: i tre commit della tappa sono lavoro dello
  studente. Il sorgente non usa funzioni, cicli, `try/except` né
  normalizzazione dei testi, come previsto dalla consegna U3.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| Casi P01-P11 | Esecuzione con gli input della tabella | Quattro righe di prezzo corrette, due decimali |
| Confini delle fasce | P02/P03, P04/P05, P06/P07 | La soglia appartiene alla fascia inferiore |
| Combinazioni dei supplementi | P08-P11 | Supplementi indipendenti e sommati |
| Casi P12-P18 | Esecuzione con valori non ammessi | Un solo messaggio, nella priorità peso → destinazione → urgenza |
| Caso P19 | Esecuzione con testo non numerico | `ValueError` in conversione, senza recupero |
| Prove aggiuntive E1-E4 | Esecuzione e regressione su copia | Atteso e osservato coincidono; la soglia modificata è rilevata |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 3 — Preventivo di spedizione di kit didattici*.
- Teoria di riferimento: cap. PY-04 — *Logica e selezione*.
- Guide operative: *Guida al debugger* (sezione sui rami) e guida a Ruff nelle
  guide `dev-tools` del sito.
