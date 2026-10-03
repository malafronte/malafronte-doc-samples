# Raccolta progressiva di programmi — fotografia U4

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 4**: conserva i programmi U1-U3 e aggiunge il gioco a tentativi con
la sua documentazione. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso: una possibile realizzazione completa, non la cronologia
che ogni studente deve costruire con i propri commit.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-03/`](../unita-03/) e [`../unita-05/`](../unita-05/).

## Traguardi della tappa

- ciclo `while` con stato esplicito: due contatori con significati diversi;
- tre esiti finali distinti — vittoria, annullamento, richieste esaurite — con
  un solo esito stampato;
- gestione dei rifiuti e dell'annullamento secondo il contratto: 0 non consuma
  richieste, ogni altra risposta sì;
- segreto, dominio e limite definiti una volta sola e usati in messaggi e
  condizioni.

## Struttura

```text
unita-04/
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
│   ├── preventivo_spedizione.py
│   └── indovina_numero.py
└── documentazione/
    ├── unita-01/flusso-sorgente-processo.md
    ├── unita-02/{specifica.md, casi-di-prova.md}
    ├── unita-03/{specifica.md, casi-di-prova.md}
    └── unita-04/progetto/{specifica.md, casi-di-prova.md, traccia.md}
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen          # ricostruisce .venv/ dal lock
uv run python --version   # Python 3.14.7
uv run python programmi/indovina_numero.py
```

I programmi delle tappe precedenti si eseguono come documentato nei README di
[`unita-01`](../unita-01/README.md), [`unita-02`](../unita-02/README.md) e
[`unita-03`](../unita-03/README.md), con gli stessi output.

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e uv 0.12.15. Caso P04
(vittoria sull'ultima richiesta):

```text
> uv run python programmi/indovina_numero.py
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 1
Il numero da trovare è maggiore.
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 2
Il numero da trovare è maggiore.
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 3
Il numero da trovare è maggiore.
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 7
Vittoria: il numero da trovare è stato indovinato.
Richieste usate: 4
Tentativi validi: 4
```

Caso P06 (i rifiuti consumano il limite):

```text
> uv run python programmi/indovina_numero.py
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: -1
Valore fuori intervallo.
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 21
Valore fuori intervallo.
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 1
Il numero da trovare è maggiore.
Numero da 1 a 20 (massimo 4 richieste), 0 per annullare: 7
Vittoria: il numero da trovare è stato indovinato.
Richieste usate: 4
Tentativi validi: 2
```

Le tabelle complete — quindici casi pubblici, tre casi motivati, prove del
numero di letture e variante del limite — sono in
[`documentazione/unita-04/progetto/casi-di-prova.md`](documentazione/unita-04/progetto/casi-di-prova.md);
la traccia del caso P04 è in
[`documentazione/unita-04/progetto/traccia.md`](documentazione/unita-04/progetto/traccia.md).

## Differenze rispetto alla tappa precedente

- nuovo file `programmi/indovina_numero.py`: primo programma con ciclo,
  stato accumulato e interruzione con `break`;
- nuova `documentazione/unita-04/progetto/` con `specifica.md`,
  `casi-di-prova.md` e `traccia.md`;
- i programmi U1-U3, l'ambiente e le documentazioni precedenti sono invariati.

## Limiti del riferimento

- Il segreto è assegnato nel sorgente di proposito: le prove sono
  riproducibili e non serve la casualità. La variante con segreto 1 e 20 è
  stata verificata su copie temporanee, senza modificare il riferimento.
- Non è presente `documentazione/unita-04/progetto/riflessione.md`: è la
  riflessione personale dello studente e non viene sostituita da un testo
  fittizio. Nessuna cronologia Git è inclusa: i tre commit della tappa sono
  lavoro dello studente.
- Il testo non convertibile (`sette`) produce `ValueError` senza recupero: è
  il limite di conversione dichiarato dalla consegna U4.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| Casi P01-P12 | Sequenze della tabella | Esito, suggerimenti e contatori corrispondono |
| Casi P13-P14 | Copie temporanee con segreto 1 e 20 | Vittoria al primo tentativo |
| Caso P15 | Risposta `sette` | `ValueError` in conversione |
| Nessuna lettura oltre l'esito | Sequenze N1-N3 con risposte in più | Contatori invariati, esito invariato |
| Casi motivati E1-E3 | Rifiuto alla quarta, vittoria dopo rifiuto, annullamento dopo due richieste | Atteso e osservato coincidono |
| Variante del limite | Copia temporanea con `limite_richieste = 3` | Arresto alla terza richiesta |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 4 — Gioco a tentativi*.
- Teoria di riferimento: cap. PY-05 — *Iterazione* e cap. PY-06 — *Dal
  problema al test*.
- Guida operativa: *Guida al debugger* nelle guide `dev-tools` del sito
  (sezione sui cicli).
