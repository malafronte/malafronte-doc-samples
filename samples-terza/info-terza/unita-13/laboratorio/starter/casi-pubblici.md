# Casi pubblici del laboratorio LAB-PY-U13

Ogni caso dichiara **risultato e stato atteso**, non soltanto che «funziona».
I casi vanno tradotti in test della propria suite: non servono dodici file
separati, una suite leggibile con un test per caso o raggruppamenti motivi
basta.

Convenzioni: `kit-a`, `kit-b` e `kit-c` sono etichette di depositi distinti;
la capacità è il numero massimo di kit; la quantità conta i kit **contenuti**.

| ID | Situazione | Operazione | Risultato atteso | Stato atteso |
|---|---|---|---|---|
| LAB13-01 | `nuovo_deposito("kit-a", 5, 0)` | costruzione | istanza valida | `quantita` 0, `capacita` 5, spazio libero 5 |
| LAB13-02 | `nuovo_deposito("kit-a", 0, 0)` | costruzione | istanza valida | `quantita` 0, `capacita` 0, spazio libero 0 |
| LAB13-03 | `nuovo_deposito("kit-a", 5, 0)` e `nuovo_deposito("kit-a", 5, 5)` | costruzione | due istanze valide | quantità iniziale ai due confini: 0 e 5 |
| LAB13-04 | `nuovo_deposito("kit-a", 5, 6)` | costruzione | `ValueError` motivato | nessun deposito prodotto |
| LAB13-05 | deposito 5/3 | `carica(deposito, 2)` | `True` | `quantita` 5, spazio libero 0 |
| LAB13-06 | deposito 5/3 | `carica(deposito, 3)` | `False` | `quantita` 3, spazio libero 2: **invariato** |
| LAB13-07 | deposito 5/3 | `preleva(deposito, 3)` | `True` | `quantita` 0, spazio libero 5 |
| LAB13-08 | deposito 5/3 | `preleva(deposito, 4)` | `False` | `quantita` 3, spazio libero 2: **invariato** |
| LAB13-09 | deposito 5/3 | `carica(deposito, -1)` oppure `carica(deposito, True)` | `ValueError` motivato | `quantita` 3: **invariato** |
| LAB13-10 | deposito 5/3 | `carica(deposito, 0)` | `True` | `quantita` 3: **invariato**. La quantità zero è un'operazione valida, non un errore |
| LAB13-11 | `primo` 5/0, `secondo` 5/0, `alias = primo` | `carica(primo, 3)`, `carica(secondo, 1)` | due esiti `True` | `primo` 5/3, `secondo` 5/1; `alias` osserva `primo` 5/3; mutare attraverso l'alias si vede da ogni nome collegato |
| LAB13-12 | deposito 5/0 | sequenza `carica(3)`, `preleva(4)`, `carica(2)`, `carica(1)`, `preleva(5)`, `carica(0)` | `True`, `False`, `True`, `False`, `True`, `True` | stati 3, 3, 5, 5, 0, 0. La variante a oggetti deve produrre **gli stessi esiti e gli stessi stati intermedi** |

## Oltre i casi pubblici

La suite deve comprendere anche **almeno un caso proprio** che la variante
difettosa non supera. Il caso va motivato per iscritto: quale errore rende
visibile, e perché i casi pubblici da soli non lo rivelerebbero.

Esempi di difetti che un caso proprio può smascherare:

- uno stato condiviso fra due istanze, perché il campo è stato scritto nel
  corpo della classe e non sull'istanza;
- un aggiornamento applicato **prima** del controllo, che su un rifiuto lascia
  un campo modificato e l'altro no;
- un metodo che aggiorna un nome locale invece dell'attributo e termina
  senza errori;
- una proiezione dello stato che restituisce il dizionario interno invece di
  una copia, permettendo una mutazione esterna nascosta.
