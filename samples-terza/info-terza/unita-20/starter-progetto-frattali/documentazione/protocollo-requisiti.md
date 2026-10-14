# Protocollo dei requisiti — Laboratorio dei frattali

Il documento elenca i requisiti obbligatori FR-01–FR-15 con l'evidenza
richiesta, le tappe FR-M1–FR-M8 con il criterio di passaggio e i casi
pubblici FR-A01–FR-A15 con lo stato iniziale. Si compila durante il lavoro:
ogni riga riceve lo stato (`da avviare`, `in corso`, `verificato`) e il
riferimento al file o al commit che la dimostra. La consegna sul sito
definisce testi completi, rubrica e variante personale.

## Requisiti obbligatori

| ID | Requisito | Evidenza | Stato |
|---|---|---|---|
| FR-01 | Curva/fiocco Koch e Sierpiński con livelli validati | Livelli 0/1/2, conteggi, orientamento e test | da avviare |
| FR-02 | Mandelbrot con seme zero e raggio 2 | Kernel e casi M-01–M-07, immagine e didascalia | da avviare |
| FR-03 | Julia con parametro modificabile e raggio sicuro | Casi J-01–J-05, preset e immagine | da avviare |
| FR-04 | Complessi e regola `z²+c` spiegati | Traccia personale e spiegazione di prodotto/modulo | da avviare |
| FR-05 | Campionamento con rapporto d'aspetto conservato | Griglia canonica e figure proporzionate in due risoluzioni | da avviare |
| FR-06 | Palette deterministiche e legenda | `None` distinto da indice `0`, comportamento ripetibile | da avviare |
| FR-07 | GUI con controlli pertinenti, messaggi e rendering annullabile | Dimostrazione durante un lavoro e nuova generazione corretta | da avviare |
| FR-08 | Zoom, spostamento tramite centro e ripristino | Ampiezza/centro/rapporto verificati | da avviare |
| FR-09 | Configurazioni JSON delle quattro famiglie | Round-trip, schema e casi invalidi senza perdita di stato | da avviare |
| FR-10 | Esportazione dell'ultimo risultato completo in PNG | Riapertura e confronto di dimensioni/pixel/parametri | da avviare |
| FR-11 | Classi, composizione e un polimorfismo motivato | UML, contratti, sostituzione del componente e test | da avviare |
| FR-12 | Modello e algoritmi verificabili senza GUI | Suite avviata senza finestra, import senza effetti grafici | da avviare |
| FR-13 | Tipi, eccezioni, test, Ruff e progetto `uv` riproducibile | Comandi eseguiti e risultati in questo README | da avviare |
| FR-14 | Costi e scelte delle strutture analizzati | Conteggi/formule e breve esperimento motivato | da avviare |
| FR-15 | Git/GitHub, documentazione, dimostrazione e modifica dal vivo | Cronologia pertinente, clone riproducibile, spiegazione | da avviare |

## Tappe e criteri di passaggio

| Tappa | Risultato concreto | Criterio di passaggio |
|---|---|---|
| FR-M1 | Requisiti e modello: casi d'uso, responsabilità, UML iniziale, ambiente, test vuoti identificati come da completare | Distinzione dominio/UI/persistenza e primo commit |
| FR-M2 | Geometria: Koch e Sierpiński con dati e test | Conteggi, caso base, punti e orientamento |
| FR-M3 | Mandelbrot: kernel, contratto esito e matrice piccola | Casi esatti e spiegazione del budget |
| FR-M4 | Julia: parametro, raggio, preset e test | Seme/parametro distinti e caso `c=-6, z_0=3` |
| FR-M5 | Immagini: campionamento, palette, Pillow e PNG provvisorio | Griglia canonica e pixel riaperti |
| FR-M6 | Interfaccia: controlli, stato, blocchi, annullamento, zoom/ripristino | Interazione durante un lavoro, nessuna callback obsoleta |
| FR-M7 | Persistenza e qualità: JSON, PNG definitivo, errori, suite, Ruff e README | Round-trip e rigenerazione dopo caricamento |
| FR-M8 | Spiegazione e revisione: costi, UML finale, relazione, dimostrazione e modifica | Previsione, prova, modifica e nuovo test personale |

## Casi pubblici di accettazione

I casi FR-A01–FR-A15 sono implementati in `tests/test_pubblici.py` con
stato iniziale, azione ed esito osservabile. La valutazione aggiunge
varianti motivate e dimostrazione personale. I kernel possono essere
studiati negli esempi preparatori; integrazione, struttura e almeno una
variante personale significativa (palette documentata, vista/preset
motivato o controllo di caricamento con test) restano lavoro autonomo.
