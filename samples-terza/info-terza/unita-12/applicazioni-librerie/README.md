# Applicazioni delle librerie — Unità 12

Quattro applicazioni eseguibili, una per libreria richiesta dal syllabus, collegate dalle pagine di laboratorio dell'Unità 12. Ogni file mostra un esempio minimo spiegato, produce un risultato osservabile, contiene una variante con riscontro e dichiara il proprio errore pertinente.

| File | Libreria | Esempio | Variante con riscontro | Pagina |
|---|---|---|---|---|
| `turtle_u12.py` | `turtle` (standard) | poligono regolare con penna, rotazione e colore | numero dei lati cambiato e due figure separate | [Disegni con turtle](/info-terza/laboratori/laboratorio-python/unita-12-disegni-turtle/) |
| `tkinter_u12.py` | `tkinter` (standard) | calcolo puro + finestra `ttk` con `grid`, callback e `mainloop` | input non valido mostrato nella stessa finestra | [Interfaccia con tkinter](/info-terza/laboratori/laboratorio-python/unita-12-interfaccia-tkinter/) |
| `grafico_frequenze_u12.py` | `matplotlib` | barre delle frequenze già calcolate, `fig, ax`, `savefig` | dataset con parità e tabella equivalente | [Grafico delle frequenze](/info-terza/laboratori/laboratorio-python/unita-12-grafici-frequenze/) |
| `immagini_u12.py` | `Pillow` (`PIL`) | apertura, conversione RGB, inversione punto per punto, salvataggio in file nuovo | confronto con `ImageOps.invert` e originale invariato | [Immagini con Pillow](/info-terza/laboratori/laboratorio-python/unita-12-immagini-pillow/) |

## Ambiente e comandi

`turtle` e `tkinter` appartengono alla libreria standard; `matplotlib` e `pillow` sono dipendenze esterne dichiarate in `pyproject.toml` e bloccate in `uv.lock`. Questa cartella è un **progetto applicativo dedicato**: si entra nella propria `.venv` con `uv sync`, senza installazioni globali e senza aggiungere dipendenze Python ad altri progetti.

```powershell
cd applicazioni-librerie
uv sync
uv run python --version
uv run python grafico_frequenze_u12.py
uv run python immagini_u12.py
uv run python turtle_u12.py
uv run python tkinter_u12.py
uv run python -m tkinter
```

Versioni della verifica: CPython 3.14.7, `uv` 0.12.15, matplotlib 3.11.2, pillow 12.3.0, Tk 9.0. `uv run python -m tkinter` apre la finestra di prova di Tcl/Tk: importare i moduli non apre nulla. I due script senza finestra producono i file in `output/`, cartella creata dallo script stesso e non versionata; i percorsi di output sono dichiarati nel codice.

## Esiti verificati

- `grafico_frequenze_u12.py`: salva `output/frequenze-canoniche.png` e `output/frequenze-pareggio.png` con il backend `Agg`, senza finestra; la tabella equivalente riporta `sole 3`, `luna 2`, `mare 1` nel dataset canonico e mantiene l'ordine alfabetico a parità in quello con parità.
- `immagini_u12.py`: immagine sintetica 4×4, pixel `(16, 16, 128)` → `(239, 239, 127)` dopo l'inversione, `confronta_imageops` vero, originale invariato dopo il salvataggio della copia invertita; la destinazione coincidente con la sorgente è rifiutata.
- `turtle_u12.py`: finestra Tk aperta, poligono a sei lati e due triangoli disegnati, chiusura programmata; la geometria (`angoli_poligono`, rotazioni di 90° sul quadrato) è verificabile anche con una penna di prova senza finestra.
- `tkinter_u12.py`: finestra reale con callback che produce `valore complessivo: 1,00 €` per `4 × 25` centesimi; la variante con input non valido mostra `input non valido: valore non valido: 'tre' non è un intero` nella stessa etichetta; `mainloop` termina regolarmente alla chiusura.

## Limiti dichiarati

L'importazione e il calcolo verificati non certificano da soli l'interazione visiva: i riscontri di finestra e clic sono esiti **separati**, registrati nella pagina del relativo laboratorio. `turtle` e `tkinter` richiedono Tcl/Tk nell'interprete effettivo; se la distribuzione di Python non lo fornisce, la diagnosi e la correzione seguono la documentazione della distribuzione stessa, senza istruzioni di installazione inventate. Il grafico è un'immagine statica prodotta da dati già calcolati: non sostituisce la tabella equivalente. La trasformazione di `immagini_u12.py` è punto per punto: il confronto con un filtro spaziale richiede di definire intorno e politica ai bordi e non è trattato qui.
