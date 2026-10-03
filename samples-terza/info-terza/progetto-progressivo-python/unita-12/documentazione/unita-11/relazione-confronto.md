# Relazione di confronto — strategie di ordinamento (U11)

Confronto fra due strategie stabili sullo stesso criterio — **ordinamento per
inserimento** (tappa U10) e **MergeSort stabile** (tappa U11) — con `sorted`
come riferimento concreto di CPython e oracolo per il risultato. Criterio
comune: `totale_cent` crescente, con la parità gestita dalla stabilità.

## Contratti ed effetti dei procedimenti

| Procedimento | Risultato | Effetti | Spazio aggiuntivo | Stack |
|---|---|---|---|---|
| `ordina_inserimento(elementi, chiave)` | lista **nuova** ordinata | nessuno sulla lista ricevuta | una lista di `n` riferimenti | costante, iterativo |
| `ordina_fusione(elementi, chiave)` | lista **nuova** ordinata | nessuno sulla lista ricevuta | Θ(n) per le liste di fusione | Θ(log n) di profondità, ricorsivo |
| `sorted(elementi, key=chiave)` | lista **nuova** ordinata | nessuno | Θ(n) | interno a CPython |

Tutti e tre condividono i **riferimenti ai record** con la lista di origine:
nessuna copia profonda, come dichiarato dai contratti U10. Entrambe le
strategie sono stabili: a parità di `totale_cent` conservano l'ordine relativo
del registro di origine, e il confronto con `sorted` — anch'esso stabile — lo
conferma.

## Scelta e previsioni prima della prova

L'inserimento confronta e sposta soltanto quanto basta per gli elementi
piccoli: quando la lista è già quasi ordinata fa `n-1` confronti, quando è in
ordine inverso arriva a `n(n-1)/2`. MergeSort dimezza sempre, qualunque sia
l'ordine iniziale, e paga invece la costante della fusione e dello spazio.
Previsione: inserimento vincente su input ordinati e quasi ordinati, MergeSort
più robusto su input avversi, `sorted` più rapido di entrambi per le costanti
dell'implementazione in C.

## Protocollo

- famiglie di input `ordinato`, `inverso`, `quasi_ordinato`, `molti_duplicati`,
  `pseudo_casuale`, costruite come dichiarato in
  `programmi/confronto_ordinamenti_u11.py`, con seme `20261003`;
- dimensioni `n = 200, 1000, 5000` record, sostenibili sulla postazione;
- **copie indipendenti** dello stesso originale per ogni procedimento: nessuna
  modifica ai dati sorgente passa inosservata;
- correttezza e parità verificate **prima** del timer: stesso multinsieme di
  record e stesso ordine dei marcatori per le due strategie e per `sorted`;
- misure con `time.perf_counter`, 5 ripetizioni, 5 chiamate per lotto, tutti i
  campioni conservati in
  [`risultati/unita-11/misure_u11.json`](../../../risultati/unita-11/misure_u11.json).

## Risultati — tempo di ordinamento

Mediane in millisecondi per chiamata. Postazione: Windows 11, CPython 3.14.7,
AMD Ryzen 7 8845HS, esecuzione normale.

| Famiglia | n | Inserimento | Fusione | `sorted` |
|---|---:|---:|---:|---:|
| ordinato | 200 | 0,049 | 0,270 | 0,011 |
| ordinato | 1.000 | 0,166 | 1,706 | 0,053 |
| ordinato | 5.000 | 0,793 | 9,955 | 0,338 |
| inverso | 200 | 2,790 | 0,286 | 0,011 |
| inverso | 1.000 | 73,743 | 1,688 | 0,054 |
| inverso | 5.000 | 2.762,640 | 14,924 | 0,383 |
| quasi_ordinato | 200 | 0,055 | 0,447 | 0,025 |
| quasi_ordinato | 1.000 | 0,238 | 2,597 | 0,084 |
| quasi_ordinato | 5.000 | 1,425 | 16,376 | 0,685 |
| molti_duplicati | 200 | 1,307 | 0,465 | 0,020 |
| molti_duplicati | 1.000 | 36,500 | 2,950 | 0,101 |
| molti_duplicati | 5.000 | 952,514 | 17,990 | 0,542 |
| pseudo_casuale | 200 | 2,008 | 0,572 | 0,023 |
| pseudo_casuale | 1.000 | 58,234 | 3,227 | 0,125 |
| pseudo_casuale | 5.000 | 1.474,705 | 19,978 | 1,024 |

Il grafico equivalente — famiglia `pseudo_casuale` sulle tre dimensioni — è in
[`risultati/unita-11/confronto_u11.png`](../../../risultati/unita-11/confronto_u11.png).

## Risultati — preparazione e query

Costo della **preparazione** della vista ordinata (una chiamata) e di una
sequenza di `q = 10` consultazioni sul **primo indice**, in millisecondi.

| Famiglia | n | Preparazione | 10 query |
|---|---:|---:|---:|
| ordinato | 5.000 | 0,815 | 0,015 |
| inverso | 5.000 | 2.645,781 | 0,029 |
| quasi_ordinato | 5.000 | 1,848 | 0,029 |
| molti_duplicati | 5.000 | 917,738 | 0,018 |
| pseudo_casuale | 5.000 | 1.608,645 | 0,021 |

La preparazione domina le consultazioni di due o cinque ordini di grandezza:
per `q = 10` la somma delle query è trascurabile rispetto al costruire l'ordine
e il conteggio teorico — Θ(q · log n) contro Θ(n²) dell'inserimento peggiore —
lo conferma. Le query lavorano su una vista già ordinata e non ripagano la
preparazione.

## Scelta motivata, non classifica

La scelta dipende da input e uso, non da una graduatoria:

- **pochi record o liste quasi ordinate** — inserimento: nessuna allocazione
  aggiuntiva, stack costante, `n-1` confronti nel caso favorevole. Su
  `quasi_ordinato` con `n = 5000` è sette volte più rapido della fusione;
- **ordine iniziale ignoto o avverso** — MergeSort: il comportamento resta
  stabile su ogni famiglia — fra 0,27 e 20 ms su `n = 5000` — mentre
  l'inserimento passa da 0,8 ms a 2,7 secondi;
- **molti record da consultare ripetutamente** — la preparazione si ammortizza
  su `q` grandi: il confronto fra procedimenti va fatto sulla somma
  preparazione + query, non sul solo ordinamento;
- **codice di produzione** — `sorted` è la scelta ragionevole: è il più
  rapido in ogni famiglia testata. Le funzioni del corso restano didattiche:
  servono a capire i procedimenti, non a battere CPython.

## Limiti

- Tre dimensioni e cinque famiglie su una sola postazione: i tempi non sono
  valori di accettazione e non dimostrano complessità asintotica. La robustezza
  di MergeSort sulle famiglie avverse **conferma** il modello Θ(n log n) contro
  Θ(n²), non lo dimostra.
- I casi peggiori dell'inserimento su `n = 5000` sono sostenibili solo appena:
  dimensioni maggiori non sono state misurate e non servono agli obiettivi.
- QuickSort non è stato incluso: sarebbe una terza strategia con stabilità da
  dichiarare e gestire separatamente. Due strategie stabili confrontabili
  bastano alla consegna.
- La famiglia `quasi_ordinato` è costruita con due scambi dichiarati: altri
  significati di «quasi ordinato» darebbero dati diversi.

## Verifiche di regressione

La suite U5-U10 è stata rieseguita senza modifiche ai contratti:
`uv run pytest -q` riporta 96 test superati, dei quali 10 di questa tappa.
Ordinamenti, viste e consultazioni delle tappe precedenti sono invariati.
