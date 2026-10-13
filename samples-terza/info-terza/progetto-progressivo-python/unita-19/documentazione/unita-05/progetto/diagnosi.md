# Diagnosi guidata — il totale che dimentica un supplemento (U5)

Questa scheda mostra come si diagnostica un difetto di composizione con la
suite di test. Il riferimento **non contiene il difetto**: il procedimento è
stato eseguito su una copia temporanea del sorgente corrotta di proposito, poi
eliminata. Non si racconta un errore personale né una sessione di debugger non
svolta: ogni esito riportato è stato realmente osservato.

## Sintomo

Il difetto considerato è la riga di `totale_spedizione` che omette il
supplemento di urgenza:

```python
# versione difettosa della copia temporanea
    return (
        costo_base_spedizione(peso_g)
        + supplemento_destinazione(destinazione)
    )
```

Sintomo osservato: i casi con `urgenza == "s"` producono un totale inferiore di
2 euro. Nessun errore in esecuzione: il programma risponde, ma sbaglia.

## Causa

Le tre funzioni di tariffazione sono corrette — `supplemento_urgenza("s")`
restituisce 2 — mentre la composizione non le chiama tutte. Il difetto è
nella **composizione**, non nei componenti: per questo una verifica delle sole
componenti non lo rileva e serve un caso che controlli il totale.

## Caso discriminante e esecuzione della suite

Sulla copia corrotta la suite è stata rieseguita: **6 fallimenti su 30 test**.

| Test fallito | Atteso | Osservato con il difetto |
|---|---:|---:|
| `test_sp08_massimo_con_entrambi_i_supplementi` | 14 | 12 |
| `test_sp10_supplemento_solo_urgenza` | 5 | 3 |
| `test_sp11_supplementi_indipendenti_e_sommati` | 9 | 7 |
| `test_sp21_peso_9999_terza_fascia_con_supplementi` | 14 | 12 |
| `test_proprio_1_seconda_fascia_con_entrambi_i_supplementi` | 11 | 9 |
| `test_proprio_3_totale_non_omette_il_supplemento_di_urgenza` | 7 | 5 |

I casi con urgenza `n` e i casi di validazione restano verdi: confermano che il
difetto riguarda la sola componente di urgenza. Il caso PR-3 è stato scritto
proprio per questo difetto e fallisce con 5 invece di 7.

## Modifica minima e nuova prova

Ripristinata la riga `+ supplemento_urgenza(urgenza)` nella composizione, la
suite rieseguita torna **30 superati** e le sessioni CLI di SP08 e SP10
producono i totali attesi. La regressione completa — suite e CLI — è il
controllo che chiude la diagnosi: una correzione è verificata soltanto quando
i casi che rilevavano il difetto tornano verdi **e** quelli che passavano
continuano a passare.

## Errore da evitare

Non correggere il difetto cambiando l'atteso del test: l'atteso nasce dal
contratto del listino e non dall'output osservato. Se un caso fallisce, prima
si confronta il contratto con il codice e poi si decide se il difetto è nel
codice — come qui — oppure nella lettura della consegna.
