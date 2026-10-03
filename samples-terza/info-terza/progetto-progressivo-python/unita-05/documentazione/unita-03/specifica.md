# Specifica — preventivo di spedizione di kit didattici (U3)

Listino fittizio e didattico per stimare il costo convenzionale di spedizione
di un kit: non rappresenta offerte commerciali.

| Dato | Nome | Tipo dopo la conversione | Dominio didattico |
|---|---|---|---|
| Peso del kit | `peso_g` | `int` | da 1 a 10.000 grammi inclusi |
| Destinazione | `destinazione` | `str` | esattamente `locale` oppure `nazionale` |
| Urgenza | `urgenza` | `str` | esattamente `s` oppure `n` |

Si effettua una sola acquisizione per ciascun dato: prima i tre testi, poi la
conversione del peso con `int`. Il contratto di conversione assume un testo
numerico convertibile: `mezzo chilo`, `1.5` o una riga vuota producono un errore
di conversione che questa versione non recupera.

## Validazione e priorità

Dopo la conversione i tre valori si validano con la priorità **peso →
destinazione → urgenza**. Un valore non ammesso produce **un solo messaggio** —
`Peso non ammesso`, `Destinazione non ammessa`, `Urgenza non ammessa` — e
nessuna riga di prezzo; se più campi sono errati prevale il primo secondo la
priorità. Il programma termina senza ripetere le domande. Non c'è
normalizzazione implicita: `S` non è `s` e `estero` non è `nazionale`.

## Listino e composizione

| Fascia di peso | Costo base per l'intera spedizione |
|---|---:|
| 1–500 g | 3 euro |
| 501–2000 g | 5 euro |
| 2001–10000 g | 8 euro |

Supplemento destinazione: `locale` 0 euro, `nazionale` 4 euro. Supplemento
urgenza: `n` 0 euro, `s` 2 euro. **Totale = costo base + supplemento
destinazione + supplemento urgenza**. I supplementi sono indipendenti e si
sommano; le fasce sono esclusive e non progressive: un kit da 501 g costa 5
euro di base, non 3 euro più una quota sull'eccedenza.

## Output

Sui dati validi: un riepilogo di peso, destinazione e urgenza, poi quattro
righe etichettate nell'ordine `Costo base`, `Supplemento destinazione`,
`Supplemento urgenza`, `Totale`, tutte con due cifre decimali e la parola
`euro`. Gli importi del listino sono interi: la composizione avviene sui
numeri e la formattazione soltanto sulle stringhe finali.

## Limiti della versione U3

Il testo del peso non convertibile produce `ValueError` senza recupero: è il
limite di conversione dichiarato dalla consegna, non un difetto da correggere
in questa tappa. Non ci sono ripetizioni delle richieste, funzioni definite
dall'utente né `try/except`.
