# Traccia del caso P04 — 1 → 2 → 3 → 7

Traccia di esecuzione del caso P04 con segreto 7 e limite 4. La colonna *riga*
indica quante istruzioni del ciclo sono già state eseguite per quella lettura;
lo stato è quello **dopo** la risposta indicata e prima della successiva. La
traccia coincide con l'esecuzione reale documentata in
[`casi-di-prova.md`](casi-di-prova.md).

| Lettura | Risposta | `richieste` | `tentativi_validi` | Confronti valutati | Stampa | `esito` |
|---|---:|---:|---:|---|---|---|
| inizio | — | 0 | 0 | — | — | `""` |
| 1 | 1 | 1 | 1 | `valore == 0` falso; `valore < minimo or valore > massimo` falso; `valore == segreto` falso; `valore < segreto` vero | `Il numero da trovare è maggiore.` | `""` |
| 2 | 2 | 2 | 2 | come sopra | `Il numero da trovare è maggiore.` | `""` |
| 3 | 3 | 3 | 3 | come sopra | `Il numero da trovare è maggiore.` | `""` |
| 4 | 7 | 4 | 4 | `valore == 0` falso; dominio ammesso; `valore == segreto` vero | — | vittoria, ciclo interrotto |
| fine | — | 4 | 4 | — | esito e i due contatori | vittoria |

## Cosa mostra la traccia

I due contatori avanzano insieme perché tutte le risposte sono dentro il
dominio: `richieste` cresce a ogni risposta non nulla, `tentativi_validi`
soltanto per gli interi validi confrontati col segreto. Il confronto
`valore == segreto` viene valutato **prima** del controllo `richieste ==
limite_richieste`: alla quarta lettura la vittoria ha precedenza
sull'esaurimento e il ciclo si interrompe con `break`, senza una quinta
lettura.

Con un rifiuto — per esempio sostituendo la quarta risposta con 21 — i due
contatori divergono: `richieste` diventa 4 e `tentativi_validi` resta 3, come
mostra il caso E1 di `casi-di-prova.md`.
