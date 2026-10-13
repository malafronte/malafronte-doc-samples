# Specifica — gioco a tentativi con numero assegnato (U4)

Il numero da trovare è un **dato assegnato nel sorgente**, `segreto = 7`, nel
dominio 1…20. Il limite è `limite_richieste = 4`. Gli estremi del dominio sono
`minimo = 1` e `massimo = 20`: ogni nome è definito una sola volta e usato nei
confronti, nei messaggi e nelle condizioni di arresto.

## Contratto di ogni lettura

1. si acquisisce un intero; il prompt dichiara il dominio 1…20 e 0 per
   annullare;
2. se il valore è 0 la partita termina come **annullamento**: la risposta non
   consuma una richiesta e non è un tentativo valido;
3. ogni altra risposta numerica aumenta `richieste` di 1, **anche se fuori
   intervallo**;
4. un valore fuori 1…20 produce `Valore fuori intervallo.`, non si confronta
   col segreto e non aumenta `tentativi_validi`;
5. un valore valido aumenta `tentativi_validi`; se è uguale al segreto
   dichiara vittoria e termina; se è minore indica `Il numero da trovare è
   maggiore.`; se è maggiore indica `Il numero da trovare è minore.`;
6. dopo quattro richieste non nulle, senza vittoria e senza annullamento, la
   partita termina per **richieste esaurite**;
7. si produce **un solo esito finale** fra vittoria, annullamento e richieste
   esaurite, seguito dalle due righe `Richieste usate: ...` e `Tentativi
   validi: ...`.

## I due contatori

`richieste` conta le risposte non nulle ricevute, comprese quelle fuori
intervallo: è il consumo del limite. `tentativi_validi` conta soltanto gli
interi dentro 1…20 confrontati col segreto. Un rifiuto fa crescere il primo
contatore e non il secondo: per questo i due valori differiscono nei casi con
rifiuti.

La vittoria alla quarta richiesta ha precedenza sull'esaurimento: il confronto
col segreto avviene prima del controllo del limite.

## Errori di dominio e di conversione

Un valore numerico fuori 1…20 è un **errore di dominio**: il programma lo
riconosce e risponde con il proprio messaggio. Un testo non convertibile con
`int` è un **errore di conversione**: questa versione non lo gestisce e il
programma si interrompe con `ValueError`, come documentato nei casi P15.
Nessuna lista, funzione definita dall'utente, casualità, eccezione gestita né
persistenza: il percorso essenziale usa soltanto assegnamenti, `input`,
conversioni, confronti, `while`, `if` e `break`.
