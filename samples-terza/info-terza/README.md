# Codice Python del corso info-terza

Sorgenti Python di riferimento per il sito [info-terza](https://github.com/malafronte/info-terza). Le pagine del sito mostrano questi file con il componente `RemoteCode` oppure citano il percorso di questo repository; i file non sono distribuiti come download dal sito.

## Struttura

- `unita-01/starter-primo-progetto/main.py` — starter del primo progetto: `main.py` con TODO da completare.
- `unita-02/starter-calcolatore/rettangolo.py` — starter del calcolatore del rettangolo (LAB-PY-U2).
- `unita-03/prenotazione_sala.py` — programma monolitico della sala (cap. PY-04), baseline di debugger e rifattorizzazione.
- `unita-03/conferma_match.py` — conferma testuale con `match/case` su letterali e caso residuale (cap. PY-04).
- `unita-03/starter-mostra/tariffa_mostra.py` — starter della tariffa della mostra (LAB-PY-U3).
- `unita-04/esempi/somma_progressiva.py` — esempio completo dell'accumulatore (cap. PY-05).
- `unita-04/hardware/simulazione_livelli.py` — simulazione CPython dei livelli logici (LAB ESP-02).
- `unita-04/starter-statistiche/statistiche_temperature.py` — starter delle statistiche (LAB-PY-U4).
- `unita-05/esempi/sala_u5.py` — versione completa della lezione: funzioni annotate, `main` e guardia di avvio.
- `unita-05/esempi/test_sala_u5.py` — quindici test della sala (D01–D15).
- `unita-05/esempi/traccia_chiamate_u5.py` — listato canonico per la traccia delle chiamate (cap. PY-08 C).
- `unita-05/starter-mostra/mostra_prima_u5.py` - baseline monolitica della mostra (LAB-PY-U5).
- `unita-05/starter-mostra/test_mostra_u5.py` - starter di test: un caso completo, gli altri sono compito dello studente.
- `unita-06/esempi/ricorsione_lineare_u6.py` - funzioni ricorsive lineari: fattoriale, somma e MCD (cap. PY-10, parte I).
- `unita-06/esempi/traccia_fattoriale_u6.py` - fattoriale ricorsivo con tracciatore didattico per la discesa e la risalita dei frame (cap. PY-10, parte I).
- `unita-06/esempi/fibonacci_u6.py` - Fibonacci ricorsivo e iterativo a confronto (cap. PY-10, parte II).
- `unita-06/esempi/osserva_ricorsione_u6.py` - strumentazione di Fibonacci: ingressi totali e profondità massima (cap. PY-10, parte II).
- `unita-06/esempi/hanoi_u6.py` - generatore ricorsivo delle mosse della torre di Hanoi (cap. PY-10, parte III).
- `unita-06/esempi/test_ricorsione_u6.py` - suite di riferimento dei sorgenti d'esempio dell'Unità 6.
- `unita-06/starter-laboratorio/ricorsione_u6.py` - starter del LAB-PY-U6: versione di partenza da completare.
- `unita-06/starter-laboratorio/test_ricorsione_u6.py` - suite del LAB-PY-U6: versione di partenza.
- `unita-07/esempi/stringhe_u7.py` - API delle stringhe per problemi: pulizia, prefissi, ricerca, conteggio, tokenizzazione e ricomposizione (cap. PY-11, parte I).
- `unita-07/esempi/liste_tuple_u7.py` - API delle liste e delle tuple, attraversamenti, comprehension e controesempio su `array.array` (cap. PY-11, parte II).
- `unita-07/esempi/riferimenti_copie_u7.py` - alias, riassegnamento, copia superficiale, ricostruzione riga per riga e tupla con elemento mutabile (cap. PY-11, parte III).
- `unita-07/esempi/matrici_u7.py` - matrici rettangolari con righe indipendenti, somme per riga e per colonna e trasposta (cap. PY-11, parte V).
- `unita-07/esempi/analizzatore_testi_u7.py` - analizzatore di testi completo di riferimento (LAB-PY-U7).
- `unita-07/esempi/osserva_alias_u7.py` - programma di osservazione per la sezione U7 della guida al debugger.
- `unita-07/esempi/problemi_algoritmici_u7.py` - soluzioni di riferimento dei dieci problemi della famiglia Sequenze, testi e matrici.
- `unita-07/starter-laboratorio/analizzatore_u7.py` - starter incompleto del LAB-PY-U7: costanti, firme e docstring, corpi da completare.
- `unita-07/starter-laboratorio/test_analizzatore_u7.py` - suite completa dello starter, con i casi pubblici L01-L14.
- `unita-08/esempi/operazioni_collezioni_u8.py` - operazioni e controesempi su dizionari, viste, copie, chiavi hashable e insiemi (cap. PY-12, parti I-II).
- `unita-08/esempi/deduplicazione_raggruppamenti_u8.py` - deduplicazione stabile, ultime occorrenze, gruppi indipendenti e pattern di dizionario (cap. PY-12, parti II-III).
- `unita-08/esempi/record_catalogo_u8.py` - migrazione da liste parallele, record di catalogo, ricerca, aggiornamento e ordinamento (cap. PY-12, parte III).
- `unita-08/esempi/frequenze_u8.py` - conteggio esplicito delle parole, presentazione con politica di parità e confronto con `Counter` (cap. PY-12, parte IV).
- `unita-08/esempi/fibonacci_memoria_u8.py` - Fibonacci diretto, iterativo e con memoria esplicita, con conteggi C, D e S (cap. PY-12, parte V).
- `unita-08/esempi/test_esempi_u8.py` - suite di riferimento dei sorgenti d'esempio dell'Unità 8.
- `unita-08/starter-laboratorio/analizzatore_u8.py` - starter incompleto del LAB-PY-U8: costanti, firme e docstring, corpi da completare.
- `unita-08/starter-laboratorio/test_analizzatore_u8.py` - suite dello starter con i casi pubblici L01-L12 e L13 da progettare.
- `unita-08/riferimento-laboratorio/analizzatore_u8.py` - soluzione formativa delle quattro funzioni del LAB-PY-U8.
- `unita-08/riferimento-laboratorio/test_analizzatore_u8.py` - suite formativa completa del LAB-PY-U8, incluso un possibile caso L13.

## Convenzioni

- I file sono sorgenti verificati con CPython 3.14; i test con `pytest` eseguiti dalla root della raccolta dello studente.
- Gli starter non contengono soluzioni: i TODO e i commenti indicano le parti da completare.
- Ogni modifica qui si riflette nel sito alla prossima build: prima di modificare un file, verificare le pagine che lo mostrano.
