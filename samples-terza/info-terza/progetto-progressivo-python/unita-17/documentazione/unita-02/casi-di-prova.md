# Casi di prova — calcolatore del tempo di trasferimento (U2)

Esecuzione reale del programma con input predisposti. La colonna *atteso* è
stata scritta prima dell'esecuzione applicando le formule della
[`specifica.md`](specifica.md); la colonna *osservato* è l'output effettivo.
Per i casi P6-P8 l'esito è il traceback dell'interprete, riportato nelle righe
essenziali.

| Caso | Input | Atteso | Osservato |
|---|---|---|---|
| P1 | 150, 2.5, 10 | 60.00 / 70.00 / 1.17 | 60.00 / 70.00 / 1.17 |
| P2 | 600, 10, 0 | 60.00 / 60.00 / 1.00 | 60.00 / 60.00 / 1.00 |
| P3 | 0, 2.5, 10 | 0.00 / 10.00 / 0.17 | 0.00 / 10.00 / 0.17 |
| P4 | 1, 3, 0 | 0.33 / 0.33 / 0.01 | 0.33 / 0.33 / 0.01 |
| P5 | 1000000, 10000, 3600 | 100.00 / 3700.00 / 61.67 | 100.00 / 3700.00 / 61.67 |
| P6 | 150, 0, 10 | `ZeroDivisionError` al calcolo | `ZeroDivisionError: division by zero` sulla riga di `trasferimento_s` |
| P7 | 150, `2,5`, 10 | `ValueError` in conversione | `ValueError: could not convert string to float: '2,5'` |
| P8 | `cento`, 2.5, 10 | `ValueError` in conversione | `ValueError: invalid literal for int() with base 10: 'cento'` |
| P9 | -1, 2.5, 0 | risultato negativo non intercettato | -0.40 / -0.40 / -0.01 |

I valori di P1-P5 sono i tre risultati nell'ordine della consegna
(trasferimento in secondi, totale in secondi, totale in minuti).

## Due casi validi aggiuntivi, scelti e motivati

| Caso | Input | Perché è stato scelto | Atteso | Osservato |
|---|---|---|---|---|
| E1 | 2048, 128, 30 | dimensione non rotonda e velocità intera: verifica che il calcolo non dipenda da valori già comodi | 16.00 / 46.00 / 0.77 | 16.00 / 46.00 / 0.77 |
| E2 | 500, 0.5, 60 | velocità frazionaria vicina al minimo ammesso, con totale superiore a 15 minuti | 1000.00 / 1060.00 / 17.67 | 1000.00 / 1060.00 / 17.67 |

## Osservazioni sui casi non conformi

P6, P7 e P8 mostrano i limiti dichiarati della versione U2, non difetti da
correggere in questa tappa: `if` e `try/except` non sono fra i costrutti
ammessi. P9 mostra un dato numericamente convertibile ma fuori dominio: il
programma calcola comunque e produce risultati negativi, che non hanno senso
fisico. La distinzione fra i due gruppi è didattica: P7 e P8 falliscono nella
**conversione** del testo, P6 fallisce nel **calcolo**, P9 non fallisce affatto
e produce un risultato **fuori dominio**.

La conversione di P4 è il caso che mostra perché l'arrotondamento avviene solo
nella stampa: `1 / 3` vale circa `0.3333333333333333` e il totale in minuti
`0.00555...` viene stampato come `0.01`; se i valori intermedi fossero stati
troncati a due decimali prima del calcolo, il risultato finale sarebbe
diverso.
