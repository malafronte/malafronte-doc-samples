# Casi di prova — preventivo di spedizione (U3)

Esecuzione reale del programma con input predisposti. L'atteso è stato scritto
applicando il listino della [`specifica.md`](specifica.md) prima
dell'esecuzione; l'osservato è l'output effettivo. Le colonne degli importi
riportano base, supplemento destinazione, supplemento urgenza e totale; un
trattino significa **nessun prezzo stampato**, non zero euro.

| Caso | Peso | Destinazione | Urgenza | Atteso | Osservato |
|---|---:|---|---|---|---|
| P01 | 1 | locale | n | 3.00 / 0.00 / 0.00 / 3.00 | 3.00 / 0.00 / 0.00 / 3.00 |
| P02 | 499 | locale | n | 3.00 / 0.00 / 0.00 / 3.00 | 3.00 / 0.00 / 0.00 / 3.00 |
| P03 | 500 | locale | n | 3.00 / 0.00 / 0.00 / 3.00 | 3.00 / 0.00 / 0.00 / 3.00 |
| P04 | 501 | locale | n | 5.00 / 0.00 / 0.00 / 5.00 | 5.00 / 0.00 / 0.00 / 5.00 |
| P05 | 1999 | locale | n | 5.00 / 0.00 / 0.00 / 5.00 | 5.00 / 0.00 / 0.00 / 5.00 |
| P06 | 2000 | locale | n | 5.00 / 0.00 / 0.00 / 5.00 | 5.00 / 0.00 / 0.00 / 5.00 |
| P07 | 2001 | locale | n | 8.00 / 0.00 / 0.00 / 8.00 | 8.00 / 0.00 / 0.00 / 8.00 |
| P08 | 10000 | nazionale | s | 8.00 / 4.00 / 2.00 / 14.00 | 8.00 / 4.00 / 2.00 / 14.00 |
| P09 | 500 | nazionale | n | 3.00 / 4.00 / 0.00 / 7.00 | 3.00 / 4.00 / 0.00 / 7.00 |
| P10 | 500 | locale | s | 3.00 / 0.00 / 2.00 / 5.00 | 3.00 / 0.00 / 2.00 / 5.00 |
| P11 | 500 | nazionale | s | 3.00 / 4.00 / 2.00 / 9.00 | 3.00 / 4.00 / 2.00 / 9.00 |
| P12 | 0 | locale | n | `Peso non ammesso` | `Peso non ammesso`, nessuna riga di prezzo |
| P13 | -1 | locale | s | `Peso non ammesso` | `Peso non ammesso`, nessuna riga di prezzo |
| P14 | 10001 | nazionale | n | `Peso non ammesso` | `Peso non ammesso`, nessuna riga di prezzo |
| P15 | 100 | estero | n | `Destinazione non ammessa` | `Destinazione non ammessa`, nessuna riga di prezzo |
| P16 | 100 | locale | S | `Urgenza non ammessa` | `Urgenza non ammessa`, nessuna riga di prezzo |
| P17 | 0 | estero | forse | `Peso non ammesso` | `Peso non ammesso`, prima priorità |
| P18 | 100 | estero | forse | `Destinazione non ammessa` | `Destinazione non ammessa`, seconda priorità |
| P19 | `mezzo chilo` | locale | n | `ValueError` in conversione | `ValueError: invalid literal for int() with base 10: 'mezzo chilo'` |

## Quattro prove aggiuntive, motivate

| Caso | Input | Perché è stato scelto | Atteso | Osservato |
|---|---|---|---|---|
| E1 | 1000, nazionale, s | peso interno alla seconda fascia con entrambi i supplementi | 5.00 / 4.00 / 2.00 / 11.00 | 5.00 / 4.00 / 2.00 / 11.00 |
| E2 | 500, `` (stringa vuota), n | token vuoto della destinazione: nessuna normalizzazione ammessa | `Destinazione non ammessa` | `Destinazione non ammessa` |
| E3 | 9999, nazionale, s | valore vicino al massimo ammesso, con entrambi i supplementi | 8.00 / 4.00 / 2.00 / 14.00 | 8.00 / 4.00 / 2.00 / 14.00 |
| E4 | regressione dopo una modifica | verifica che i casi di confine rilevino il cambiamento di una soglia | vedi sotto | vedi sotto |

## E4 — prova di regressione dopo una modifica

Su una **copia temporanea** del sorgente la soglia `if peso_g <= 500:` è stata
cambiata in `if peso_g <= 400:`; la copia è stata poi eliminata e il riferimento
canonico non è stato modificato. Riesecuzione dei casi di confine sulla copia:

| Caso | Atteso del riferimento | Osservato con la soglia cambiata | Discrimina? |
|---|---|---|---|
| P03 (500 g, locale, n) | 3.00 / 0.00 / 0.00 / 3.00 | 5.00 / 0.00 / 0.00 / 5.00 | sì |
| P04 (501 g, locale, n) | 5.00 / 0.00 / 0.00 / 5.00 | 5.00 / 0.00 / 0.00 / 5.00 | no |
| P11 (500 g, nazionale, s) | 3.00 / 4.00 / 2.00 / 9.00 | 5.00 / 4.00 / 2.00 / 11.00 | sì |

L'esito mostra due fatti utili: P03 e P11 sono casi di confine e rilevano la
modifica, mentre P04 non la rileva perché appartiene alla fascia successiva e
produce lo stesso risultato con entrambe le soglie. Una regressione è davvero
tale se i suoi casi distinguono il comportamento corretto da quello modificato.

## Osservazioni

P12-P18 verificano il rifiuto gestito: un solo messaggio, nella priorità
dichiarata, e nessuna riga di prezzo. P19 non è un caso da gestire in questa
tappa: mostra il limite di conversione. La sequenza di acquisizione è sempre
la stessa — tre testi e poi `int` — anche quando il peso non è convertibile:
in P19 il programma legge comunque tutte e tre le risposte prima di fallire.
