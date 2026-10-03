# Specifica — calcolatore del tempo di trasferimento (U2)

Modello semplificato a velocità costante per stimare il tempo necessario a
trasferire un file quando sono noti dimensione, velocità media e tempo iniziale
di preparazione.

| Dato | Nome | Tipo dopo la conversione | Dominio didattico | Prompt |
|---|---|---|---|---|
| Dimensione | `dimensione_mb` | `int` | da 0 a 1.000.000 inclusi | `Dimensione in MB interi, zero ammesso: ` |
| Velocità | `velocita_mb_s` | `float` | numero finito da 0.01 a 10.000 inclusi | `Velocità in MB/s, punto decimale, minimo 0.01: ` |
| Preparazione | `preparazione_s` | `int` | da 0 a 3.600 inclusi | `Preparazione in secondi interi, zero ammesso: ` |

Formule: `trasferimento_s = dimensione_mb / velocita_mb_s`;
`totale_s = trasferimento_s + preparazione_s`; `totale_min = totale_s / 60`.
MB significa milioni di byte e MB/s la stessa convenzione al secondo: non si
tratta di megabit al secondo.

Limiti della versione U2: i domini delimitano il problema ma non sono
verificati automaticamente; gli input non conformi producono gli esiti
documentati in `casi-di-prova.md` senza recupero. I risultati si calcolano sui
valori convertiti, senza arrotondamenti intermedi: le due cifre decimali
compaiono soltanto nelle stringhe stampate.

Convenzioni di presentazione: il riepilogo stampa i dati convertiti con la loro
rappresentazione naturale — per questo la velocità `10` compare come `10.0`,
perché la conversione produce un `float` — seguito dai tre risultati
etichettati nell'ordine trasferimento in secondi, totale in secondi, totale in
minuti.
