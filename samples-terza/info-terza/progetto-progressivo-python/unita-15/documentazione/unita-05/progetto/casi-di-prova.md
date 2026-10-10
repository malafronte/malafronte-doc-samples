# Casi di prova — preventivo in funzioni (U5)

Attesi scritti prima dell'esecuzione dai contratti di
[`contratti.md`](contratti.md); osservati ottenuti dalla suite automatica e
dalle sessioni CLI. Negli importi il trattino significa **assenza di prezzo**,
non zero.

## Casi SP01-SP22 sulle funzioni

| Caso | Peso | Destinazione | Urgenza | Base | Dest. | Urg. | Totale o esito | Osservato |
|---|---:|---|---|---:|---:|---:|---|---|
| SP01 | 1 | locale | n | 3 | 0 | 0 | 3 | 3 |
| SP02 | 499 | locale | n | 3 | 0 | 0 | 3 | 3 |
| SP03 | 500 | locale | n | 3 | 0 | 0 | 3 | 3 |
| SP04 | 501 | locale | n | 5 | 0 | 0 | 5 | 5 |
| SP05 | 1999 | locale | n | 5 | 0 | 0 | 5 | 5 |
| SP06 | 2000 | locale | n | 5 | 0 | 0 | 5 | 5 |
| SP07 | 2001 | locale | n | 8 | 0 | 0 | 8 | 8 |
| SP08 | 10000 | nazionale | s | 8 | 4 | 2 | 14 | 14 |
| SP09 | 500 | nazionale | n | 3 | 4 | 0 | 7 | 7 |
| SP10 | 500 | locale | s | 3 | 0 | 2 | 5 | 5 |
| SP11 | 500 | nazionale | s | 3 | 4 | 2 | 9 | 9 |
| SP12 | 0 | locale | n | — | — | — | `Peso non ammesso` | `Peso non ammesso` |
| SP13 | -1 | locale | s | — | — | — | `Peso non ammesso` | `Peso non ammesso` |
| SP14 | 10001 | nazionale | n | — | — | — | `Peso non ammesso` | `Peso non ammesso` |
| SP15 | 100 | estero | n | — | — | — | `Destinazione non ammessa` | `Destinazione non ammessa` |
| SP16 | 100 | locale | S | — | — | — | `Urgenza non ammessa` | `Urgenza non ammessa` |
| SP17 | 0 | estero | forse | — | — | — | `Peso non ammesso` | `Peso non ammesso` |
| SP18 | 100 | estero | forse | — | — | — | `Destinazione non ammessa` | `Destinazione non ammessa` |
| SP19 | testo `mezzo chilo` | locale | n | — | — | — | `ValueError` in conversione CLI | `ValueError: invalid literal for int() with base 10: 'mezzo chilo'` (sessione manuale) |
| SP20 | 100 | stringa vuota | n | — | — | — | `Destinazione non ammessa` | `Destinazione non ammessa` |
| SP21 | 9999 | nazionale | s | 8 | 4 | 2 | 14 | 14 |
| SP22 | 100 | locale | forse | — | — | — | `Urgenza non ammessa` | `Urgenza non ammessa` |

SP01-SP18, SP20-SP22 sono verificati dalla suite automatica; SP19 è verificato
dalla sessione CLI perché riguarda la conversione fatta da `main`.

## Sessioni CLI ripetute manualmente

Le dieci sessioni richieste sono state eseguite con
`uv run python programmi/spedizione_u5.py` e i risultati coincidono con la
tabella. Esempi osservati:

```text
> uv run python programmi/spedizione_u5.py          (caso SP08)
Peso del kit in grammi interi (da 1 a 10000): 10000
Destinazione (locale o nazionale): nazionale
Urgenza (s o n): s
Peso: 10000 g
Destinazione: nazionale
Urgenza: s
Costo base: 8.00 euro
Supplemento destinazione: 4.00 euro
Supplemento urgenza: 2.00 euro
Totale: 14.00 euro
```

```text
> uv run python programmi/spedizione_u5.py          (caso SP17)
Peso del kit in grammi interi (da 1 a 10000): 0
Destinazione (locale o nazionale): estero
Urgenza (s o n): forse
Peso non ammesso
```

```text
> uv run python programmi/spedizione_u5.py          (caso SP19)
Peso del kit in grammi interi (da 1 a 10000): mezzo chilo
Destinazione (locale o nazionale): locale
Urgenza (s o n): n
Traceback (most recent call last):
  ...
  File "programmi/spedizione_u5.py", line 136, in main
    peso_g = int(peso_testo)
ValueError: invalid literal for int() with base 10: 'mezzo chilo'
```

## Casi SP-L01-SP-L06 sulle collezioni

| Caso | Operazione | Atteso | Osservato |
|---|---|---|---|
| SP-L01 | Registrare `3` in una lista vuota | lista `[3]`, ritorno `None` | come atteso |
| SP-L02 | Registrare `7` in `[3, 5]` | stessa lista `[3, 5, 7]` | come atteso, identità della lista conservata |
| SP-L03 | Anteprima con `7` da `[3, 5]` | nuova lista `[3, 5, 7]`, originale `[3, 5]` | come atteso, oggetto diverso |
| SP-L04 | Anteprima con `3` da `[]` | nuova lista `[3]`, originale `[]` | come atteso |
| SP-L05 | Riepilogo di `[3, 5, 7]` | `(3, 15)`, input invariato | come atteso |
| SP-L06 | Riepilogo di `[]` | `(0, 0)`, input invariato | come atteso |

## Tre casi propri motivati

| Caso | Input | Perché è stato scelto | Atteso | Osservato |
|---|---|---|---|---|
| PR-1 | 1200 g, nazionale, s | peso interno alla seconda fascia con entrambi i supplementi | 5 + 4 + 2 = 11 | 11 |
| PR-2 | 100 g, locale, urgenza vuota | il token vuoto non è `n`: nessuna normalizzazione ammessa | `Urgenza non ammessa` | `Urgenza non ammessa` |
| PR-3 | 501 g, locale, s | avrebbe rilevato il difetto della [`diagnosi.md`](diagnosi.md): totale senza il supplemento di urgenza | 5 + 0 + 2 = 7 | 7 |

## Import senza interazione

`import spedizione_u5` da un interprete nuovo non legge input e non stampa:
verificato con un processo che importa il modulo e termina. La guardia di
avvio separa il comportamento della CLI da quello della libreria.
