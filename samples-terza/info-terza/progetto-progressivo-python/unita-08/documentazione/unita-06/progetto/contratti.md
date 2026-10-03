# Contratti — totale ricorsivo dei preventivi (U6)

Documento della tappa U6, scritto prima del codice. La funzione aggiuntiva non
sostituisce il riepilogo iterativo di U5: è un **secondo procedimento** sullo
stesso problema, utile al confronto fra iterazione e ricorsione.

## Contratto

`totale_preventivi_ric(importi_cent: list[int], quanti: int) -> int`

- **Dominio**: lista di interi non negativi in **centesimi**; `quanti` intero
  con `0 <= quanti <= len(importi_cent)`; per le prove pubbliche al massimo 100
  elementi.
- **Risultato**: la somma dei primi `quanti` elementi della lista.
- **Effetti**: nessuno; la lista resta invariata.
- **Fuori contratto**: `quanti` maggiore della lunghezza, importi negativi e
  tipi non ammessi sono valori fuori precondizione; la funzione non è un
  validatore e non promette esiti per quegli input.

## Decomposizione scelta

La misura del problema è `quanti`, una **quantità** di elementi e non
l'indice dell'ultimo: l'indice dell'ultimo elemento del prefisso è
`quanti - 1`. Questa distinzione decide la forma del passo ricorsivo.

| Parte | Scelta |
|---|---|
| Base | `quanti = 0` → `0`: il prefisso vuoto ha somma nulla, anche su una lista non vuota |
| Riduzione | si toglie l'ultimo elemento del prefisso, passando da `quanti` a `quanti - 1` |
| Ricomposizione | `importi_cent[quanti - 1] + totale_preventivi_ric(importi_cent, quanti - 1)` |

Ogni chiamata riduce `quanti` di un'unità e si ferma alla base: la misura
decresce a ogni passo e non può proseguire all'infinito sul dominio ammesso.
Nessuno slicing, nessuna funzione annidata, nessun aumento del limite di
ricorsione.

## Traccia dei frame — caso PR05 `([250, 0, 750], 3)`

| Frame | Chiamata | Valore calcolato |
|---|---|---|
| 1 | `totale_preventivi_ric([250, 0, 750], 3)` | `750 +` risultato del frame 2 |
| 2 | `totale_preventivi_ric([250, 0, 750], 2)` | `0 +` risultato del frame 3 |
| 3 | `totale_preventivi_ric([250, 0, 750], 1)` | `250 +` risultato del frame 4 |
| 4 | `totale_preventivi_ric([250, 0, 750], 0)` | `0`, base |

Discesa: si apre un frame per ogni valore di `quanti` da 3 fino a 0, per una
profondità massima di 4 frame con il primo a profondità 1. Risalita: i frame
si chiudono nell'ordine inverso — 0, 250, 250 + 0, 1000 — e il risultato è
1000. Il **totale** calcolato (1000) e la **profondità** raggiunta (4) sono
grandezze diverse: la profondità cresce con `quanti`, non con la somma.

## Confronto con il riepilogo U5

Il riepilogo `riepilogo_preventivi` lavora su una lista di importi in **euro**
e restituisce `(numero, somma)`; `totale_preventivi_ric` lavora su una lista in
**centesimi**. Il confronto si fa sul totale completo:

```text
totale_preventivi_ric(importi_cent, len(importi_cent)) == somma_euro * 100
```

La conversione euro → centesimi (`importo_euro * 100`) si esegue **una sola
volta**, quando `importi_cent` viene costruita. Una seconda moltiplicazione
sugli importi già convertiti è un errore di unità, non di aritmetica: produce
totali cento volte maggiori senza nessun errore in esecuzione.

## Scelta da mantenere nell'uso ordinario

Per il lavoro ordinario resta il riepilogo iterativo: non consuma stack, è
lineare e leggibile. La versione ricorsiva resta come secondo procedimento da
confrontare, non come sostituto.
