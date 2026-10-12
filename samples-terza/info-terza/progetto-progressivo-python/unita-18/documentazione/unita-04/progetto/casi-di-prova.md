# Casi di prova — gioco a tentativi (U4)

Esecuzione reale del programma con sequenze di risposte predisposte. Segreto 7,
limite 4 salvo indicazione. La colonna *esito* riporta l'esito finale seguito
dai contatori `richieste / tentativi_validi`; `maggiore` e `minore` descrivono
il numero da trovare rispetto a quello inserito.

| Caso | Risposte | Atteso | Osservato |
|---|---|---|---|
| P01 | 7 | Vittoria; 1 / 1 | Vittoria; 1 / 1 |
| P02 | 1 → 7 | maggiore, poi Vittoria; 2 / 2 | maggiore, poi Vittoria; 2 / 2 |
| P03 | 20 → 7 | minore, poi Vittoria; 2 / 2 | minore, poi Vittoria; 2 / 2 |
| P04 | 1 → 2 → 3 → 7 | maggiore ×3, poi Vittoria; 4 / 4 | maggiore ×3, poi Vittoria; 4 / 4 |
| P05 | 1 → 2 → 3 → 4 | maggiore ×4, poi Esaurite; 4 / 4 | maggiore ×4, poi Esaurite; 4 / 4 |
| P06 | -1 → 21 → 1 → 7 | fuori intervallo ×2, maggiore, poi Vittoria; 4 / 2 | come atteso; 4 / 2 |
| P07 | -1 → 21 → -2 → 22 | fuori intervallo ×4, poi Esaurite; 4 / 0 | come atteso; 4 / 0 |
| P08 | 0 | Annullamento; 0 / 0 | Annullamento; 0 / 0 |
| P09 | 1 → 0 | maggiore, poi Annullamento; 1 / 1 | come atteso; 1 / 1 |
| P10 | -1 → 0 | fuori intervallo, poi Annullamento; 1 / 0 | come atteso; 1 / 0 |
| P11 | 1 → 2 → 3 → 0 | maggiore ×3, poi Annullamento; 3 / 3 | come atteso; 3 / 3 |
| P12 | 1 → 20 → 1 → 20 | maggiore/minore alternati, poi Esaurite; 4 / 4 | come atteso; 4 / 4 |
| P13 | 1, con segreto 1 | Vittoria; 1 / 1 | Vittoria; 1 / 1 (copia temporanea) |
| P14 | 20, con segreto 20 | Vittoria; 1 / 1 | Vittoria; 1 / 1 (copia temporanea) |
| P15 | `sette` | `ValueError`, nessun esito regolare | `ValueError: invalid literal for int() with base 10: 'sette'` |

P13 e P14 sono stati eseguiti su copie temporanee del sorgente con `segreto`
modificato: il riferimento canonico non è stato toccato.

## Tre casi motivati

| Caso | Risposte | Perché è stato scelto | Atteso | Osservato |
|---|---|---|---|---|
| E1 | 1 → 2 → 3 → 21 | rifiuto alla quarta richiesta: il limite si consuma anche senza tentativi validi | Esaurite; 4 / 3 | Esaurite; 4 / 3 |
| E2 | -1 → 5 → 7 | vittoria dopo un rifiuto, con richieste ancora disponibili | fuori intervallo, maggiore, poi Vittoria; 3 / 2 | come atteso; 3 / 2 |
| E3 | 3 → 4 → 0 | annullamento dopo due richieste non nulle | maggiore ×2, poi Annullamento; 2 / 2 | come atteso; 2 / 2 |

## Nessuna lettura oltre l'esito

Il collaudo controlla il **numero di letture**, non solo l'ultima stampa: a
ogni sequenza sono state fornite risposte aggiuntive che, se lette, avrebbero
cambiato l'esito.

| Prova | Risposte fornite | Atteso | Osservato |
|---|---|---|---|
| N1 | 1 → 2 → 3 → 4 → **7** | Esaurite; 4 / 4, la quinta risposta non è letta | Esaurite; 4 / 4 |
| N2 | 0 → **7** | Annullamento; 0 / 0, la seconda risposta non è letta | Annullamento; 0 / 0 |
| N3 | 7 → **1** | Vittoria; 1 / 1, la seconda risposta non è letta | Vittoria; 1 / 1 |

## Variante del limite verificata

Su una copia temporanea con `limite_richieste = 3` (poi eliminata):

| Risposte | Atteso | Osservato |
|---|---|---|
| 1 → 2 → 3 | Esaurite; 3 / 3 | Esaurite; 3 / 3 |
| 1 → 2 → 7 | maggiore ×2, poi Vittoria; 3 / 3 | come atteso; 3 / 3 |

Il limite compare nel prompt come `massimo 3 richieste`: il nome unico
`limite_richieste` alimenta sia la condizione di arresto sia il messaggio.

## Osservazioni

P06 e P07 mostrano che i rifiuti consumano il limite senza produrre tentativi
validi; P12 mostra che entrambi gli estremi 1 e 20 sono valori validi e
confrontati col segreto; P11 mostra che 0 non consuma la quarta richiesta.
P15 appartiene alla classe degli errori di conversione: il testo non
convertibile non è un valore fuori dominio e questa versione non lo recupera.
