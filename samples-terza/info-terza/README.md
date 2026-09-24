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
- `unita-07/esempi/stringhe_u7.py` - API delle stringhe per problemi: pulizia, prefissi, ricerca, conteggio, tokenizzazione e ricomposizione (cap. PY-11, parte I).
- `unita-07/esempi/liste_tuple_u7.py` - API delle liste e delle tuple, attraversamenti, comprehension e controesempio su `array.array` (cap. PY-11, parte II).
- `unita-07/esempi/riferimenti_copie_u7.py` - alias, riassegnamento, copia superficiale, ricostruzione riga per riga e tupla con elemento mutabile (cap. PY-11, parte III).
- `unita-07/esempi/matrici_u7.py` - matrici rettangolari con righe indipendenti, somme per riga e per colonna e trasposta (cap. PY-11, parte V).
- `unita-07/esempi/analizzatore_testi_u7.py` - analizzatore di testi completo di riferimento (LAB-PY-U7).
- `unita-07/esempi/osserva_alias_u7.py` - programma di osservazione per la sezione U7 della guida al debugger.
- `unita-07/esempi/problemi_algoritmici_u7.py` - soluzioni di riferimento dei dieci problemi della famiglia Sequenze, testi e matrici.
- `unita-07/starter-laboratorio/analizzatore_u7.py` - starter incompleto del LAB-PY-U7: costanti, firme e docstring, corpi da completare.
- `unita-07/starter-laboratorio/test_analizzatore_u7.py` - suite completa dello starter, con i casi pubblici L01-L14.

## Convenzioni

- I file sono sorgenti verificati con CPython 3.14; i test con `pytest` eseguiti dalla root della raccolta dello studente.
- Gli starter non contengono soluzioni: i TODO e i commenti indicano le parti da completare.
- Ogni modifica qui si riflette nel sito alla prossima build: prima di modificare un file, verificare le pagine che lo mostrano.
